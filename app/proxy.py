"""Proxy for external data APIs with fallback chain."""

import json
import logging
import re
from typing import Any, Optional

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger("docmaker")

TIMEOUT = 10.0


async def fetch_by_inn(inn: str) -> Optional[dict[str, Any]]:
    """
    Fetch company/individual info by INN.
    Fallback chain: List-Org (HTML parsing) → Sber Self-Employed (API) → None
    """
    sources = [
        ("List-Org", _fetch_list_org, {"inn": inn}),
        ("Sber Self-Employed", _fetch_sber_self_employed, {"inn": inn}),
    ]

    for source_name, fetch_func, params in sources:
        try:
            data = await fetch_func(**params)
            if data:
                logger.info(f"Auto-fill by INN succeeded via {source_name}")
                return data
        except Exception as e:
            logger.warning(f"Auto-fill by INN failed via {source_name}: {e}")
            continue

    logger.info("Auto-fill by INN: all sources failed, using manual input")
    return None


async def _fetch_list_org(inn: str) -> Optional[dict[str, Any]]:
    """Parse List-org.com HTML search results for INN.

    Two page types:
    1. Short page (man/): contains link to company page
    2. Full page (company/): contains organization data directly
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True) as client:
            resp = await client.get(f"https://list-org.com/search?val={inn}")
            if resp.status_code == 200:
                # Try full page first
                data = _parse_list_org_full_page(resp.text, inn)
                if data:
                    return data

                # Try short page (follow link to company page)
                data = await _parse_list_org_short_page(resp.text, inn, client)
                if data:
                    return data
    except Exception as e:
        logger.warning(f"List-Org HTML parse failed: {e}")
    return None


def _parse_list_org_full_page(html: str, inn: str) -> Optional[dict[str, Any]]:
    """Parse full company page (company/12345) with org_list structure.

    Two formats:
    1. Company page: p contains "NAME...руководительLEADERинн/кппINN/KPPадресADDRESS"
    2. Search page: p contains "NAME (ИНН: XXX, TYPE)"
    """
    try:
        soup = BeautifulSoup(html, "html.parser")

        # Find the result card
        org_card = soup.find("div", class_="org_list")
        if not org_card:
            return None

        # Extract link (organization name)
        link = org_card.find("a")
        if not link:
            return None

        name = link.get_text(strip=True)

        # Get the paragraph with all data
        para = org_card.find("p")
        if not para:
            return None

        text = para.get_text()

        # Try format 1: "NAME...руководительLEADERинн/кппINN/KPPадресADDRESS"
        parts = re.split(r"(руководитель|инн/кпп|юр\.?адрес|адрес)", text, flags=re.IGNORECASE)
        if len(parts) >= 7:
            # Format 1 detected
            name = parts[0].strip()
            inn_kpp = parts[4].strip()
            inn_match = re.match(r"(\d{10,12})/", inn_kpp)
            if not inn_match:
                return None
            extracted_inn = inn_match.group(1)
            if extracted_inn != inn:
                return None
            address = parts[6].strip()
            org_type = ""
            name_upper = name.upper()
            for t in ["АО", "ЗАО", "ОАО", "ООО", "ИП"]:
                if t in name_upper:
                    org_type = t
                    break
            return {"name": name, "inn": inn, "type": org_type, "address": address}

        # Try format 2: "NAME (ИНН: XXX, TYPE)"
        inn_match = re.search(r"ИНН:\s*(\d+)", text)
        if inn_match and inn_match.group(1) == inn:
            # Extract type (ИП/ООО/etc)
            type_match = re.search(r"(ИП|ООО|АО|ЗАО|ОАО)", text)
            org_type = type_match.group(1) if type_match else ""
            return {"name": name, "inn": inn, "type": org_type}

        return None
    except Exception as e:
        logger.warning(f"List-Org full page parsing error: {e}")
        import traceback
        logger.warning(traceback.format_exc())
    return None


async def _parse_list_org_short_page(html: str, inn: str, client: httpx.AsyncClient) -> Optional[dict[str, Any]]:
    """Parse short search page (man/) and follow link to company page."""
    try:
        soup = BeautifulSoup(html, "html.parser")

        # Find link to company page
        # Short page structure: div.card > a[href="/company/XXX"] or a[href="/man/XXX"]
        company_link = soup.find("a", href=re.compile(r"/(company|man)/"))
        if not company_link:
            logger.debug("Short page: no company link found")
            return None

        href = company_link.get("href", "")
        if not href:
            return None

        # Build full URL
        if href.startswith("http"):
            url = href
        else:
            url = f"https://www.list-org.com{href}"

        logger.info(f"Short page: following link to {url}")

        # Fetch company page
        resp = await client.get(url)
        if resp.status_code == 200:
            return _parse_list_org_full_page(resp.text, inn)

        return None
    except Exception as e:
        logger.warning(f"List-Org short page parsing error: {e}")
        return None


async def _fetch_sber_self_employed(inn: str) -> Optional[dict[str, Any]]:
    """
    Check self-employed status via Sber API.
    NOTE: This is a placeholder. Real Sber API requires:
    - API key from Sber Developer Portal (https://developer.sber.ru)
    - Registration of application
    - OAuth2 authentication

    For now, returns None and logs the requirement.
    """
    # TODO: Implement real Sber API integration
    # API endpoint: https://api.sberbank.ru/techrepo/sdk-not-own/easyclient/dev/doc/java/classcom_1_1sbrf_1_1devtools_1_1sdk_1_1_easy_client.html
    # Or use Nalog.ru API: https://npd.nalog.ru/

    logger.info("Sber Self-Employed API: placeholder, requires API key")
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
