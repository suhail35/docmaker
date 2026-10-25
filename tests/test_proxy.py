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
    async def test_returns_data_on_success(self):
        """When first source succeeds, return parsed data."""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"full_name": "Test LLC", "address": "Test addr"}]

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)

        with patch("app.proxy.httpx.AsyncClient", return_value=mock_client):
            result = await proxy.fetch_by_inn("1234567890")
            assert result is not None
            assert result["name"] == "Test LLC"


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


class TestFetchCurrencyRate:
    @pytest.mark.asyncio
    async def test_returns_none_on_failure(self):
        """Should return None when API fails."""
        with patch("app.proxy.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.side_effect = Exception("Network error")
            result = await proxy.fetch_currency_rate("2024-01-01", "USD")
            assert result is None
