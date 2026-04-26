import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        # Wait until network is mostly idle to ensure UI loads properly
        await page.goto("https://github.com/codewithme-dev/OEL-SVV-Lab-", wait_until="networkidle")
        # Ensure we screenshot the full repo view
        await page.screenshot(path="screenshots/github_repo.png", full_page=True)
        await browser.close()

asyncio.run(main())
