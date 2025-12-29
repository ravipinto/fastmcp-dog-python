#!/usr/bin/env python3
"""
Test script for Dog MCP Server
Simulates MCP protocol communication to test server functionality
"""

import asyncio
import json
import sys
from src.server import server

async def test_tools():
    """Test that tools are registered and callable"""
    print("=" * 60)
    print("DOG MCP SERVER - TEST SUITE")
    print("=" * 60)
    
    # Test 1: List tools
    print("\n[TEST 1] Listing registered tools...")
    try:
        tools = await server.list_tools()
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
            print(f"     Input schema: {tool.inputSchema}")
    except Exception as e:
        print(f"❌ Error listing tools: {e}")
        return False
    
    # Test 2: Call randomDog
    print("\n[TEST 2] Calling randomDog tool...")
    try:
        result = await server.call_tool("randomDog", {})
        print(f"✅ randomDog returned {len(result)} content items:")
        for item in result:
            print(f"   - Type: {item.type}")
            if hasattr(item, 'text'):
                print(f"     Text: {item.text[:100]}...")
    except Exception as e:
        print(f"❌ Error calling randomDog: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Call dogByBreed with valid breed
    print("\n[TEST 3] Calling dogByBreed with 'poodle'...")
    try:
        result = await server.call_tool("dogByBreed", {"breed": "poodle"})
        print(f"✅ dogByBreed(poodle) returned {len(result)} content items:")
        for item in result:
            print(f"   - Type: {item.type}")
            if hasattr(item, 'text'):
                print(f"     Text: {item.text[:100]}...")
    except Exception as e:
        print(f"❌ Error calling dogByBreed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Call dogByBreed with invalid breed
    print("\n[TEST 4] Calling dogByBreed with invalid breed 'invalid_breed_xyz'...")
    try:
        result = await server.call_tool("dogByBreed", {"breed": "invalid_breed_xyz"})
        print(f"✅ dogByBreed(invalid_breed_xyz) returned {len(result)} content items:")
        for item in result:
            print(f"   - Type: {item.type}")
            if hasattr(item, 'text'):
                print(f"     Text: {item.text[:100]}...")
    except Exception as e:
        print(f"❌ Error calling dogByBreed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = asyncio.run(test_tools())
    sys.exit(0 if success else 1)
