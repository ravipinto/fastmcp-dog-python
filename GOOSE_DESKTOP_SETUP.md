# Using Dog MCP Server with Goose Desktop

This guide explains how to make the Python Dog MCP Server available in Goose Desktop.

## Current Status

Your Python Dog MCP Server is already configured for Goose CLI:
- **Location:** `/Users/ravi/.config/goose/config.yaml`
- **Server:** Dog MCP Server (Python version)
- **Status:** ✅ Enabled

## Option 1: Automatic (Recommended)

Goose Desktop likely **shares the same configuration** as Goose CLI. This means your server should already be available!

### Steps:

1. **Restart Goose Desktop**
   - Close Goose Desktop completely
   - Reopen it from Applications

2. **Check if the server is available**
   - Open Goose Desktop
   - Look for "Dog MCP Server" in the extensions or available tools
   - Try using the `randomDog` or `dogByBreed` tools

3. **Done!** ✅

If it works, you're all set! The server is automatically shared between CLI and Desktop.

---

## Option 2: Manual Configuration (If Automatic Doesn't Work)

If Goose Desktop doesn't recognize the server after restarting, follow these steps:

### Step 1: Access Goose Desktop Settings

1. Open **Goose Desktop** application
2. Look for a **Settings** or **Preferences** menu
3. Navigate to **Extensions** or **MCP Servers** section
4. Click **Add Extension** or **Add MCP Server**

### Step 2: Add the Python Server

Fill in the following details:

| Field | Value |
|-------|-------|
| **Name** | Dog MCP Server |
| **Type** | stdio |
| **Command** | `/Users/ravi/Work/repo/fastmcp-dog-python/venv/bin/python` |
| **Args** | `/Users/ravi/Work/repo/fastmcp-dog-python/src/server.py` |
| **Timeout** | 300 (seconds) |

### Step 3: Save and Restart

1. Click **Save** or **Add**
2. Restart Goose Desktop
3. The server should now be available

---

## Option 3: Direct Config File Edit (Advanced)

If the UI doesn't have MCP server management, you can edit the config file directly:

### Step 1: Open the Config File

```bash
nano ~/.config/goose/config.yaml
```

### Step 2: Add/Update the Server Entry

Look for the `dogmcpserver` section. It should look like this:

```yaml
dogmcpserver:
  enabled: true
  type: stdio
  name: Dog MCP Server
  description: 'Python MCP Server for fetching dog images'
  cmd: /Users/ravi/Work/repo/fastmcp-dog-python/venv/bin/python
  args:
  - /Users/ravi/Work/repo/fastmcp-dog-python/src/server.py
  envs: {}
  env_keys: []
  timeout: 300
  bundled: null
  available_tools: []
```

If it's already there, you're good! If not, add it exactly as shown.

### Step 3: Save and Restart

1. Save the file: `Ctrl+X`, then `Y`, then `Enter` (in nano)
2. Restart Goose Desktop
3. Done! ✅

---

## Verify It's Working

### In Goose Desktop:

1. Open a conversation
2. Try asking: "Get me a picture of a husky using the dogByBreed tool"
3. Goose should fetch the image using your Python MCP Server

### In Goose CLI (Terminal):

```bash
# The server should already work
goose
# Then ask: "Get me a random dog picture"
```

---

## Troubleshooting

### Server Not Showing Up

1. **Check the config file exists:**
   ```bash
   cat ~/.config/goose/config.yaml | grep -A 10 "dogmcpserver"
   ```

2. **Verify the paths are correct:**
   ```bash
   ls -la /Users/ravi/Work/repo/fastmcp-dog-python/venv/bin/python
   ls -la /Users/ravi/Work/repo/fastmcp-dog-python/src/server.py
   ```

3. **Check if the venv is active/valid:**
   ```bash
   cd /Users/ravi/Work/repo/fastmcp-dog-python
   source venv/bin/activate
   python -c "import fastmcp; print('✅ Dependencies OK')"
   ```

### Server Fails to Start

1. **Check for Python errors:**
   ```bash
   cd /Users/ravi/Work/repo/fastmcp-dog-python
   source venv/bin/activate
   python src/server.py
   ```
   (Press Ctrl+C to stop)

2. **Verify dependencies:**
   ```bash
   cd /Users/ravi/Work/repo/fastmcp-dog-python
   source venv/bin/activate
   pip list | grep -E "fastmcp|pydantic|httpx"
   ```

3. **Check Goose Desktop logs:**
   ```bash
   cat ~/.local/state/goose/logs/server/*mcp*.log | tail -50
   ```

---

## Configuration Locations

| App | Config Location |
|-----|-----------------|
| **Goose CLI** | `~/.config/goose/config.yaml` |
| **Goose Desktop** | Same as CLI (shared) or `~/Library/Application Support/Goose/` |
| **Logs** | `~/.local/state/goose/logs/` |

---

## Summary

**Most Likely:** Goose Desktop shares the same config as Goose CLI, so:

1. ✅ Your server is already configured
2. ✅ Just restart Goose Desktop
3. ✅ Start using the Dog MCP Server!

If that doesn't work, follow **Option 2** or **Option 3** above.

---

## Questions?

If you encounter any issues:
1. Check the troubleshooting section
2. Verify the paths match your system
3. Ensure the venv is properly set up
4. Check the logs for error messages

Good luck! 🐕
