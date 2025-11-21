# /brp-browser-pages

Run a first-level home → primary navigation pages visual smoke test with screenshots. This command validates the critical user journey from the home page through top navigation, sidebars, and key entry points, catching visual issues that HTTP 200 responses can miss.

**Required for**: UI/web repository PRs that affect front-end behavior (see `standards/4_10_planning_docs_ci_standards.md`).

Backlinks:

- `guides/tools/browser/browser_pages_visual_journey.md` — detailed guide on when and how to use this command
- `standards/4_10_planning_docs_ci_standards.md` — PR checklist requirement
- `rules/4_10_planning_docs_ci_standards.md` — normative requirement for front-end PRs

## Command sequence (run in order)

1. **Verify repository context**

   ```bash
   gtimeout 5 git rev-parse --show-toplevel
   ```

2. **Identify the application URL and port**

   - Determine the local development server URL (e.g., `http://localhost:3000` or `http://localhost:8501` for Streamlit)
   - If the server is not running, start it first

3. **Navigate to the home page**

   - Use MCP browser tools to navigate: `browser_navigate(url="http://localhost:<port>/")`
   - Wait for initial load: `browser_wait_for(time=2-3)`
   - Capture baseline: `home_snapshot = browser_snapshot()`

4. **Enumerate first-level navigation targets**

   - **Top navigation**: Identify tabs, menu items, or buttons in the header/top bar
   - **Left sidebar**: List all sidebar navigation links
   - **Right sidebar**: Note any quick links or secondary navigation
   - **Home cards/tiles**: Identify dashboard cards, report tiles, or form entry points on the home page
   - Keep the list focused on primary user entry points (typically 5-10 targets)

5. **For each navigation target** (starting from home each time):

   - **Navigate**: Use `browser_click(element="<human label>", ref="<element ref>")` or `browser_fill_form()` as appropriate
   - **Wait for render**: `browser_wait_for(time=2-4)` to allow data fetches and rerenders
   - **Capture structure**: `snapshot = browser_snapshot()` to inspect the rendered tree
   - **Capture visuals**:
     - With Cursor Browser Extension: `browser_take_screenshot(type="png", fullPage=true, filename="<page-slug>.png")`
     - With Puppeteer: `puppeteer_screenshot(name="<page-slug>", selector="body")`
   - **Perform visual checks** (using snapshot + screenshot):
     - **Not blank/black/white-only**: Verify there are visible headings, text blocks, and interactive elements. If the screenshot is essentially empty or a solid color, treat as failure even if status is 200.
     - **Contrast sanity**: Visually confirm text is readable against background (no light-on-light or dark-on-dark primary content).
     - **Layout boundaries**: Scan for obvious overflow (content cut off, horizontal scrollbars where none expected, elements overlapping, nav covering content).
     - **Defaults and placeholders**: Where inputs or filters exist, confirm sensible placeholder/default values are present (not blank where UX requires guidance).
     - **Real or seed data**: On list/table/chart pages, confirm that either realistic sample data or well-labeled "empty"/skeleton states are visible. An empty but supposedly "ready" page should be called out.
   - **If any visual check fails**:
     - Pull console errors: `console_messages = browser_console_messages()`
     - Pull recent network: `network_requests = browser_network_requests()`
     - Log failure: Note the home → page path, screenshot filename, and a short summary (e.g., "Home → Reports: blank page with 200, JS error in console")

6. **Generate summary report**
   - List all pages visited: `[home, page1, page2, ...]`
   - For each page, indicate: `✅ OK` or `❌ FAILED: <brief reason>`
   - Include screenshot filenames for reference
   - If failures found, recommend running `/browser-debug` on the specific failing page for deeper investigation

## Notes

- This command is a **visual smoke test**, not a comprehensive debugging tool. Use `/browser-debug` for deeper console/network investigation.
- Always start from the home page for each navigation target to ensure consistent state.
- Screenshots should capture the full page including header and sidebars (use `fullPage=true`).
- Visual checks are qualitative but critical—trust the screenshot over HTTP status codes.
- For UI/web repos, this command is **required** before merging PRs that affect front-end behavior (see `standards/4_10_planning_docs_ci_standards.md`).
