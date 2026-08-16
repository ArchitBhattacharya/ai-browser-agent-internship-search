# AI Browser Agent — Internship Search

A learning-focused AI browser agent built with Python, Google Gemini, and Playwright.

The project demonstrates how a Large Language Model can be combined with browser automation tools to interpret a natural-language goal, decide an action, interact with a real web browser, and extract useful information from web pages.

This project was built as a hands-on mock implementation to understand the fundamentals of browser-based AI agents before moving on to a larger browser-agent project.

---

## Overview

The goal of this project was to build an AI agent capable of receiving a natural-language request such as:

> Find Python internships in Kolkata

and using that goal to perform actions on the web.

The project combines:

- **Google Gemini** for language understanding and action decision-making
- **Playwright** for browser automation
- **Python** for the agent logic and tool implementation
- **Bing** as the search engine used during browser automation

The agent can search the web, extract search results, open a selected result, and read the contents of the resulting web page.

---

## Project Architecture

The project follows a basic AI-agent architecture:

```text
User Goal
    ↓
Gemini
    ↓
Action Decision
    ↓
Browser Tool
    ↓
Playwright
    ↓
Real Web Browser
    ↓
Search / Navigation
    ↓
Extract Web Content
    ↓
Return Information


The agent is intentionally designed as a simplified version of a browser-based AI agent. Instead of attempting to autonomously complete an entire workflow, it demonstrates the core loop of:

1. Understanding a user goal
2. Deciding what action to take
3. Calling a browser tool
4. Performing the action using Playwright
5. Extracting information from the page
6. Returning the result to the agent

---

## Features

### 1. Natural-Language Goal

The user can provide a goal in natural language, for example:

```text
Find Python internships in Kolkata
The goal is passed to Gemini, which interprets the request and determines the appropriate action.

2. Web Search

The agent can use a browser-controlled Bing search to search for information on the web.

For example:

Python internships in Kolkata

The browser is opened using Playwright and the search results are extracted from the page.

3. Search Result Extraction

The search tool extracts information such as:

Result title
Result URL
Result description

The extracted results are converted into structured Python data so they can be used by the agent.

Example:

RESULT 1
Title: Python Programming Internship at codegeeky in Kolkata
URL: https://...
Description: ...
4. Web Page Navigation

After obtaining search results, the agent can select a result and open the corresponding web page using Playwright.

5. Web Page Content Extraction

Once a page is opened, the agent reads the visible text from the page using Playwright.

This allows the agent to move beyond simply finding a webpage and actually inspect the information contained on it.

| Technology | Purpose |
|---|---|
| Python | Core agent and tool implementation |
| Google Gemini | Natural-language understanding and action decisions |
| Playwright | Browser automation |
| Bing | Web search |
| Git & GitHub | Version control and project hosting |
Project Files
ai-browser-agent/
│
├── agent.py
├── agent_browser.py
├── browser_test.py
├── tool_test.py
├── .gitignore
└── README.md

agent.py

Contains the initial agent logic and Gemini interaction used during experimentation.

agent_browser.py

Contains browser-related functionality used to interact with webpages through Playwright.

browser_test.py

Used to test browser functionality independently from the main agent.

It verifies that the browser can:

Launch
Open a URL
Read the page title
Read webpage content
tool_test.py

Contains the main experimental agent workflow.

It combines:

User input
Gemini-based decision making
Search functionality
Browser navigation
Webpage content extraction
.gitignore

Prevents local and sensitive files from being uploaded to GitHub.

Examples include:

.env
.venv/
__pycache__/
*.pyc
How the Agent Works

A typical execution follows this flow:

User
 │
 │ "Find Python internships in Kolkata"
 ▼
Gemini
 │
 │ Determines search action
 ▼
search_web()
 │
 ▼
Playwright
 │
 │ Opens browser
 ▼
Bing
 │
 │ Performs search
 ▼
Search Results
 │
 │ Extract title, URL and description
 ▼
Agent
 │
 │ Selects a result
 ▼
open_page()
 │
 ▼
Playwright
 │
 │ Opens selected webpage
 ▼
Web Page
 │
 │ Extract visible text
 ▼
Agent Result

This demonstrates the basic Perception → Decision → Action → Observation loop used by browser-based agents

Example Run

Example user input:

Find Python internships in Kolkata


The agent generates a search query:

Python internships in Kolkata


Playwright then launches a browser and performs the search.

The agent can extract results such as:

Python Programming Internship at codegeeky in Kolkata


Naukri — Python Internship Jobs in Kolkata

LinkedIn — Python Internship Jobs in Kolkata

Indeed — Python Internship Fresher Jobs in Kolkata

The agent can then open a selected result and extract the visible content from the webpage.

Gemini API Usage

Gemini is used as the reasoning component of the prototype.

The model is responsible for interpreting the user's goal and deciding which action should be performed.

For example:

Goal:


Find Python internships in Kolkata

Possible action:

SEARCH

Query:

Python internships in Kolkata

The browser itself does not perform the reasoning. Playwright is responsible for browser interaction, while Gemini provides the language-model component that helps determine the next action.

API Quota Limitation

During development, the Gemini API free tier quota was reached several times.

The API returned an error similar to:

429 RESOURCE_EXHAUSTED


This occurred because the free-tier request limit for the Gemini model being used was exceeded.

As a result, the full autonomous agent loop could not reliably make repeated Gemini decisions during testing.

This was a limitation of the development environment/API quota rather than a Playwright browser automation failure.

How the project was tested despite the limitation

The browser tools were tested independently from Gemini.

This allowed the following components to be verified:

Browser launching
Bing navigation
Search execution
Search-result extraction
URL navigation
Webpage content extraction

Therefore, the project demonstrates the browser-agent architecture and the browser automation components even though continuous Gemini-powered autonomous decision-making was limited by API quota.

Current Capabilities

The current prototype can:

Accept a natural-language search goal
Generate a search query using Gemini
Launch a real browser using Playwright
Search Bing
Extract multiple search results
Extract result titles, URLs and descriptions
Open a selected result
Read visible webpage content
Demonstrate an AI decision/action workflow
Current Limitations

This project is intentionally a learning-focused prototype and is not yet a fully autonomous browser agent.

Current limitations include:

Gemini API free-tier quota can limit repeated agent decisions.
The agent currently supports a relatively small set of browser actions.
Search-result handling is designed around the current Bing page structure.
Websites with anti-bot systems may interfere with browser automation.
The agent does not yet reliably complete multi-step workflows autonomously.
It does not currently submit internship applications automatically.
It does not maintain long-term memory between tasks.
It does not yet perform sophisticated result ranking or validation.
Dynamic websites may expose different content depending on their structure or login requirements.

These limitations are intentional for this mock implementation and provide the foundation for the next stage of development.

What I Learned

This project was built to understand the fundamentals of browser-based AI agents before working on a larger implementation.

Key concepts explored include:

Large Language Models as decision-making components
Tool calling
Browser automation
Playwright
Web navigation
Webpage content extraction
Agent action loops
Handling browser automation errors
Handling API rate limits and quotas
Separating AI reasoning from browser tools
Testing individual agent components independently
Future Improvements

Possible improvements for a production-level browser agent include:

Support for multiple browser actions
Better action planning
Multi-step task execution
Improved webpage understanding
Automatic result ranking
Website-specific interaction strategies
Robust handling of dynamic webpages
Memory between actions
Better error recovery
Support for additional search engines
Structured result storage
Automated application workflows where appropriate
Integration with a self-learning browser-agent infrastructure
Project Status

Status: Completed learning prototype

The primary objective of this project was to understand how an AI model and browser automation can work together to perform web-based tasks.

The prototype successfully demonstrates the core browser-agent components, while continuous autonomous reasoning is currently constrained by Gemini API free-tier quota limitations.

This project serves as a foundation for exploring more advanced browser-agent architectures