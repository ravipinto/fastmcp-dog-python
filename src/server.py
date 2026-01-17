import os
import sys
import argparse
import logging
import re
from typing import Optional

import httpx
from fastmcp import FastMCP

# Security constants
HTTP_TIMEOUT = 10.0  # seconds
BREED_PATTERN = re.compile(r'^[a-z]+(/[a-z]+)?$', re.IGNORECASE)


# Create a new FastMCP server instance
server = FastMCP(
    name="Dog MCP Server",  # The name clients will display
)


@server.tool(
    name="randomDog",
    description="Get a random dog image",
)
async def random_dog() -> str:
    """Fetch a random dog image from dog.ceo API."""
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        res = await client.get("https://dog.ceo/api/breeds/image/random")
        data = res.json()
        image_url = data.get("message")
        return f"Here's a random dog:\n{image_url}"


@server.tool(
    name="dogByBreed",
    description="Get a random image of a specific dog breed",
)
async def dog_by_breed(breed: str) -> str:
    """Fetch a random dog image of a specific breed."""
    # Input validation: only allow lowercase letters and single forward slash for sub-breeds
    breed_clean = breed.strip().lower()
    if not breed_clean or not BREED_PATTERN.match(breed_clean):
        return (
            "Error: Invalid breed name format. "
            "Breed names should only contain letters (e.g., 'poodle', 'husky', 'hound/basset')."
        )

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        res = await client.get(f"https://dog.ceo/api/breed/{breed_clean}/images/random")
        data = res.json()

        # Handle errors from the API
        if data.get("status") != "success":
            return (
                f"Error: Could not find breed '{breed_clean}'.\n\n"
                "Tip: Try using common breed names like 'poodle', 'husky', 'labrador', or sub-breeds like 'hound/basset'."
            )

        image_url = data.get("message")
        return f"Here's a random {breed_clean}:\n{image_url}"


# Start the server so clients can connect (dual transport)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Dog MCP Server with different transports")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default=os.environ.get("FASTMCP_TRANSPORT", os.environ.get("MCP_TRANSPORT", "stdio")),
        help="Transport to use: stdio (default), http (streamable HTTP), or sse (legacy)",
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("FASTMCP_HOST", "127.0.0.1"),
        help="Host to bind for HTTP/SSE transports (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("FASTMCP_PORT", "8000")),
        help="Port to bind for HTTP/SSE transports (default: 8000)",
    )
    parser.add_argument(
        "--stateless-http",
        action="store_true",
        default=os.environ.get("FASTMCP_STATELESS_HTTP", "").lower() in {"1", "true", "yes"},
        help="Enable stateless mode for Streamable HTTP (useful for multi-worker/load-balanced setups)",
    )

    args = parser.parse_args()

    # Logging to stderr so STDIO stays clean
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )

    logger = logging.getLogger(__name__)
    logger.info("Starting Dog MCP Server...")
    logger.info("Registered tools: randomDog, dogByBreed")
    logger.info(
        f"Args: transport={args.transport} host={args.host} port={args.port} stateless_http={args.stateless_http}"
    )

    try:
        if args.transport == "stdio":
            logger.info("Transport: stdio")
            server.run(transport="stdio")
        elif args.transport == "http":
            # Streamable HTTP (recommended for network clients, including ChatGPT Developer Mode)
            logger.info(f"Transport: http (streamable) on http://{args.host}:{args.port}/mcp")
            server.run(
                transport="http",
                host=args.host,
                port=args.port,
                stateless_http=args.stateless_http,
            )
        else:  # sse
            # SSE is legacy; prefer Streamable HTTP unless you have an older client.
            logger.info(f"Transport: sse (legacy) on http://{args.host}:{args.port}/sse")
            server.run(
                transport="sse",
                host=args.host,
                port=args.port,
            )
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
