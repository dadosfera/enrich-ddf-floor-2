# /brd_browser_debug

Use MCP browser tools to debug front‑end issues by combining automation with **console logs**, **network requests**, and **page snapshots**. Always set up monitoring **before** performing any action.

Backlinks:

- `$BUDGET_DDF_REPO/docs/guides/browser-automation-mcp-tools.md`

## Command sequence (run in order)

1. Select the browser tool

- **Default (fast path)**: Use the **MCP Cursor Browser Extension** (`browser_*` tools) for quick debugging, console logs, network requests, and accessibility snapshots.
- **Advanced**: Use **MCP Puppeteer Browser** (`puppeteer_*` tools) only when you need screenshots, complex JavaScript execution, or deeper DevTools-style control.

2. Navigate to the target page

- With Cursor Browser:
  - Call `browser_navigate(url="http://localhost:<port>/<path>")`.
  - If needed, use `browser_wait_for(time=2)` followed by `browser_snapshot()` to confirm the page loaded.
- With Puppeteer:
  - Call `puppeteer_navigate(url="http://localhost:<port>/<path>")`.

3. Capture the baseline state (before any action)

- **Console**: `console_before = browser_console_messages()`
- **Network**: `network_before = browser_network_requests()`
- **URL**: `url_before = browser_evaluate("() => window.location.href")`
- **Snapshot (optional but recommended)**: `snapshot_before = browser_snapshot()`
- Treat these as your "before" set for comparisons.

4. Install in‑page monitoring (optional but recommended)

- Use `browser_evaluate` (or `puppeteer_evaluate`) to add lightweight debugging hooks:
  - Console interception: capture `log`, `warn`, and `error` into `window._debugConsoleLogs`.
  - URL monitoring: track history API usage and `window.location.href` changes into `window._debugUrlChanges`.
  - Network interception: wrap `fetch` and `XMLHttpRequest` to push entries into `window._debugNetworkRequests`.
- Retrieve these later via:
  - `browser_evaluate("() => window._debugConsoleLogs || []")`
  - `browser_evaluate("() => window._debugUrlChanges || []")`
  - `browser_evaluate("() => window._debugNetworkRequests || []")`

5. Perform the action under investigation

- Use Cursor Browser tools to reproduce the issue:
  - Clicks: `browser_click(element="<human label>", ref="<element ref>")`
  - Typing: `browser_type(element="<input label>", ref="<element ref>", text="...")`
  - Forms: `browser_fill_form(fields=[{...}])`
  - Hovers or key presses: `browser_hover(...)`, `browser_press_key(key="Enter")`
- If the action is multi-step (e.g., login + navigation), execute each step while keeping monitoring active.

6. Wait for async work to settle

- Use `browser_wait_for(time=2-3)` to allow network requests, rerenders, and URL updates to complete.
- If the app is particularly slow or rerun-heavy (e.g., Streamlit), increase the wait time modestly instead of repeating the action too quickly.

7. Capture the after state (post‑action)

- **Console**: `console_after = browser_console_messages()`
- **Network**: `network_after = browser_network_requests()`
- **URL**: `url_after = browser_evaluate("() => window.location.href")`
- **Snapshot**: `snapshot_after = browser_snapshot()`
- **Optional debug structures**:
  - `debug_console = browser_evaluate("() => window._debugConsoleLogs || []")`
  - `debug_network = browser_evaluate("() => window._debugNetworkRequests || []")`
  - `debug_url = browser_evaluate("() => window._debugUrlChanges || []")`

8. Compare before vs after

- **Console**:
  - `new_console = [m for m in console_after if m not in console_before]`
  - Focus on entries with `level == "error"` or containing navigation/query keywords.
- **Network**:
  - `new_network = [r for r in network_after if r not in network_before]`
  - Check that expected requests were fired (method, URL, status).
- **URL**:
  - `url_changed = url_before != url_after`
  - If the action should navigate but `url_changed` is false, suspect routing/query‑param issues.
- **Snapshot**:
  - Compare `snapshot_before` vs `snapshot_after` for structural changes (new buttons, sections, or missing elements).

9. Interpret common failure patterns

- **Navigation button does nothing**:
  - No URL change, no network requests, and console errors → likely JavaScript or routing bug.
  - URL changes but page state doesn't → query‑param or client state desync.
- **Form submit fails silently**:
  - Network requests missing → submit handler not firing.
  - Network requests present but console shows validation errors → client‑side validation blocking submit.
- **JavaScript errors**:
  - Filter console messages for `level == "error"`; extract key stack traces and error messages for follow‑up fixes.

10. Escalate with Puppeteer (if needed)

- When visual confirmation or advanced JS is required:
  - Use `puppeteer_screenshot(name="<slug>", selector="<optional selector>")` to capture the broken state.
  - Use `puppeteer_evaluate(script="...")` for more advanced in‑page inspection or to run longer debugging snippets.

## Notes

- Prefer the Cursor Browser Extension for **quick, iterative debugging**; only switch to Puppeteer when you need screenshots or deeper control.
- Always set up console and network monitoring **before** triggering the action; avoid reloading or repeating the action without capturing a fresh baseline.
- For cross‑repo details and full code snippets, see `$BUDGET_DDF_REPO/docs/guides/browser-automation-mcp-tools.md`.
