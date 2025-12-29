# Dog MCP Server - Python Edition

A Python port of the FastMCP Dog Server. This server provides tools to fetch and display random dog images using the [dog.ceo API](https://dog.ceo).

## Features

- **Random Dog Tool** (`randomDog`) - Get a random dog image from any breed
- **Breed-Specific Tool** (`dogByBreed`) - Get a random dog image of a specific breed
- **Interactive UI** - Rich HTML cards with copy, share, and meme caption functionality
- **MCP Protocol** - Communicates with Goose and other MCP clients via stdio

## Project Structure

```
fastmcp-dog-python/
├── src/
│   └── server.py          # Main FastMCP server implementation
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Setup

### 1. Create a Virtual Environment

```bash
cd /Users/ravi/Work/repo/fastmcp-dog-python
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
python src/server.py
```

The server will start listening on stdio and be ready to receive requests from Goose.

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `fastmcp` | 0.1.0 | MCP protocol implementation |
| `pydantic` | 2.5.0 | Data validation using Python type hints |
| `httpx` | 0.25.1 | Async HTTP client for API calls |

## Tools

### 1. Random Dog

**Name:** `randomDog`

**Description:** Get a random dog image

**Parameters:** None

**Returns:** Random dog image URL with interactive HTML card UI

**Example:**
```python
# Called as: randomDog()
# Returns: Image URL + Interactive card with view, copy, share buttons
```

### 2. Dog by Breed

**Name:** `dogByBreed`

**Description:** Get a random image of a specific dog breed

**Parameters:**
- `breed` (string, required) - The breed of the dog (e.g., 'husky', 'pug')

**Returns:** Breed-specific dog image URL with interactive HTML card UI

**Example:**
```python
# Called as: dogByBreed(breed="husky")
# Returns: Random husky image + Interactive card
```

## UI Features

The interactive HTML card includes:

- 🐶 Dog image display
- 🔗 **View** - Open image in new tab
- 📋 **Copy URL** - Copy image URL to clipboard
- 🧠 **Meme Caption** - Ask Goose to write a funny caption
- ↗️ **Share** - Share on Twitter with a pre-filled message

## API Integration

This server uses the free [dog.ceo API](https://dog.ceo):

- **Random Dog:** `GET https://dog.ceo/api/breeds/image/random`
- **By Breed:** `GET https://dog.ceo/api/breed/{breed}/images/random`

## Differences from TypeScript Version

| Aspect | TypeScript | Python |
|--------|-----------|--------|
| HTTP Client | `node-fetch` | `httpx` (async) |
| Validation | `zod` | `pydantic` |
| Async/Await | JavaScript-style | Python-style |
| Server Start | `server.start()` | `server.run()` |
| Tool Decoration | Object method pattern | `@server.tool()` decorator |

## Python-Specific Notes

- Uses `async/await` for all I/O operations
- Pydantic models provide type safety and validation
- F-strings with double braces `{{}}` escape JavaScript code in HTML templates
- `urllib.parse.quote()` for URL encoding instead of JavaScript's `encodeURIComponent()`

## License

Same as parent project

## Related

- [FastMCP Boilerplate (TypeScript)](../fastmcp-boilerplate) - Original TypeScript version
- [dog.ceo API](https://dog.ceo/api) - Dog image API
- [FastMCP](https://github.com/block/fastmcp) - Model Context Protocol implementation
