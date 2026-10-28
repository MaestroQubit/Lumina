"""Unit tests for domain intelligence and popular site clones (WhatsApp, Amazon, Spotify)."""
import zipfile
import io
from app import domain_data, clone, jobs


def test_domain_identification():
    assert domain_data.identify_domain("https://web.whatsapp.com") == "whatsapp"
    assert domain_data.identify_domain("https://www.whatsapp.com/features") == "whatsapp"
    assert domain_data.identify_domain("https://www.amazon.com/dp/B0CX234") == "amazon"
    assert domain_data.identify_domain("https://amazon.in") == "amazon"
    assert domain_data.identify_domain("https://open.spotify.com") == "spotify"
    assert domain_data.identify_domain("https://youtube.com/watch?v=123") == "youtube"
    assert domain_data.identify_domain("https://twitter.com/home") == "twitter"
    assert domain_data.identify_domain("https://unknown-random-app.com") is None


def test_whatsapp_pages_and_clone():
    url = "https://web.whatsapp.com"
    pages = domain_data.get_domain_pages(url)
    assert pages is not None
    assert len(pages) >= 4
    paths = {p["path"] for p in pages}
    assert "/" in paths
    assert "/status" in paths
    assert "/settings" in paths
    assert "/qr" in paths

    a = {
        "id": "wa1", "target_url": url, "status": "completed",
        "pages": pages, "edges": [{"source": "p0", "target": "p1", "action": "click status", "provenance": "observed"}]
    }
    assert clone.is_whatsapp_app(a) is True
    html = clone.build_static(a)
    assert "WhatsApp Web" in html
    assert "Alice Walker" in html
    assert "wa-message-input" in html

    files = clone.build_project_files(a)
    assert "backend/main.py" in files
    assert "WhatsApp Clone API" in files["backend/main.py"]
    assert "frontend/package.json" in files
    assert "frontend/index.standalone.html" in files

    zip_bytes = clone.build_fullstack_zip(a)
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
        names = zf.namelist()
        assert any(n.endswith("backend/main.py") for n in names)
        assert any(n.endswith("frontend/package.json") for n in names)


def test_amazon_pages_and_clone():
    url = "https://www.amazon.com"
    pages = domain_data.get_domain_pages(url)
    assert pages is not None
    assert len(pages) >= 4
    paths = {p["path"] for p in pages}
    assert "/" in paths
    assert "/cart" in paths
    assert "/checkout" in paths

    a = {
        "id": "amz1", "target_url": url, "status": "completed",
        "pages": pages, "edges": [{"source": "p0", "target": "p3", "action": "click cart", "provenance": "observed"}]
    }
    assert clone.is_amazon_app(a) is True
    assert clone.is_whatsapp_app(a) is False
    html = clone.build_static(a)
    assert "amazon" in html.lower()
    assert "MacBook Air" in html
    assert "Proceed to checkout" in html

    files = clone.build_project_files(a)
    assert "backend/main.py" in files
    assert "Amazon Clone API" in files["backend/main.py"]

    zip_bytes = clone.build_fullstack_zip(a)
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
        names = zf.namelist()
        assert any(n.endswith("backend/main.py") for n in names)
        assert any(n.endswith("frontend/package.json") for n in names)


def test_qa_synthesis_fallback():
    from app import qa
    pages = domain_data.get_domain_pages("https://web.whatsapp.com")
    a = {
        "id": "wa_qa", "target_url": "https://web.whatsapp.com", "status": "completed",
        "pages": pages, "edges": [], "hypotheses": [{"title": "Real-time Messaging", "description": "Websocket sync", "provenance": "observed", "confidence": "high"}]
    }
    ans = qa._synthesize_analytical_answer(a, "What does this app do?", [{"page_id": "p0", "score": 1.0}], "")
    assert "web.whatsapp.com" in ans
    assert "Real-time Messaging" in ans

    route_ans = qa._synthesize_analytical_answer(a, "What routes and pages exist?", [{"page_id": "p0", "score": 1.0}], "")
    assert "`/status`" in route_ans or "`/settings`" in route_ans
