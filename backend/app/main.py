import asyncio
import io
import os
from pathlib import Path
import re
from urllib.parse import urlsplit

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import clone, config, db, domain_data, embeddings, jobs, llm, qa
from .demo_app import demo
from .inference import build_edges, infer
from .safety import UnsafeURL

app = FastAPI(title="BlackBox Atlas API")


class StartRequest(BaseModel):
    url: str = Field(default="demo", max_length=2048)
    demo: bool = False
    max_pages: int = Field(default=25, ge=1, le=100)
    time_limit_s: int = Field(default=120, ge=10, le=600)


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/config")
def get_config():  # capability flags only; secrets are never exposed
    return {"embeddings": {"enabled": embeddings.enabled(), "model": config.NVIDIA_EMBEDDING_MODEL if embeddings.enabled() else None, "provider": "NVIDIA"}, "llm": llm.enabled(), "qa": {"enabled": qa.enabled(), "model": config.LLM_MODEL if qa.enabled() else None}}


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=300)
    top_k: int = Field(default=8, ge=1, le=25)


@app.post("/api/analyses/{id_}/search")
async def search(id_: str, req: SearchRequest):
    a = jobs.JOBS.get(id_) or db.load(id_)
    if not a:
        raise HTTPException(404, "Analysis not found")
    if not embeddings.enabled():
        raise HTTPException(503, "Semantic search needs NVIDIA_API_KEY in the backend environment.")
    stored = db.load_embeddings(id_)
    if not stored:
        raise HTTPException(409, "This analysis has no stored embeddings (it ran without a key, or embedding failed).")
    model, vecs = stored
    try:
        (qv,) = await embeddings.embed([req.query], input_type="query")
    except embeddings.EmbeddingError as e:
        raise HTTPException(502, f"Embeddings provider error: {e}")
    if model != config.NVIDIA_EMBEDDING_MODEL:
        raise HTTPException(409, f"Stored vectors use model '{model}' but the server is set to '{config.NVIDIA_EMBEDDING_MODEL}'; re-run the analysis.")
    paths = {p["id"]: p for p in a["pages"]}
    return {"model": model, "results": [{**r, "path": paths[r["page_id"]]["path"], "title": paths[r["page_id"]]["title"]} for r in embeddings.rank(qv, vecs, req.top_k) if r["page_id"] in paths]}


@app.post("/api/analyses")
async def start(req: StartRequest, request: Request):
    origin = f"{request.url.scheme}://{request.url.netloc}"
    if req.demo:
        url, demo_origin, scope = f"{origin}/demo/", origin, "/demo"
    else:
        url, demo_origin, scope = req.url.strip(), None, "/"
    try:
        checker = await jobs.validate_target(url, demo_origin)
    except UnsafeURL as e:
        raise HTTPException(400, f"Target rejected: {e}")
    a = jobs.new_job(url, req.demo, req.max_pages, req.time_limit_s)
    task = asyncio.create_task(jobs.run(a, checker, scope))
    jobs.TASKS.add(task); task.add_done_callback(jobs.TASKS.discard)
    return {"id": a["id"]}


@app.get("/api/analyses")
def list_():
    return db.list_all()


@app.get("/api/analyses/{id_}")
def get(id_: str):
    a = jobs.JOBS.get(id_) or db.load(id_)
    if not a:
        raise HTTPException(404, "Analysis not found")
    return a


class ChatTurn(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(max_length=4000)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    history: list[ChatTurn] = Field(default_factory=list, max_length=20)


@app.post("/api/analyses/{id_}/ask")
async def ask(id_: str, req: AskRequest):
    a = jobs.JOBS.get(id_) or db.load(id_)
    if not a:
        raise HTTPException(404, "Analysis not found")
    if not qa.enabled():
        raise HTTPException(503, "Ask AI needs NVIDIA_API_KEY (or LLM_API_KEY) set in the backend .env.")
    if a.get("status") != "completed":
        raise HTTPException(409, "Wait for the analysis to complete before asking questions.")
    try:
        return await qa.answer(a, req.question.strip(), [t.model_dump() for t in req.history])
    except qa.QAError as e:
        raise HTTPException(502, f"AI provider error: {e}")


class CloneRequest(BaseModel):
    mode: str = Field(default="auto", pattern="^(auto|ai|static|app|multi)$")


@app.post("/api/analyses/{id_}/clone")
async def build_clone(id_: str, req: CloneRequest | None = None):
    a = jobs.JOBS.get(id_) or db.load(id_)
    if not a:
        raise HTTPException(404, "Analysis not found")
    try:
        return await clone.build_clone(a, (req or CloneRequest()).mode)  # yields structured multi-file app + static/AI HTML
    except ValueError as e:
        raise HTTPException(409, str(e))
    except Exception as e:
        raise HTTPException(500, f"Clone generation failed: {type(e).__name__}: {e}")


@app.get("/api/analyses/{id_}/clone/preview")
def preview_clone(id_: str):
    """Serves the clone application in a safe, isolated preview sandbox with strict CSP."""
    a = jobs.JOBS.get(id_) or db.load(id_)
    if not a:
        raise HTTPException(404, "Analysis not found")
    try:
        html_doc = clone.build_static(a)
        csp = (
            "default-src 'self' 'unsafe-inline' data: blob:; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "connect-src 'self' http://localhost:8000 http://127.0.0.1:8000; "
            "frame-ancestors 'self'"
        )
        return Response(
            content=html_doc,
            media_type="text/html",
            headers={
                "Content-Security-Policy": csp,
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "SAMEORIGIN",
                "Referrer-Policy": "no-referrer",
            }
        )
    except Exception as e:
        raise HTTPException(500, f"Failed to generate isolated preview: {e}")


@app.get("/api/analyses/{id_}/clone/zip")
def download_clone_zip(id_: str):
    a = jobs.JOBS.get(id_) or db.load(id_)
    if not a:
        raise HTTPException(404, "Analysis not found")
    try:
        zip_bytes = clone.build_fullstack_zip(a)
        host = urlsplit(a.get("target_url", "")).netloc or "app"
        clean_name = re.sub(r'[^a-z0-9]+', '-', host.lower()).strip('-')[:40] or "app"
        return Response(
            content=zip_bytes,
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="fullstack-{clean_name}.zip"'}
        )
    except Exception as e:
        raise HTTPException(500, f"Failed to build fullstack zip: {e}")


class InstantCloneRequest(BaseModel):
    url: str = Field(default="demo", max_length=2048)
    demo: bool = False


@app.post("/api/clone-instant")
async def clone_instant(req: InstantCloneRequest, request: Request):
    origin = f"{request.url.scheme}://{request.url.netloc}"
    if req.demo:
        url, demo_origin, scope = f"{origin}/demo/", origin, "/demo"
    else:
        url, demo_origin, scope = req.url.strip(), None, "/"
    try:
        checker = await jobs.validate_target(url, demo_origin)
    except UnsafeURL as e:
        raise HTTPException(400, f"Target rejected: {e}")

    a = jobs.new_job(url, req.demo, max_pages=1, time_limit=30)
    domain_pages = domain_data.get_domain_pages(url)
    if domain_pages:
        a["pages"] = domain_pages
        out_dict = {
            "pages": domain_pages,
            "path_to_id": {p["path"]: p["id"] for p in domain_pages},
            "redirect_map": {},
            "followed": [],
            "third_party": {}
        }
        a["edges"] = build_edges(out_dict)
        res = infer(out_dict, a["edges"])
        a.update(hypotheses=res["hypotheses"], missing_info=res["missing_info"], next_experiments=res["next_experiments"])
        a["status"] = "completed"
        jobs.db.save(a)
    else:
        await jobs.run(a, checker, scope)

    try:
        clone_res = await clone.build_clone(a, "auto")
        return {
            "id": a["id"],
            "analysis": a,
            **clone_res,
            "zip_url": f"/api/analyses/{a['id']}/clone/zip"
        }
    except Exception as e:
        raise HTTPException(500, f"Instant clone failed: {e}")


@app.post("/api/analyses/{id_}/cancel")
def cancel(id_: str):
    if id_ not in jobs.JOBS:
        raise HTTPException(404, "Analysis not found")
    jobs.CANCEL.add(id_)
    return {"ok": True}


app.mount("/demo", demo)
_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if _dist.exists():  # single-command mode: serve the built UI
    app.mount("/", StaticFiles(directory=_dist, html=True), name="ui")
