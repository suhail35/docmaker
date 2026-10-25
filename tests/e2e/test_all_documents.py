"""E2E test: all documents accessible."""

from playwright.async_api import async_playwright


async def test_all_documents_accessible():
    """Test that all 10 documents are accessible from catalog."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto("http://localhost:8080")

        # Check all document names are present
        documents = [
            "Счёт (НПД)",
            "Акт выполненных работ",
            "Договор возмездного оказания услуг",
            "Чек-подтверждение",
            "Договор дарения движимого имущества",
            "Расписка в получении денег",
            "Договор займа между физлицами",
            "Акт приёма-передачи",
            "Согласие на обработку ПДн",
            "Заявление-пояснение в ФНС",
        ]

        for doc_name in documents:
            element = page.get_by_text(doc_name)
            await element.scroll_into_view_if_needed()
            assert await element.is_visible(), f"Document '{doc_name}' not found"

        await browser.close()
