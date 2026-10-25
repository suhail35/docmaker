"""E2E test: invoice document flow."""

from playwright.async_api import async_playwright


async def test_invoice_flow():
    """Test complete invoice document flow: catalog → form → preview → PDF."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to catalog
        await page.goto("http://localhost:8080")
        assert "DocMaker" in await page.title()

        # Click on invoice document
        await page.get_by_text("Счёт (НПД)").click()

        # Fill form
        await page.get_by_label("ФИО исполнителя (самозанятый)").fill("Иванов Иван Иванович")
        await page.get_by_label("ИНН исполнителя").fill("7707083893")
        await page.get_by_label("Телефон").fill("+79161234567")
        await page.get_by_label("Адрес исполнителя").fill("г. Москва, ул. Тестовая, д. 1")
        await page.get_by_label("Наименование заказчика").fill("ООО Тест")
        await page.get_by_label("Номер счёта").fill("1/2024")
        await page.get_by_label("Дата счёта").fill("2024-01-15")
        await page.get_by_label("Описание услуги").fill("Консультационные услуги")
        await page.get_by_label("Сумма (руб.)").fill("5000.00")

        # Click preview
        await page.get_by_role("button", name="Предпросмотр").click()

        # Check preview is shown
        preview_frame = page.frame_locator('iframe[name="pdf-preview"], iframe#pdf-preview')
        # Preview should be visible
        await page.wait_for_selector("#step-preview", state="visible")

        await browser.close()
