"""Clone builder tests: static output is checked structurally; the AI path uses a mocked NVIDIA chat response."""
import asyncio, httpx, pytest
from fastapi.testclient import TestClient
from app import clone, config, jobs
from app.main import app

A = {
    "id": "c1", "target_url": "https://shop.example/", "status": "completed",
    "pages": [
        {"id": "p0", "path": "/", "title": "Home", "headings": ["Welcome"], "buttons": ["Go to login", "<b>x</b>"], "forms": [],
         "links": [{"text": "Login", "href": "/login"}, {"text": "Cart", "href": "https://shop.example/cart"}, {"text": "Ext", "href": "https://other.test/"}]},
        {"id": "p1", "path": "/login", "title": "Sign in", "headings": ["Sign in"], "buttons": ["Sign in"], "links": [],
         "forms": [{"action": "/login", "method": "post", "fields": ["email", "password"]}]},
        {"id": "p2", "path": "/cart", "title": "Cart", "headings": [], "buttons": ["Checkout"], "links": [],
         "forms": [{"action": "/checkout", "method": "post", "fields": ["coupon", "message"]}]},
    ],
    "edges": [{"id": "e0", "source": "p0", "target": "p1", "provenance": "observed", "action": "link 'Login'", "evidence": []}],
    "hypotheses": [],
}


@pytest.fixture(autouse=True)
def _nokey(monkeypatch):
    monkeypatch.setattr(config, "LLM_API_KEY", "")


def test_regression_forms_with_string_fields_do_not_crash():  # the old builder raised AttributeError here
    assert "<form" in clone.build_static(A)


def test_static_clone_has_one_view_per_page_router_and_typed_inputs():
    h = clone.build_static(A)
    assert h.count('class="view"') == 3 and "hashchange" in h
    assert 'type="password"' in h and 'type="email"' in h and "<textarea" in h and 'type="number"' not in h  # 'message' != 'age'
    assert 'data-go="/login"' in h  # "Go to login" fuzzily matches the Login link
    assert "&lt;b&gt;x&lt;/b&gt;" in h and "<b>x</b>" not in h  # observed text is escaped
    assert "https://other.test" not in h  # external links are not rendered


def test_static_is_default_without_key_and_ai_mode_notes_missing_key():
    r = asyncio.run(clone.build_clone(A))
    assert r["mode"] == "static" and r["filename"] == "clone-shop-example.html" and "Static clone" in r["note"]
    assert "No NVIDIA key" in asyncio.run(clone.build_clone(A, "ai"))["note"]


def test_requires_completed_analysis():
    with pytest.raises(ValueError):
        asyncio.run(clone.build_clone({**A, "status": "running"}))


def _client(h):
    return httpx.AsyncClient(transport=httpx.MockTransport(h))


GOOD = "<!DOCTYPE html><html><body><script>addEventListener('hashchange',()=>{});/* / /login /cart */</script></body></html>"


def test_ai_clone_used_when_valid(monkeypatch):
    monkeypatch.setattr(config, "LLM_API_KEY", "nvapi-test")
    seen = {}
    def h(req):
        import json; seen["body"] = json.loads(req.read()); seen["auth"] = req.headers["authorization"]
        return httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {"content": "```html\n" + GOOD + "\n```"}}]})
    r = asyncio.run(clone.build_clone(A, client=_client(h)))
    assert r["mode"] == "ai" and r["html"].startswith("<!DOCTYPE") and seen["auth"] == "Bearer nvapi-test"
    p = seen["body"]["messages"][0]["content"]
    assert "PAGE /login" in p and "email, password" in p and "/ -> /login" in p  # real fields/edges reach the prompt


@pytest.mark.parametrize("resp", [
    httpx.Response(500),
    httpx.Response(401),
    httpx.Response(200, json={"choices": [{"finish_reason": "length", "message": {"content": GOOD}}]}),               # truncated
    httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {"content": "<!DOCTYPE html><html><body>hi"}}]}),  # incomplete
    httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {"content": GOOD.replace("/cart", "")}}]}),       # route missing
])
def test_bad_ai_output_falls_back_to_static(monkeypatch, resp):
    monkeypatch.setattr(config, "LLM_API_KEY", "nvapi-test")
    r = asyncio.run(clone.build_clone(A, client=_client(lambda req: resp)))
    assert r["mode"] == "static" and "AI generation failed" in r["note"] and r["html"].count('class="view"') == 3


def test_clone_endpoint(monkeypatch):
    jobs.JOBS["c1"] = A
    c = TestClient(app)
    r = c.post("/api/analyses/c1/clone")
    assert r.status_code == 200 and r.json()["mode"] == "static" and r.json()["html"].startswith("<!DOCTYPE")
    assert c.post("/api/analyses/c1/clone", json={"mode": "bogus"}).status_code == 422
    assert c.post("/api/analyses/nope/clone").status_code == 404
    jobs.JOBS["c1"] = {**A, "status": "running"}
    assert c.post("/api/analyses/c1/clone").status_code == 409
    jobs.JOBS.pop("c1", None)


def test_spotify_clone_builder():
    spotify_analysis = {
        "id": "sp1",
        "target_url": "https://open.spotify.com",
        "status": "completed",
        "pages": [{"id": "p0", "path": "/", "title": "Spotify - Web Player", "headings": ["Today's Top Hits"], "buttons": ["Play"], "forms": [], "links": []}],
        "edges": [],
        "hypotheses": []
    }
    assert clone.is_music_app(spotify_analysis) is True
    res = clone.build_static(spotify_analysis)
    assert "Spotify - Web Player" in res
    assert "AudioContext" in res
    assert "playSynthChord" in res
    assert "Blinding Lights" in res
    assert "ctrl-play" in res


def test_fullstack_zip_export():
    jobs.JOBS["c1"] = A
    c = TestClient(app)
    zip_bytes = clone.build_fullstack_zip(A)
    assert len(zip_bytes) > 500
    import zipfile, io
    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    namelist = zf.namelist()
    assert "frontend/index.html" in namelist
    assert "backend/main.py" in namelist
    assert "backend/requirements.txt" in namelist
    assert "README.md" in namelist

    r = c.get("/api/analyses/c1/clone/zip")
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/zip"
    jobs.JOBS.pop("c1", None)


def test_structured_multi_file_app_generation():
    files = clone.build_project_files(A)
    # Check reusable components
    assert "frontend/src/components/Header.jsx" in files
    assert "frontend/src/components/Sidebar.jsx" in files
    assert "frontend/src/components/FormCard.jsx" in files
    assert "frontend/src/components/ActionCard.jsx" in files
    assert "frontend/src/components/Toast.jsx" in files
    # Check page modules
    assert "frontend/src/pages/HomePage.jsx" in files
    assert "frontend/src/pages/LoginPage.jsx" in files
    assert "frontend/src/pages/CartPage.jsx" in files
    # Check routing, styles, and entrypoint
    assert "frontend/src/router.jsx" in files
    assert "frontend/src/styles.css" in files
    assert "frontend/src/main.jsx" in files
    assert "frontend/src/App.jsx" in files
    assert "frontend/src/api.js" in files
    # Check configuration
    assert "frontend/package.json" in files
    assert "frontend/vite.config.js" in files
    assert "frontend/index.html" in files
    # Check standalone fallback
    assert "frontend/index.standalone.html" in files


def test_build_validation_success_and_failure():
    files = clone.build_project_files(A)
    valid, issues = clone.validate_project_build(files, A["pages"])
    assert valid is True
    assert len(issues) == 0

    # Failure 1: Corrupted package.json
    broken_files = dict(files)
    broken_files["frontend/package.json"] = "INVALID JSON"
    valid, issues = clone.validate_project_build(broken_files, A["pages"])
    assert valid is False
    assert any("package.json is invalid JSON" in err for err in issues)

    # Failure 2: Missing essential file
    missing_files = dict(files)
    del missing_files["frontend/src/router.jsx"]
    valid, issues = clone.validate_project_build(missing_files, A["pages"])
    assert valid is False
    assert any("Missing essential file: frontend/src/router.jsx" in err for err in issues)

    # Failure 3: Missing route in router
    unmapped_files = dict(files)
    unmapped_files["frontend/src/router.jsx"] = "export const routes = [];"
    valid, issues = clone.validate_project_build(unmapped_files, A["pages"])
    assert valid is False
    assert any("Route not mapped" in err for err in issues)


def test_complete_project_zip_integrity():
    import ast, io, json, zipfile
    zip_bytes = clone.build_fullstack_zip(A)
    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    
    # 1. CRC Check
    assert zf.testzip() is None, "ZIP archive corrupted"

    # 2. Package.json validity
    pkg_bytes = zf.read("frontend/package.json").decode("utf-8")
    pkg = json.loads(pkg_bytes)
    assert pkg["scripts"]["dev"] == "vite"
    assert "react" in pkg["dependencies"]

    # 3. Backend python syntax validity
    py_code = zf.read("backend/main.py").decode("utf-8")
    ast.parse(py_code)

    # 4. Vite config and entrypoint present
    assert "frontend/vite.config.js" in zf.namelist()
    assert "frontend/src/main.jsx" in zf.namelist()
    assert "frontend/src/App.jsx" in zf.namelist()


def test_safe_isolated_preview_endpoint():
    jobs.JOBS["c1"] = A
    c = TestClient(app)
    
    # Valid preview
    r = c.get("/api/analyses/c1/clone/preview")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "Content-Security-Policy" in r.headers
    assert "default-src 'self'" in r.headers["Content-Security-Policy"]
    assert r.headers["X-Frame-Options"] == "SAMEORIGIN"
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert "Home" in r.text

    # Missing preview returns 404
    r_bad = c.get("/api/analyses/nonexistent/clone/preview")
    assert r_bad.status_code == 404

    jobs.JOBS.pop("c1", None)

