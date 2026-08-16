from dotenv import load_dotenv
from google import genai
import os

# --------------------------------
# 1. Load the .env file
# --------------------------------

load_dotenv()

# Get the Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Check that the key exists
if not api_key:
    print("ERROR: GEMINI_API_KEY was not found in .env")
    exit()

# --------------------------------
# 2. Create the Gemini client
# --------------------------------

client = genai.Client(
    api_key=api_key,
    http_options={"api_version": "v1"}
)

# --------------------------------
# 3. Ask the user for a goal
# --------------------------------

goal = input("What should the agent do? ")

print("\n================================")
print("          AI AGENT")
print("================================")

print("\nGOAL:")
print(goal)

# --------------------------------
# 4. Send the goal to Gemini
# --------------------------------

prompt = f"""
You are the decision-making part of a simple browser agent.

The user has given you this goal:

{goal}

Decide what the agent should do FIRST.

Explain your decision briefly.

Then clearly state the first action the browser agent should perform.
"""

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=prompt
)

# --------------------------------
# 5. Display Gemini's response
# --------------------------------

print("\nAI DECISION:")
print(interaction.output_text)

print("\n================================")