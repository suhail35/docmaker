"""DocMaker — Генератор юридических документов."""

import json
import logging
import os
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from weasyprint import HTML

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


# ── Import documents ────────────────────────────────────────────────────

from .documents import DOCUMENTS
from . import proxy as auto_fill_proxy


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


@app.get("/document/{doc_type}", response_class=HTMLResponse)
async def document_wizard(doc_type: str, request: Request):
    """Document wizard page."""
    if doc_type not in DOCUMENTS:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    doc_spec = DOCUMENTS[doc_type]
    return templates.TemplateResponse("document_wizard.html", {
        "request": request,
        "doc_type": doc_type,
        "doc_name": doc_spec["name"],
    })


# ── API ─────────────────────────────────────────────────────────────────

@app.post("/api/generate-pdf/{doc_type}", tags=["api"])
async def generate_pdf(doc_type: str, request: Request):
    """Generate PDF from form data."""
    if doc_type not in DOCUMENTS:
        return JSONResponse(
            status_code=404,
            content={"error": f"Unknown document type: {doc_type}"},
        )

    doc_spec = DOCUMENTS[doc_type]
    data_class = doc_spec["data_class"]

    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON body"},
        )

    # Build data from form fields
    filter_keys = set(data_class.__dataclass_fields__.keys())
    filtered = {k: v for k, v in body.items() if k in filter_keys}

    # Convert numeric fields from strings
    numeric_fields = {"service_amount", "work_amount", "price", "amount", "property_value",
                      "loan_amount", "service_amount"}
    for field in numeric_fields:
        if field in filtered and isinstance(filtered[field], str):
            try:
                filtered[field] = float(filtered[field])
            except (ValueError, TypeError):
                filtered[field] = 0.0

    try:
        data = data_class(**filtered)
    except (ValidationError, TypeError) as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)},
        )

    # Render HTML template
    html_str = templates.get_template(doc_spec["template"]).render(data=data)

    # Generate PDF
    pdf_bytes = HTML(string=html_str, base_url=".").write_pdf()

    return JSONResponse(content={
        "pdf": pdf_bytes.hex(),
        "filename": f"{doc_type}.pdf",
    })


@app.get("/api/auto-fill/inn/{inn}", tags=["api"])
async def auto_fill_by_inn(inn: str):
    """Auto-fill company info by INN."""
    data = await auto_fill_proxy.fetch_by_inn(inn)
    if data:
        return JSONResponse(content=data)
    return JSONResponse(content={})


@app.get("/api/auto-fill/bik/{bik}", tags=["api"])
async def auto_fill_by_bik(bik: str):
    """Auto-fill bank info by BIK."""
    data = await auto_fill_proxy.fetch_by_bik(bik)
    if data:
        return JSONResponse(content=data)
    return JSONResponse(content={})
