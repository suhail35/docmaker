"""DocMaker — Генератор юридических документов."""

import logging
import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("docmaker")

app = FastAPI(title="DocMaker", version="0.1.0")

# Paths
_base_dir = os.path.dirname(os.path.abspath(__file__))
_static_dir = os.path.join(_base_dir, "static")
_templates_dir = os.path.join(_base_dir, "templates")

# Mount static files
app.mount("/static", StaticFiles(directory=_static_dir), name="static")

# Templates
templates = Jinja2Templates(directory=_templates_dir)


# ── Operations ──────────────────────────────────────────────────────────

@app.get("/health", tags=["operations"])
async def health():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}


# ── Pages ───────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page — document catalog."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
    """Privacy policy page."""
    return templates.TemplateResponse("privacy.html", {"request": request})
