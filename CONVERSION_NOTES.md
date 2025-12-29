# TypeScript to Python Conversion Notes

## Overview

This document details the conversion from the TypeScript FastMCP Dog Server to Python.

## Project Structure

```
/Users/ravi/Work/repo/
├── fastmcp-boilerplate/          # Original TypeScript project
│   ├── src/
│   │   ├── server.ts
│   │   └── types/
│   ├── package.json
│   └── tsconfig.json
│
└── fastmcp-dog-python/           # Python port (NEW)
    ├── src/
    │   ├── __init__.py
    │   └── server.py
    ├── requirements.txt
    ├── pyproject.toml
    ├── README.md
    ├── .gitignore
    ├── setup.sh
    └── CONVERSION_NOTES.md
```

## Key Conversions

### 1. Module System

**TypeScript:**
```typescript
import { FastMCP } from "fastmcp";
import { z } from "zod";
import fetch from "node-fetch";
```

**Python:**
```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import httpx
```

### 2. Server Initialization

**TypeScript:**
```typescript
const server = new FastMCP({
  name: "Dog MCP Server",
  version: "1.0.0",
});
```

**Python:**
```python
server = FastMCP(
    name="Dog MCP Server",
    version="1.0.0",
)
```

### 3. Tool Definition

**TypeScript (Object-based):**
```typescript
server.addTool({
  name: "randomDog",
  description: "Get a random dog image",
  parameters: z.object({}),
  execute: async () => {
    const res = await fetch("https://dog.ceo/api/breeds/image/random");
    const json = (await res.json()) as { message: string };
    return json.message;
  }
});
```

**Python (Decorator-based):**
```python
@server.tool(
    name="randomDog",
    description="Get a random dog image",
)
async def random_dog() -> dict:
    """Fetch a random dog image from dog.ceo API"""
    async with httpx.AsyncClient() as client:
        res = await client.get("https://dog.ceo/api/breeds/image/random")
        data = res.json()
        image_url = data.get("message")
        return {"content": [...]}
```

### 4. Parameter Validation

**TypeScript (Zod):**
```typescript
parameters: z.object({
  breed: z.string().describe("The breed of the dog (e.g., 'husky', 'pug')"),
}),
```

**Python (Pydantic):**
```python
class DogByBreedParams(BaseModel):
    breed: str = Field(..., description="The breed of the dog (e.g., 'husky', 'pug')")
```

### 5. HTTP Requests

**TypeScript (node-fetch - synchronous style):**
```typescript
const res = await fetch("https://dog.ceo/api/breeds/image/random");
const json = (await res.json()) as { message: string };
```

**Python (httpx - async client):**
```python
async with httpx.AsyncClient() as client:
    res = await client.get("https://dog.ceo/api/breeds/image/random")
    data = res.json()
```

### 6. HTML Template Generation

**TypeScript (Template literals):**
```typescript
return `
  <!doctype html>
  <html>
  <head>
    <style>
      body { margin:0; ... }
    </style>
  </head>
  ...
`;
```

**Python (F-strings with double braces for JavaScript):**
```python
return f"""
  <!doctype html>
  <html>
  <head>
    <style>
      body {{ margin:0; ... }}
    </style>
  </head>
  ...
"""
```

**Note:** Python uses `{{` and `}}` to escape braces in f-strings, preventing them from being interpreted as template variables.

### 7. URL Encoding

**TypeScript:**
```typescript
const tweet = encodeURIComponent(`I didn't write this… Goose did.`);
const tweetUrl = `https://twitter.com/intent/tweet?text=${tweet}&url=${encodeURIComponent(imageUrl)}`;
```

**Python:**
```python
tweet = urllib.parse.quote("I didn't write this… Goose did.")
tweet_url = f"https://twitter.com/intent/tweet?text={tweet}&url={urllib.parse.quote(image_url)}"
```

### 8. Server Startup

**TypeScript:**
```typescript
server.start({
  transportType: "stdio",
});
```

**Python:**
```python
if __name__ == "__main__":
    server.run(transport="stdio")
```

## Dependencies Mapping

| Purpose | TypeScript | Python |
|---------|-----------|--------|
| MCP Protocol | fastmcp | fastmcp |
| Input Validation | zod | pydantic |
| HTTP Requests | node-fetch | httpx |
| Runtime | Node.js | Python 3.8+ |

## Code Quality Improvements in Python Version

1. **Type Hints**: Full type annotations for better IDE support and error detection
2. **Docstrings**: Comprehensive docstrings for all functions
3. **Project Metadata**: `pyproject.toml` for modern Python packaging
4. **Setup Script**: `setup.sh` for automated environment setup
5. **Git Initialization**: Proper `.git` repo with meaningful initial commit
6. **Documentation**: Detailed README with all setup instructions

## Running the Server

### TypeScript Version
```bash
cd /Users/ravi/Work/repo/fastmcp-boilerplate
npm install
npm run dev  # or node built-in script
```

### Python Version
```bash
cd /Users/ravi/Work/repo/fastmcp-dog-python
chmod +x setup.sh
./setup.sh
source venv/bin/activate
python src/server.py
```

## Testing Equivalence

Both versions:
- ✅ Implement the same two tools (randomDog, dogByBreed)
- ✅ Call the same dog.ceo API endpoints
- ✅ Return identical HTML UI cards
- ✅ Support interactive features (copy, share, meme caption)
- ✅ Use stdio transport for MCP communication

## Python-Specific Considerations

1. **Async/Await Pattern**: Python's `async def` and `await` are more explicit than TypeScript
2. **Context Managers**: Using `async with` for proper resource cleanup
3. **F-string Escaping**: Double braces needed in f-strings for JavaScript code
4. **Import Statements**: More explicit imports compared to TypeScript's export patterns
5. **Virtual Environments**: Required for isolated Python development (not needed with Node.js/npm)

## Future Enhancements

- [ ] Add error handling for API failures
- [ ] Implement caching for frequently requested breeds
- [ ] Add logging configuration
- [ ] Create unit tests with pytest
- [ ] Add type checking with mypy
- [ ] Create Docker support
- [ ] Add CLI argument parsing

## Notes

- Both versions maintain 100% feature parity
- The Python version uses modern async patterns
- Pydantic provides better type safety than zod in some cases
- The project structure follows Python best practices
- All dependencies are pinned to specific versions for reproducibility

## References

- [FastMCP Documentation](https://github.com/block/fastmcp)
- [dog.ceo API](https://dog.ceo/api)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [httpx Documentation](https://www.python-httpx.org/)
