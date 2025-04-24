# --- Prerequisites: ---
# 1. pip install playwright
# 2. playwright install chromium
# --- ---

import asyncio
from playwright.async_api import async_playwright
import os

# --- Configuration ---
html_file = 'index.html' # Assumes HTML is in the same directory
pdf_file = 'nikolay_dimitrov_cv_flex_layout.pdf' # New output name

async def html_to_pdf_playwright(html_path, pdf_path):
    # Ensure HTML path is absolute and uses file:/// scheme
    absolute_html_path = 'file:///' + os.path.abspath(html_path).replace('\\', '/')
    absolute_pdf_path = os.path.abspath(pdf_path)

    print("Starting Playwright...")
    async with async_playwright() as p:
        browser = None # Initialize browser variable
        try:
            # Launch Chromium (Playwright manages its download/location)
            print("Launching browser...")
            browser = await p.chromium.launch()
            page = await browser.new_page()
            print("Browser launched, new page created.")

            print(f"Navigating to: {absolute_html_path}")
            # Navigate to the local HTML file - wait until content is loaded
            await page.goto(absolute_html_path, wait_until='domcontentloaded')
            print("Page loaded.")

            # --- Emulate screen media type before PDF generation ---
            # This tries to ensure screen styles (like flexbox) are applied
            await page.emulate_media(media="screen")
            print("Emulating screen media.")

            # Give a brief moment for rendering adjustments after emulation
            await asyncio.sleep(1.5)

            print(f"Generating PDF: {absolute_pdf_path}")
            # Generate PDF using Playwright's method
            await page.pdf(
                path=absolute_pdf_path,
                format='A4',
                print_background=True, # Crucial for background colors
                margin={ # Standard margins
                    'top': '20mm',
                    'right': '20mm',
                    'bottom': '20mm',
                    'left': '20mm'
                }
                # Playwright will use print styles by default here,
                # but the flex layout is defined in the HTML's print styles now.
            )
            print(f"PDF generated successfully: {absolute_pdf_path}")
        except Exception as e:
            print(f"An error occurred during Playwright PDF generation: {e}")
        finally:
            if browser:
                await browser.close()
                print("Browser closed.")

# --- Run the async function ---
print(f"Attempting to convert '{html_file}' to '{pdf_file}' using Playwright...")
# Check if HTML file exists before running
if os.path.exists(html_file):
    asyncio.run(html_to_pdf_playwright(html_file, pdf_file))
else:
    print(f"Error: HTML file not found at '{os.path.abspath(html_file)}'")
print("Script finished.")