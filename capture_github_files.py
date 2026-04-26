import asyncio
from playwright.async_api import async_playwright

files_to_capture = {
    "requirements/analysis.md": "screenshots/github_requirements.png",
    "z-spec/SRCCS.tex": "screenshots/github_z-spec.png",
    "vdm/SRCCS.vdmpp": "screenshots/github_vdm.png",
    "alloy/SRCCS.als": "screenshots/github_alloy.png",
    "logs/verification.md": "screenshots/github_logs.png",
    "README.md": "screenshots/github_readme.png"
}

base_url = "https://github.com/codewithme-dev/OEL-SVV-Lab-/blob/main/"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        for file_path, save_path in files_to_capture.items():
            print(f"Capturing {file_path}...")
            target_url = base_url + file_path
            await page.goto(target_url, wait_until="networkidle")
            # Small delay to ensure code formatting completes
            await asyncio.sleep(2)
            await page.screenshot(path=save_path, full_page=True)
            print(f"Saved {save_path}")
            
        await browser.close()

asyncio.run(main())
