# --- Prerequisites: ---
# 1. pip install playwright
# 2. playwright install chromium
# --- ---

import asyncio
from playwright.async_api import async_playwright
import os

# --- Configuration ---
html_file = 'index.html' # Assumes HTML is in the same directory
main_pdf_file = 'nikolay_dimitrov_cv_main.pdf' # Output PDF for <main>
sidebar_pdf_file = 'nikolay_dimitrov_cv_sidebar.pdf' # Output PDF for <aside>

async def split_html_to_pdfs(html_path, main_pdf_path, sidebar_pdf_path):
    # Ensure HTML path is absolute and uses file:/// scheme
    absolute_html_path = 'file:///' + os.path.abspath(html_path).replace('\\', '/')
    absolute_main_pdf_path = os.path.abspath(main_pdf_path)
    absolute_sidebar_pdf_path = os.path.abspath(sidebar_pdf_path)

    print("Starting Playwright...")
    async with async_playwright() as p:
        browser = None # Initialize browser variable
        try:
            # Launch Chromium
            print("Launching browser...")
            browser = await p.chromium.launch()
            page = await browser.new_page()
            print("Browser launched, new page created.")

            # --- Generate PDF for MAIN content ---
            print(f"\n--- Generating PDF for <main>: {main_pdf_path} ---")
            print(f"Navigating to: {absolute_html_path}")
            await page.goto(absolute_html_path, wait_until='domcontentloaded')
            print("Page loaded for main content.")

            # Inject CSS to HIDE the sidebar and make main take full width for print
            await page.add_style_tag(content='''
                @media print {
                    aside.side-bar { display: none !important; }
                    main {
                        width: 100% !important;
                        flex-basis: 100% !important; /* Reset flex basis if using flex */
                        padding-right: 0 !important; /* Remove simulated gap */
                        float: none !important; /* Remove float if using float */
                    }
                    .container {
                        display: block !important; /* Reset container display if needed */
                    }
                }
            ''')
            print("CSS injected to hide sidebar.")
            await asyncio.sleep(1) # Short delay

            await page.pdf(
                path=absolute_main_pdf_path,
                format='A4',
                print_background=True,
                margin={'top': '20mm', 'right': '20mm', 'bottom': '20mm', 'left': '20mm'}
            )
            print(f"Main content PDF generated: {absolute_main_pdf_path}")

            # --- Generate PDF for SIDEBAR content ---
            print(f"\n--- Generating PDF for <aside>: {sidebar_pdf_path} ---")
            # Reload the page to clear previous CSS injection and state
            print(f"Reloading page: {absolute_html_path}")
            await page.goto(absolute_html_path, wait_until='domcontentloaded') # Use goto again for clean state
            print("Page reloaded for sidebar content.")

             # Inject CSS to HIDE the main content and make sidebar take full width for print
            await page.add_style_tag(content='''
                @media print {
                    main { display: none !important; }
                    aside.side-bar {
                        width: 100% !important;
                        flex-basis: 100% !important; /* Reset flex basis if using flex */
                        float: none !important; /* Remove float if using float */
                         box-shadow: none !important; /* Clean up print styles */
                         border-radius: 0 !important;
                    }
                     .container {
                        display: block !important; /* Reset container display if needed */
                    }
                }
            ''')
            print("CSS injected to hide main content.")
            await asyncio.sleep(1) # Short delay

            await page.pdf(
                path=absolute_sidebar_pdf_path,
                format='A4',
                print_background=True,
                margin={'top': '20mm', 'right': '20mm', 'bottom': '20mm', 'left': '20mm'}
            )
            print(f"Sidebar content PDF generated: {absolute_sidebar_pdf_path}")

        except Exception as e:
            print(f"An error occurred during Playwright PDF generation: {e}")
        finally:
            if browser:
                await browser.close()
                print("\nBrowser closed.")

# --- Run the async function ---
print(f"Attempting to split '{html_file}' into two PDFs...")
if os.path.exists(html_file):
    asyncio.run(split_html_to_pdfs(html_file, main_pdf_file, sidebar_pdf_file))
else:
    print(f"Error: HTML file not found at '{os.path.abspath(html_file)}'")
print("Script finished.")