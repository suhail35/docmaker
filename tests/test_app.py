"""Tests for main app routes."""

import pytest
from httpx import AsyncClient


class TestRoutes:
    @pytest.mark.asyncio
    async def test_health(self, client: AsyncClient):
        """Health check should return ok."""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data

    @pytest.mark.asyncio
    async def test_index(self, client: AsyncClient):
        """Index page should return 200."""
        response = await client.get("/")
        assert response.status_code == 200
        assert b"DocMaker" in response.content

    @pytest.mark.asyncio
    async def test_privacy(self, client: AsyncClient):
        """Privacy page should return 200."""
        response = await client.get("/privacy")
        assert response.status_code == 200
        assert "\u041f\u043e\u043b\u0438\u0442\u0438\u043a\u0430" in response.text

    @pytest.mark.asyncio
    async def test_document_wizard(self, client: AsyncClient):
        """Document wizard should return 200."""
        response = await client.get("/document/invoice")
        assert response.status_code == 200
        assert "\u0421\u0447\u0435\u0442" in response.text

    @pytest.mark.asyncio
    async def test_document_404(self, client: AsyncClient):
        """Unknown document should return 404."""
        response = await client.get("/document/unknown")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_all_documents_accessible(self, client: AsyncClient):
        """All 10 documents should be accessible."""
        from app.documents import DOCUMENTS
        for doc_type in DOCUMENTS:
            response = await client.get(f"/document/{doc_type}")
            assert response.status_code == 200, f"Document {doc_type} not accessible"
