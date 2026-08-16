from dotenv import load_dotenv
from google import genai
from httpx2 import query
from playwright.sync_api import sync_playwright
from urllib.parse import quote_plus, urlparse, parse_qs
import base64
import os


# ==========================================
# 1. LOAD API KEY
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY was not found.")
    exit()


# ==========================================
# 2. CREATE GEMINI CLIENT
# ==========================================

client = genai.Client(
    api_key=api_key,
    http_options={"api_version": "v1"}
)

def decide_action(goal, current_page, state):

    print("\n[AI] Simulated decision-making...")
    print("[AI] Current state:", state)

    if state == "":
        action = "SEARCH"

    elif state == "search_completed":
        action = "OPEN"

    elif state == "page_opened":
        action = "BACK"

    elif state == "went_back":
        action = "DONE"

    else:
        action = "DONE"

    print("[AI] Decision:")
    print(action)

    return action

def run_agent(goal):

    print("\n==============================")
    print("       AGENT STARTED")
    print("==============================")

    current_page = ""
    state = ""

    for step in range(5):

        print(f"\n[AGENT] Step {step + 1}")

        action = decide_action(
    goal,
    current_page,
    state
)

        print("[AGENT] Action:", action)

        if action == "SEARCH":

            print("[AGENT] Searching...")
            
            current_page = search_web(goal)

            state = "search_completed"

        elif action == "OPEN":

            print("[AGENT] Opening page...")

            state = "page_opened"

            # We will connect this later.

        elif action == "BACK":

            print("[AGENT] Going back...")

            state = "went_back"

            # We will connect this later.

        elif action == "DONE":

            print("\n[AGENT] Task completed!")
            break

        else:

            print("[AGENT] Unknown action.")
            break
def choose_link_with_ai(goal, links):

    print("\n[AI] Asking Gemini to choose the best result...")

    # Give Gemini only the first 10 links
    links_text = ""

    for i, link in enumerate(links[:10], start=1):
        links_text += f"{i}. {link['text']}\n"
        links_text += f"URL: {link['url']}\n\n"

    prompt = f"""
You are helping a browser agent.

USER GOAL:
{goal}

Here are links found on a search engine:

{links_text}

Choose the single link that is most relevant to the user's goal.

Return ONLY the number of the link.

For example:
3
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    answer = response.text.strip()

    print("[AI] Gemini chose:")
    print(answer)

    try:
        choice = int(answer)

        if 1 <= choice <= len(links[:10]):
            return links[choice - 1]

    except ValueError:
        pass

    print("[AI] Gemini returned an invalid choice.")

    return None

class BrowserAgent:

    def click(self, selector):

        print("\n[BROWSER] Clicking:")
        print(selector)

        self.page.locator(selector).click()

        self.page.wait_for_timeout(3000)

        print("[BROWSER] Click completed.")

        print("\n[BROWSER] New URL:")
        print(self.page.url)

        print("\n[BROWSER] New page title:")
        print(self.page.title())

    def __init__(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.page = self.browser.new_page()

        print("\n[BROWSER] Browser started.")
    def search(self, query):

        print("\n[BROWSER] Searching for:")
        print(query)

        search_url = "https://www.bing.com/search?q=" + quote_plus(query)

        self.page.goto(search_url)

        self.page.wait_for_timeout(5000)

        print("\n[BROWSER] Search completed.")

        print("[BROWSER] URL:")
        print(self.page.url)

        print("\n[BROWSER] Title:")
        print(self.page.title())
    def open_page(self, url):

        print("\n[BROWSER] Opening:")
        print(url)

        self.page.goto(url)

        self.page.wait_for_timeout(3000)

        print("[BROWSER] Page opened.")

        print("\n[BROWSER] Title:")
        print(self.page.title())

        print("\n[BROWSER] URL:")
        print(self.page.url)
    def go_back(self):

        print("\n[BROWSER] Going back...")

        self.page.go_back()

        self.page.wait_for_timeout(3000)

        print("[BROWSER] Returned to:")
        print(self.page.url)

        print("\n[BROWSER] Page title:")
        print(self.page.title())
    def read_page(self):

        print("\n[BROWSER] Reading page...")

        page_text = self.page.locator("body").inner_text()

        print("\n[BROWSER] Page content:")
        print(page_text[:5000])

        return page_text
    
    def get_links(self):

        print("\n[BROWSER] Finding links...")

        links = self.page.locator("a").all()

        results = []

        for link in links:

            try:
                text = link.inner_text().strip()
                href = link.get_attribute("href")

                # Ignore empty or invalid links
                if not text:
                    continue

                if not href:
                    continue

                if href == "#":
                    continue

                if not href.startswith("http"):
                    continue

                if text.lower() in [
                    "images",
                    "videos",
                    "maps",
                    "news",
                    "shopping",
                    "all",
                    "more"
                ]:
                    continue

                results.append({
                    "text": text,
                    "url": href
                })

            except:
                pass

        print("\n[BROWSER] Valid links found:", len(results))

        for i, link in enumerate(results[:20], start=1):

            print(f"\nLINK {i}")
            print("Text:", link["text"])
            print("URL:", link["url"])

        return results

    def close(self):

        print("\n[BROWSER] Closing browser...")

        self.browser.close()

        self.playwright.stop()

# ==========================================
# 3. DEFINE A TOOL
# ==========================================

def search_web(query):

    print("\n[TOOL] search_web() was called!")
    print("[TOOL] Query:", query)

    with sync_playwright() as p:

        print("[TOOL] Starting browser...")

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        print("[TOOL] Opening Bing...")

        page.goto("https://www.bing.com")

        print("[TOOL] Bing opened.")

        search_url = "https://www.bing.com/search?q=" + quote_plus(query)

        print("[TOOL] Opening search URL:")
        print(search_url)

        page.goto(search_url)

        print("[TOOL] Search page opened.")

        page.wait_for_timeout(5000)

        print("[TOOL] Current URL:")
        print(page.url)

        print("[TOOL] Current page title:")
        print(page.title())

        print("[TOOL] Reading search results...")

        results = page.locator("li.b_algo")

        print("[TOOL] Number of results found:", results.count())

        clean_results = []

        for i in range(min(results.count(), 5)):

            result = results.nth(i)

            title = result.locator("h2").inner_text()

            link = result.locator("h2 a").get_attribute("href")

            if link and "bing.com/ck/a" in link:
                parsed = urlparse(link)
                params = parse_qs(parsed.query)

                if "u" in params:
                    encoded_url = params["u"][0]

                    try:
                        decoded = base64.b64decode(
                            encoded_url[2:] + "=="
                        ).decode("utf-8")

                        link = decoded
                    except Exception:
                        pass

            description = result.inner_text()

            clean_results.append({
    "title": title,
    "url": link,
    "description": description
})

        print("\n[TOOL] Clean search results:")

        for i, result in enumerate(clean_results):
            print(f"""
        RESULT {i + 1}
        Title: {result['title']}
        URL: {result['url']}
        Description:
        {result['description']}
        """)

        input("\nPress ENTER to close the browser...")

        return clean_results
def open_page(url):

    print("\n[TOOL] open_page() was called!")
    print("[TOOL] URL:", url)

    with sync_playwright() as p:

        print("[TOOL] Starting browser...")

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        print("[TOOL] Opening page...")

        page.goto(url)

        print("[TOOL] Page opened.")

        page.wait_for_timeout(3000)

        print("\n[TOOL] Page title:")
        print(page.title())

        print("\n[TOOL] Current URL:")
        print(page.url)

        print("\n[TOOL] Reading page...")

        page_text = page.locator("body").inner_text()

        print("\n[TOOL] Page content:")
        print(page_text[:5000])

        input("\nPress ENTER to close the browser...")

    return page_text
# ==========================================
# 4. DESCRIBE THE TOOL TO GEMINI
# ==========================================

search_tool = {
    "type": "function",
    "name": "search_web",
    "description": "Search the web for information.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to use."
            }
        },
        "required": ["query"]
    }
}


# ==========================================
# 5. ASK GEMINI TO USE THE TOOL
# ==========================================

goal = input("\nWhat should the agent do? ")

print("\nAsking Gemini...")




# ==========================================
# 6. CHECK FOR TOOL CALL
# ==========================================

print("\n==============================")
print("       MOCK AI AGENT")
print("==============================")

goal = input("\nWhat should the agent search for? ")

if "internship" in goal.lower() and "python" in goal.lower():
    query = "Python internships in Kolkata"
else:
    query = goal

print("\n[AGENT] Decided to search:")
print(query)

result = search_web(query)

print("\n==============================")
print("       AGENT FINAL RESULT")
print("==============================")

print(result)

# ==============================
# OPEN FIRST SEARCH RESULT
# ==============================

print("\n[AGENT] Opening the first result...")

first_url = result[0]["url"]

print("[AGENT] URL:", first_url)

page_content = open_page(first_url)

print("\n==============================")
print("       PAGE CONTENT READ")
print("==============================")

print(page_content)