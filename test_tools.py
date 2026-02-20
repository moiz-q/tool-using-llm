"""
Test suite for tools.
"""

import json
from tools import calculator, search_docs, web_fetch, execute_tool


def test_calculator():
    """Test calculator tool."""
    print("Testing Calculator...")
    
    # Test addition
    result = calculator("add", 5, 3)
    assert result["success"] == True
    assert result["result"] == 8
    print("  ✓ Addition: 5 + 3 = 8")
    
    # Test subtraction
    result = calculator("subtract", 10, 4)
    assert result["success"] == True
    assert result["result"] == 6
    print("  ✓ Subtraction: 10 - 4 = 6")
    
    # Test multiplication
    result = calculator("multiply", 7, 8)
    assert result["success"] == True
    assert result["result"] == 56
    print("  ✓ Multiplication: 7 * 8 = 56")
    
    # Test division
    result = calculator("divide", 20, 4)
    assert result["success"] == True
    assert result["result"] == 5.0
    print("  ✓ Division: 20 / 4 = 5.0")
    
    # Test divide by zero
    result = calculator("divide", 10, 0)
    assert result["success"] == False
    assert "divide by zero" in result["error"].lower()
    print("  ✓ Divide by zero handled")
    
    # Test invalid operation
    result = calculator("power", 2, 3)
    assert result["success"] == False
    print("  ✓ Invalid operation handled")
    
    print("Calculator tests passed!\n")


def test_search_docs():
    """Test document search tool."""
    print("Testing Search Documents...")
    
    # Test search with results
    result = search_docs("Python")
    assert result["success"] == True
    assert len(result["results"]) > 0
    print(f"  ✓ Found {len(result['results'])} documents for 'Python'")
    
    # Test search with no results
    result = search_docs("nonexistent_query_xyz")
    assert result["success"] == True
    assert len(result["results"]) == 0
    print("  ✓ No results for nonexistent query")
    
    # Test max_results parameter
    result = search_docs("Python", max_results=1)
    assert result["success"] == True
    assert len(result["results"]) <= 1
    print("  ✓ max_results parameter works")
    
    print("Search tests passed!\n")


def test_web_fetch():
    """Test web fetch tool."""
    print("Testing Web Fetch...")
    
    # Test fetching title
    result = web_fetch("python.org", "title")
    assert result["success"] == True
    assert "Python" in result["content"]
    print("  ✓ Fetched title from python.org")
    
    # Test fetching summary
    result = web_fetch("example.com", "summary")
    assert result["success"] == True
    print("  ✓ Fetched summary from example.com")
    
    # Test fetching content
    result = web_fetch("github.com", "content")
    assert result["success"] == True
    print("  ✓ Fetched content from github.com")
    
    # Test invalid URL
    result = web_fetch("invalid-url.xyz", "title")
    assert result["success"] == False
    print("  ✓ Invalid URL handled")
    
    # Test invalid extract type
    result = web_fetch("python.org", "invalid")
    assert result["success"] == False
    print("  ✓ Invalid extract type handled")
    
    print("Web fetch tests passed!\n")


def test_execute_tool():
    """Test tool execution wrapper."""
    print("Testing Tool Execution...")
    
    # Test valid tool call
    result = execute_tool("calculator", {"operation": "add", "a": 5, "b": 3})
    assert result["success"] == True
    assert result["result"] == 8
    print("  ✓ Valid tool call executed")
    
    # Test invalid tool name
    result = execute_tool("nonexistent_tool", {})
    assert result["success"] == False
    assert "not found" in result["error"].lower()
    print("  ✓ Invalid tool name handled")
    
    # Test invalid arguments
    result = execute_tool("calculator", {"operation": "add"})  # Missing a and b
    assert result["success"] == False
    print("  ✓ Invalid arguments handled")
    
    print("Tool execution tests passed!\n")


def run_all_tests():
    """Run all tests."""
    print("="*80)
    print("RUNNING TOOL TESTS")
    print("="*80)
    print()
    
    try:
        test_calculator()
        test_search_docs()
        test_web_fetch()
        test_execute_tool()
        
        print("="*80)
        print("ALL TESTS PASSED ✓")
        print("="*80)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        raise
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
