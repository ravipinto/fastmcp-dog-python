import asyncio
import json
import urllib.parse
from typing import Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import httpx
from mcp.types import TextContent


# Create a new FastMCP server instance
server = FastMCP(
    name="Dog MCP Server",  # The name that Goose will display
)


# MCP-UI CODE

# Reusable mcp-ui interface
def dog_card_html(image_url: str, breed: Optional[str] = None) -> str:
    """Generate HTML card for dog image display"""
    safe_url = image_url.replace('"', '&quot;')
    title = f"Random {breed}" if breed else "Random Dog"
    tweet = urllib.parse.quote("I didn't write this… Goose did.")
    tweet_url = f"https://twitter.com/intent/tweet?text={tweet}&url={urllib.parse.quote(image_url)}"

    return f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8"/>
      <meta name="viewport" content="width=device-width,initial-scale=1"/>
      <title>{title}</title>
      <style>
        body {{ margin:0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI; background:#f6f7f9; }}
        .wrap {{ max-width: 720px; margin: 0 auto; padding: 16px; }}
        .card {{ background:#fff; border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,.07); overflow:hidden; }}
        .head {{ padding:16px 20px; border-bottom:1px solid #eee; display:flex; align-items:center; gap:8px; }}
        .head h1 {{ margin:0; font-size:16px; font-weight:600; }}
        .media {{ padding:16px; text-align:center; }}
        .media img {{ max-width:100%; border-radius:12px; display:block; margin:0 auto; }}
        .actions {{ padding:16px; display:flex; flex-wrap:wrap; gap:10px; }}
        .btn {{ padding:10px 14px; border:0; border-radius:999px; background:#111; color:#fff; cursor:pointer; }}
        .btn.secondary {{ background:#2563eb; }}
        .btn.ghost {{ background:#e5e7eb; color:#111; }}
      </style>
    </head>
    <body>
      <div class="wrap">
        <div class="card">
          <div class="head">
            <div>🐶</div>
            <h1>{title}</h1>
          </div>
          <div class="media">
            <img src="{safe_url}" alt="dog"/>
          </div>
          <div class="actions">
            <a class="btn" target="_blank" href="{safe_url}">🔗 View</a>
            <button class="btn ghost" onclick="navigator.clipboard.writeText('{safe_url}')">📋 Copy URL</button>
            <button class="btn secondary" onclick="makeMeme()">🧠 Meme caption</button>
            <button class="btn ghost" onclick="share()">↗️ Share</button>
          </div>
        </div>
      </div>

      <script>
        // Resize with content
        const ro = new ResizeObserver(es => {{
          for (const e of es) {{
            parent.postMessage({{ type: "ui-size-change", payload: {{ height: e.contentRect.height }} }}, "*");
          }}
        }});
        ro.observe(document.documentElement);

        // Ask Goose to write a caption (PROMPT action)
        function makeMeme() {{
          parent.postMessage({{
            type: "prompt",
            payload: {{
              prompt: "Write a short, funny meme caption for this dog photo: {safe_url}"
            }}
          }}, "*");
        }}

        // Open share link in a new tab (LINK action)
        function share() {{
          parent.postMessage({{
            type: "link",
            payload: {{ url: "{tweet_url}" }}
          }}, "*");
        }}
      </script>
    </body>
    </html>"""


# Define parameter models using Pydantic
class RandomDogParams(BaseModel):
    """No parameters needed for random dog"""
    pass


class DogByBreedParams(BaseModel):
    """Parameters for dog by breed"""
    breed: str = Field(..., description="The breed of the dog (e.g., 'husky', 'pug')")


# 🐕 Tool 1: Random dog
@server.tool(
    name="randomDog",
    description="Get a random dog image",
)
async def random_dog() -> list:
    """Fetch a random dog image from dog.ceo API"""
    async with httpx.AsyncClient() as client:
        res = await client.get("https://dog.ceo/api/breeds/image/random")
        data = res.json()
        image_url = data.get("message")

        return [
            TextContent(
                type="text",
                text=f"Here's a random dog:\n{image_url}"
            )
        ]


# 🐶 Tool 2: Dog by breed
@server.tool(
    name="dogByBreed",
    description="Get a random image of a specific dog breed",
)
async def dog_by_breed(breed: str) -> list:
    """Fetch a random dog image of a specific breed"""
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://dog.ceo/api/breed/{breed}/images/random")
        data = res.json()
        
        # Handle errors from the API
        if data.get("status") != "success":
            error_msg = data.get("message", "Unknown error")
            return [
                TextContent(
                    type="text",
                    text=f"Error: Could not find breed '{breed}'. {error_msg}\n\nTip: Try using common breed names like 'poodle', 'husky', 'golden retriever', 'labrador', etc."
                )
            ]
        
        image_url = data.get("message")

        return [
            TextContent(
                type="text",
                text=f"Here's a random {breed}:\n{image_url}"
            )
        ]


# Start the server so Goose can connect via stdio
if __name__ == "__main__":
    import sys
    import logging
    
    # Set up logging to stderr so we can see errors
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stderr)]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Dog MCP Server...")
    logger.info(f"Registered tools: randomDog, dogByBreed")
    
    try:
        server.run(transport="stdio")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
