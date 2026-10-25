"""Tests for PDF generation."""

import pytest
from httpx import AsyncClient


class TestPDFGeneration:
    @pytest.mark.asyncio
    async def test_generate_invoice_pdf(self, client: AsyncClient):
        """Should generate valid PDF for invoice."""
        form_data = {
            "issuer_name": "Иванов Иван Иванович",
            "issuer_inn": "7707083893",
            "issuer_phone": "+79161234567",
            "issuer_address": "г. Москва, ул. Тестовая, д. 1",
            "recipient_name": "ООО Тест",
            "recipient_inn": "7701234567",
            "recipient_address": "г. Москва, ул. Примерная, д. 10",
            "invoice_number": "1/2024",
            "invoice_date": "2024-01-15",
            "service_description": "Консультационные услуги",
            "service_amount": "5000.00",
            "payment_method": "bank_transfer",
        }

        response = await client.post("/api/generate-pdf/invoice", json=form_data)
        assert response.status_code == 200
        data = response.json()
        assert "pdf" in data
        assert "filename" in data
        assert data["filename"] == "invoice.pdf"
        # PDF hex should be non-empty
        assert len(data["pdf"]) > 0

    @pytest.mark.asyncio
    async def test_generate_pdf_unknown_type(self, client: AsyncClient):
        """Should return 404 for unknown document type."""
        response = await client.post("/api/generate-pdf/unknown", json={})
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_generate_pdf_invalid_json(self, client: AsyncClient):
        """Should return 400 for invalid JSON."""
        response = await client.post(
            "/api/generate-pdf/invoice",
            content="not json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 400
