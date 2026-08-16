from playwright.sync_api import sync_playwright


def search_google(query):
    print("Starting browser...")

    with sync_playwright() as p:

        # Start Chromium
        browser = p.chromium.launch(headless=False)

        # Create a new page
        page = browser.new_page()

        print("Opening Google...")

        # Open Google
        page.goto("https://www.google.com")

        print("Google opened!")

        # Find Google's search box
        search_box = page.locator("textarea[name='q']")

        # Type the search query
        search_box.fill(query)

        print("Search query entered:", query)

        # Press Enter
        search_box.press("Enter")

        print("Search submitted!")

        # Wait for results to load
        page.wait_for_timeout(5000)

        print("Search results loaded!")

        # Keep the browser open for 5 more seconds
        page.wait_for_timeout(5000)

        # Close browser
        browser.close()

        print("Browser closed!")


# --------------------------------
# Main program
# --------------------------------

query = input("What should I search for? ")

search_google(query)