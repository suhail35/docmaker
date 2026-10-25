"""Proxy for external data APIs with fallback chain."""

import json
import logging
from typing import Any, Optional

import httpx

logger = logging.getLogger("docmaker")

TIMEOUT = 10.0


async def fetch_by_inn(inn: str) -> Optional[dict[str, Any]]:
    """
    Fetch company/individual info by INN.
    Fallback chain: List-Org → KontragentPro → Checko.ru → None
    """
    sources = [
        ("List-Org", "https://list-org.com/api/v1/list/member", {"number": inn}),
        ("KontragentPro", "https://kontragent.pro/api/free?inn={inn}", None),
        ("Checko", "https://api.checko.ru/v1/companies/{inn}", None),
    ]

    for source_name, url, params in sources:
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                if params:
                    resp = await client.get(url, params=params)
                else:
                    final_url = url.format(inn=inn)
                    resp = await client.get(final_url)

                if resp.status_code == 200:
                    data = resp.json()
                    logger.info(f"Auto-fill by INN succeeded via {source_name}")
                    return _parse_inn_response(data, source_name)
        except Exception as e:
            logger.warning(f"Auto-fill by INN failed via {source_name}: {e}")
            continue

    logger.info("Auto-fill by INN: all sources failed, using manual input")
    return None


async def fetch_by_bik(bik: str) -> Optional[dict[str, Any]]:
    """
    Fetch bank info by BIK from local JSON directory.
    """
    import os
    data_path = os.path.join(os.path.dirname(__file__), "data", "banks.json")
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            banks = json.load(f)
        for bank in banks:
            if bank.get("bik") == bik:
                return {
                    "bank_name": bank.get("name"),
                    "correspondent_account": bank.get("corresp_account"),
                }
    except Exception as e:
        logger.warning(f"Local bank lookup failed: {e}")
    return None


async def fetch_currency_rate(date: str, currency: str = "USD") -> Optional[float]:
    """
    Fetch currency rate from CBR API.
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.get(
                "https://www.cbr-xml-daily.ru/daily_json.js",
                params={"dateDef": date},
            )
            if resp.status_code == 200:
                data = resp.json()
                if "Valute" in data and currency in data["Valute"]:
                    return data["Valute"][currency]["Value"]
    except Exception as e:
        logger.warning(f"Currency rate fetch failed: {e}")
    return None


def _parse_inn_response(data: dict, source: str) -> Optional[dict]:
    """Parse API response into common format."""
    try:
        if source == "List-Org":
            # List-Org returns array of members
            if isinstance(data, list) and len(data) > 0:
                member = data[0]
                return {
                    "name": member.get("full_name") or member.get("short_name"),
                    "address": member.get("address"),
                    "director": member.get("position"),
                }
        elif source == "KontragentPro":
            if isinstance(data, dict):
                return {
                    "name": data.get("name"),
                    "address": data.get("address"),
                    "director": data.get("director"),
                }
        elif source == "Checko":
            if isinstance(data, dict):
                return {
                    "name": data.get("company_name"),
                    "address": data.get("address"),
                    "director": data.get("director_name"),
                }
    except Exception as e:
        logger.warning(f"Failed to parse {source} response: {e}")
    return None
