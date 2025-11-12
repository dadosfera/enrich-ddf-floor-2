# Cursor/VSCode Terminal Profiles and Settings – Workspace vs User

This guide documents how integrated terminals behave in Cursor/VSCode, how workspace settings override user/global settings, and how to configure profiles to match your developer terminal reliably (colors, starship, venvs), without double-sourcing.

## Settings locations and precedence (highest to lowest)

- Workspace (Cursor): `.cursor/settings.json`
- Workspace (VSCode-compatible): `.vscode/settings.json`
- User (Global): `~/Library/Application Support/Cursor/User/settings.json`

Workspace settings override user/global settings. If behavior differs between AI/automation and your dev terminal, check workspace files first.

## Key terminal settings

- `terminal.integrated.defaultProfile.osx`

  - The default shell profile for interactive terminals you open manually
  - Accepts a profile name (e.g., `"zsh"`) or an object

- `terminal.integrated.tabs.defaultProfile.osx`

  - The default profile for new terminal tabs (may be in user settings)
  - Workspace settings override user/global settings
  - Typically set to `"zsh"` in user settings for consistency

- `terminal.integrated.automationProfile.osx`

  - The shell profile used by automation/agent terminals
  - Use object form to pass args and env
  - For zsh: prefer interactive mode (`-i`) so prompt/colors/starship load

- `terminal.integrated.shellIntegration.enabled`
  - When enabled, VSCode/Cursor injects helpers (e.g., `__vsc_prompt_cmd`)
  - May cause duplicate actuation effects (e.g., double activation prompts)
  - Disable in workspace for consistent, minimal behavior in automation

### Recommended workspace configuration (Cursor)

Place the following in `.cursor/settings.json`:

```json
{
  "terminal.integrated.defaultProfile.osx": "zsh",
  "terminal.integrated.automationProfile.osx": {
    "path": "/bin/zsh",
    "args": ["-i"],
    "env": {
      "TERM": "xterm-256color"
    }
  },
  "terminal.integrated.shellIntegration.enabled": false
}
```

Place the following in `.vscode/settings.json` (if present):

```json
{
  "terminal.integrated.shellIntegration.enabled": false,
  "terminal.integrated.automationProfile.osx": {
    "path": "/bin/zsh",
    "args": ["-i"],
    "env": {
      "TERM": "xterm-256color"
    }
  }
}
```

Notes:

- `-i` ensures zsh runs interactively so `.zshrc` loads (starship/colors)
- `TERM=xterm-256color` enables colorized output
- We disable shell integration in the workspace to avoid duplicate prompts

## Python extension settings and venv auto-activation

The Python extension can auto-activate environments in terminals. Misconfiguration can cause double-sourcing. Prefer explicit, correct paths:

- `python.defaultInterpreterPath`: Point to the real project venv interpreter
- `python.venvPath`: Point to the workspace root for consistency
- `python.terminal.activateEnvironment`: Set to `false` if you prefer manual activation or if double-sourcing is observed

Example (Cursor workspace):

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/budget_ddf_venv_py311/bin/python",
  "python.venvPath": "${workspaceFolder}",
  "python.terminal.activateEnvironment": false
}
```

For repos with conventional `venv` under workspace root:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.venvPath": "${workspaceFolder}",
  "python.terminal.activateEnvironment": false
}
```

## zsh behavior: `-i` vs `-l` and init files

zsh has separate concepts for login and interactive shells; they read different init files:

- `.zshenv`: read for all zsh invocations (login and non-login)
- `.zprofile`: read for login shells only (`-l` or login)
- `.zshrc`: read for interactive shells only (`-i`)

If your `.zshenv`/`.zshrc` contains early login exits (common for safety), then `zsh -l` may exit. Use `zsh -i` in automation profiles to ensure `.zshrc` is sourced and prompt/colors load.

If using starship, ensure `.zshrc` includes:

```zsh
eval "$(starship init zsh)"
```

## Shell integration and double-sourcing

Shell integration injects environment helpers that can interact with prompts and activation messages. When combined with Python auto-activation and various init scripts, this may produce duplicate activation prompts/echoes. Disabling shell integration at the workspace level makes automation terminals minimal and predictable.

## Troubleshooting checklists

- Prompt not colored / starship not loaded in agent terminals

  - Ensure automation profile uses `zsh -i`
  - Set `TERM=xterm-256color`
  - Confirm `.zshrc` contains `eval "$(starship init zsh)"`

- Double venv activation prompt

  - Set `python.terminal.activateEnvironment` to `false`
  - Confirm no auto-activation in `.zshrc`/`.zprofile`
  - Consider disabling shell integration in workspace

- Automation terminal differs from dev terminal
  - Verify workspace overrides in `.cursor/settings.json`
  - Match `defaultProfile` (manual) and `automationProfile` (agent)
  - Prefer `zsh -i` for automation so interactive config loads

## Verification commands

Run these from the project root to simulate a fresh automation shell:

```bash
# Fresh interactive zsh with minimal env (should load starship/colors)
env -i HOME="$HOME" USER="$USER" TERM="xterm-256color" SHELL="/bin/zsh" zsh -i -c 'echo $SHELL; echo $ZSH_VERSION; test -n "$VOLTA_HOME" && echo ok'
```

Check shell integration state and prompt injection:

```bash
# In automation terminal
printenv | grep -E '__vsc_prompt_cmd|VSCODE_INJECTION' || echo "shell integration not active"
```

Confirm Python interpreter path is correct:

```bash
# Should print the expected venv Python
cat .cursor/settings.json | grep -A1 "python.defaultInterpreterPath"
```

## Summary

- Use workspace settings to standardize terminal behavior across the team
- Prefer `zsh -i` for automation; set `TERM=xterm-256color`
- Disable shell integration in workspace to prevent double echo/sourcing
- Keep Python interpreter paths consistent with `${workspaceFolder}`
- Avoid Python auto-activation when it causes duplication

With these settings, automation/agent terminals should reliably match your dev terminal (colors, prompt, env), without double activation issues.
