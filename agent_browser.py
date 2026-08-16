from dotenv import load_dotenv
from google import genai
from playwright.sync_api import sync_playwright
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


# ==========================================
# 3. BROWSER TOOL
# ==========================================

def search_google(query):

    print("\n[TOOL] Starting Google search...")
    print("[TOOL] Query:", query)

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        print("[TOOL] Opening Google...")

        page.goto("https://www.google.com")

        print("[TOOL] Google opened.")

        search_box = page.locator("textarea[name='q']")

        search_box.fill(query)

        print("[TOOL] Search entered.")

        search_box.press("Enter")

        print("[TOOL] Search submitted.")

        page.wait_for_timeout(5000)

        print("[TOOL] Search results loaded.")

        page.wait_for_timeout(5000)

        browser.close()

        print("[TOOL] Browser closed.")


# ==========================================
# 4. GET USER GOAL
# ==========================================

goal = input(
    "\nWhat should the agent do? "
)


print("\n================================")
print("        AI BROWSER AGENT")
print("================================")

print("\nGOAL:")
print(goal)


# ==========================================
# 5. ASK GEMINI WHAT TO DO
# ==========================================

prompt = f"""
You are the decision-making part of a browser agent.

The user's goal is:

{goal}

You have exactly ONE tool available:

search_google(query)

Your job is to decide whether this tool should be used.

If searching Google is appropriate, respond EXACTLY in this format:

SEARCH: <search query>

Do not add anything else.
"""

print("\n[AI] Asking Gemini for a decision...")


interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=prompt
)


decision = interaction.output_text.strip()


print("\n[AI] Decision:")
print(decision)


# ==========================================
# 6. EXECUTE THE AI'S DECISION
# ==========================================

if decision.startswith("SEARCH:"):

    query = decision.replace(
        "SEARCH:",
        "",
        1
    ).strip()

    print("\n[AGENT] Gemini selected the search tool.")

    search_google(query)

else:

    print("\n[AGENT] Gemini did not select a tool.")


print("\n================================")
print("           AGENT DONE")
print("================================")