
import sys
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse

async def url_to_pdf(url, output_filename):
    """
    Navigates to a URL, expands thinking traces, extracts the main content, 
    and saves it as a PDF.
    """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            print(f"Navigating to {url}...")
            await page.goto(url, wait_until='networkidle')
            
            main_content_selector = "main"
            await page.wait_for_selector(main_content_selector, timeout=60000)

            # Find and click all "Thought for..." dropdowns
            print("Expanding 'Thought for...' sections...")
            # Using a regex-like selector to find the buttons
            thought_dropdowns = page.locator('button:has-text("Thought for")')
            count = await thought_dropdowns.count()
            
            if count > 0:
                print(f"Found {count} 'Thought for...' section(s). Clicking to expand...")
                # Click all elements found
                for i in range(count):
                    await thought_dropdowns.nth(i).click()
                    # Brief pause to allow content to render
                    await asyncio.sleep(0.5)
            else:
                print("No 'Thought for...' sections found.")

            # A final wait to ensure all content is settled
            await asyncio.sleep(2)

            # Extract the HTML of the main content
            print("Extracting chat content...")
            chat_html = await page.inner_html(main_content_selector)
            
            # Create a new, clean page with only the chat content
            new_page = await browser.new_page()
            await new_page.set_content(f'''
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>ChatGPT Conversation</title>
                        <style>
                            body {{ font-family: sans-serif; margin: 40px; }}
                            /* Add any other styles needed for proper rendering */
                        </style>
                    </head>
                    <body>
                        {chat_html}
                    </body>
                </html>
            ''')

            print(f"Generating PDF: {output_filename}...")
            await new_page.pdf(path=output_filename, format='A4', print_background=True)
            
            await browser.close()
        print(f"Successfully created {output_filename}")
    except Exception as e:
        print(f"Error processing {url}: {e}")

def generate_filename_from_url(url):
    """
    Generates a clean PDF filename from a URL.
    """
    parsed = urlparse(url)
    path_part = parsed.path.lstrip('/').replace('/', '-')
    return f"chatgpt-{path_part}.pdf"

async def main():
    if len(sys.argv) < 2:
        print("Usage: poetry run python converter.py <url1> <url2> ...")
        sys.exit(1)

    urls = sys.argv[1:]
    
    for url in urls:
        if not url.startswith(('http://', 'https://')):
            print(f"Skipping invalid URL: {url}")
            continue
            
        output_filename = generate_filename_from_url(url)
        await url_to_pdf(url, output_filename)

if __name__ == "__main__":
    asyncio.run(main())
