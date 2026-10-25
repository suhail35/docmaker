"""Tests for proxy module."""

import json
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app import proxy


class TestFetchByInn:
    @pytest.mark.asyncio
    async def test_returns_none_on_all_failures(self):
        """When all sources fail, return None."""
        with patch("app.proxy.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.side_effect = Exception("Connection error")
            result = await proxy.fetch_by_inn("1234567890")
            assert result is None

    @pytest.mark.asyncio
    async def test_parses_list_org_html_success(self):
        """When List-Org returns HTML, parse it correctly."""
        html = """
        <html>
        <body>
        <div class="org_list">
            <a href="/profile/352901890320">TEST COMPANY LLC</a>
            <p>TEST COMPANY LLCруководительLEADERинн/кпп352901890320/123456789адресMOSCOW</p>
        </div>
        </body>
        </html>
        """
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.text = html

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)

        with patch("app.proxy.httpx.AsyncClient", return_value=mock_client):
            result = await proxy.fetch_by_inn("352901890320")
            assert result is not None
            assert result["name"] == "TEST COMPANY LLC"
            assert result["inn"] == "352901890320"

    @pytest.mark.asyncio
    async def test_returns_none_when_no_org_card(self):
        """When HTML has no org_list div, return None."""
        html = """
        <html>
        <body>
        <p>No organization found</p>
        </body>
        </html>
        """
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.text = html

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)

        with patch("app.proxy.httpx.AsyncClient", return_value=mock_client):
            result = await proxy.fetch_by_inn("1234567890")
            assert result is None


class TestFetchByBIK:
    @pytest.mark.asyncio
    async def test_returns_bank_info(self):
        """Should return bank info from local JSON."""
        result = await proxy.fetch_by_bik("044525225")
        assert result is not None
        assert "bank_name" in result
        assert "correspondent_account" in result

    @pytest.mark.asyncio
    async def test_returns_none_for_unknown_bik(self):
        """Should return None for unknown BIK."""
        result = await proxy.fetch_by_bik("000000000")
        assert result is None


class TestParseListOrgHtml:
    """Unit tests for HTML parsing logic."""

    def test_parses_real_structure(self):
        """Should parse real List-org HTML structure (format 1)."""
        html = """
        <div class="org_list">
            <a href="/company/62112">AO "R-FARM"</a>
            <p>AO "R-FARM"FULL NAMEруководительLEADERинн/кпп7726311464/773401001юр.адрес123154, MOSCOW, UL. TEST, D. 1</p>
        </div>
        """
        result = proxy._parse_list_org_full_page(html, "7726311464")
        assert result is not None
        assert result["name"] == 'AO "R-FARM"FULL NAME'
        assert result["inn"] == "7726311464"
        assert result["address"] == "123154, MOSCOW, UL. TEST, D. 1"

    def test_parses_ip_format(self):
        """Should parse ИП search page format (format 2)."""
        html = """
        <div class="org_list">
            <a href="/man/3199656">МАМАДКУЛОВ СУХАЙЛ ОЧИЛБОЙЕВИЧ</a>
            <p>МАМАДКУЛОВ СУХАЙЛ ОЧИЛБОЙЕВИЧ (ИНН: 352901890320, ИП)</p>
        </div>
        """
        result = proxy._parse_list_org_full_page(html, "352901890320")
        assert result is not None
        assert result["name"] == "МАМАДКУЛОВ СУХАЙЛ ОЧИЛБОЙЕВИЧ"
        assert result["inn"] == "352901890320"
        assert result["type"] == "ИП"

    def test_returns_none_on_inn_mismatch(self):
        """Should return None if INN in HTML doesn't match query."""
        html = """
        <div class="org_list">
            <a href="/company/123">OTHER COMPANY</a>
            <p>OTHER COMPANYруководительLEADERинн/кпп1234567890/123адресADDRESS</p>
        </div>
        """
        result = proxy._parse_list_org_full_page(html, "9999999999")
        assert result is None

    def test_returns_none_on_empty_html(self):
        """Should return None for empty HTML."""
        result = proxy._parse_list_org_full_page("", "1234567890")
        assert result is None

    def test_returns_none_on_missing_org_card(self):
        """Should return None when no org_list div exists."""
        html = "<html><body>No results</body></html>"
        result = proxy._parse_list_org_full_page(html, "1234567890")
        assert result is None

    def test_returns_none_on_bad_inn_format(self):
        """Should return None if INN/KPP format is invalid."""
        html = """
        <div class="org_list">
            <a href="/company/123">COMPANY</a>
            <p>COMPANYруководительLEADERинн/кппBADFORMATадресADDRESS</p>
        </div>
        """
        result = proxy._parse_list_org_full_page(html, "1234567890")
        assert result is None


class TestFetchCurrencyRate:
    @pytest.mark.asyncio
    async def test_returns_none_on_failure(self):
        """Should return None when API fails."""
        with patch("app.proxy.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.side_effect = Exception("Network error")
            result = await proxy.fetch_currency_rate("2024-01-01", "USD")
            assert result is None
