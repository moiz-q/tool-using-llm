"""
Tool implementations for the agent.
"""

import json
import os
from typing import Dict, Any, List


def calculator(operation: str, a: float, b: float) -> Dict[str, Any]:
    """
    Perform basic arithmetic operations.
    
    Args:
        operation: One of "add", "subtract", "multiply", "divide"
        a: First number
        b: Second number
    
    Returns:
        Dict with result or error
    """
    try:
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return {
                    "success": False,
                    "error": "Cannot divide by zero"
                }
            result = a / b
        else:
            return {
                "success": False,
                "error": f"Unknown operation: {operation}"
            }
        
        return {
            "success": True,
            "result": result,
            "operation": operation,
            "inputs": {"a": a, "b": b}
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def search_docs(query: str, max_results: int = 3) -> Dict[str, Any]:
    """
    Search through local documents.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        Dict with search results or error
    """
    try:
        docs_dir = "docs"
        
        # Create docs directory if it doesn't exist
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)
            # Create sample documents
            _create_sample_docs(docs_dir)
        
        # Simple keyword search
        results = []
        query_lower = query.lower()
        
        for filename in os.listdir(docs_dir):
            if filename.endswith(('.txt', '.md')):
                filepath = os.path.join(docs_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Check if query appears in content
                    if query_lower in content.lower():
                        # Get snippet around match
                        idx = content.lower().find(query_lower)
                        start = max(0, idx - 50)
                        end = min(len(content), idx + 150)
                        snippet = content[start:end].strip()
                        
                        results.append({
                            "filename": filename,
                            "snippet": snippet,
                            "relevance": content.lower().count(query_lower)
                        })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance'], reverse=True)
        results = results[:max_results]
        
        if not results:
            return {
                "success": True,
                "results": [],
                "message": f"No documents found matching '{query}'"
            }
        
        return {
            "success": True,
            "results": results,
            "query": query,
            "count": len(results)
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def web_fetch(url: str, extract: str = "content") -> Dict[str, Any]:
    """
    Simulate fetching web content (mocked for learning).
    
    Args:
        url: URL to fetch
        extract: What to extract ("title", "summary", "content")
    
    Returns:
        Dict with fetched content or error
    """
    try:
        # Mocked responses for common URLs
        mock_data = {
            "example.com": {
                "title": "Example Domain",
                "summary": "This domain is for use in illustrative examples in documents.",
                "content": "Example Domain. This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission."
            },
            "python.org": {
                "title": "Welcome to Python.org",
                "summary": "The official home of the Python Programming Language.",
                "content": "Python is a programming language that lets you work quickly and integrate systems more effectively. Python is powerful and fast, plays well with others, runs everywhere, is friendly and easy to learn, and is Open."
            },
            "github.com": {
                "title": "GitHub: Let's build from here",
                "summary": "GitHub is where over 100 million developers shape the future of software.",
                "content": "GitHub is where over 100 million developers shape the future of software, together. Contribute to the open source community, manage your Git repositories, review code like a pro, track bugs and features, power your CI/CD and DevOps workflows, and secure code before you commit it."
            }
        }
        
        # Normalize URL
        url_clean = url.replace("http://", "").replace("https://", "").replace("www.", "").strip("/")
        
        # Check if we have mock data
        if url_clean in mock_data:
            data = mock_data[url_clean]
            
            if extract == "title":
                result = data["title"]
            elif extract == "summary":
                result = data["summary"]
            elif extract == "content":
                result = data["content"]
            else:
                return {
                    "success": False,
                    "error": f"Unknown extract type: {extract}. Use 'title', 'summary', or 'content'."
                }
            
            return {
                "success": True,
                "url": url,
                "extract_type": extract,
                "content": result
            }
        else:
            return {
                "success": False,
                "error": f"URL not found in mock data. Available: {', '.join(mock_data.keys())}"
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def _create_sample_docs(docs_dir: str):
    """Create sample documents for search testing."""
    
    docs = {
        "python_intro.txt": """Python Programming Language

Python is a high-level, interpreted programming language known for its simplicity and readability. 
It was created by Guido van Rossum and first released in 1991.

Python is widely used in web development, data science, artificial intelligence, automation, and more.
Its extensive standard library and vast ecosystem of third-party packages make it suitable for almost any programming task.

Key features of Python include dynamic typing, automatic memory management, and support for multiple programming paradigms.""",
        
        "machine_learning.txt": """Machine Learning Basics

Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.

There are three main types of machine learning:
1. Supervised Learning - Learning from labeled data
2. Unsupervised Learning - Finding patterns in unlabeled data
3. Reinforcement Learning - Learning through trial and error

Popular machine learning frameworks include TensorFlow, PyTorch, and scikit-learn.""",
        
        "web_development.txt": """Web Development Overview

Web development involves building websites and web applications. It typically consists of two main areas:

Frontend Development: The client-side of web applications, dealing with what users see and interact with. Technologies include HTML, CSS, and JavaScript.

Backend Development: The server-side of web applications, handling data storage, business logic, and server configuration. Common languages include Python, JavaScript (Node.js), Java, and Ruby.

Modern web development often uses frameworks like React, Vue.js, Django, and Express.js to speed up development."""
    }
    
    for filename, content in docs.items():
        filepath = os.path.join(docs_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)


# Tool registry
TOOLS = {
    "calculator": {
        "function": calculator,
        "description": "Performs basic arithmetic operations (add, subtract, multiply, divide)",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The arithmetic operation to perform"
                },
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["operation", "a", "b"]
        }
    },
    "search_docs": {
        "function": search_docs,
        "description": "Search through local documents for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 3)",
                    "default": 3
                }
            },
            "required": ["query"]
        }
    },
    "web_fetch": {
        "function": web_fetch,
        "description": "Fetch content from a URL (mocked for learning)",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to fetch (example.com, python.org, github.com)"
                },
                "extract": {
                    "type": "string",
                    "enum": ["title", "summary", "content"],
                    "description": "What to extract from the page (default: content)",
                    "default": "content"
                }
            },
            "required": ["url"]
        }
    }
}


def get_tool_schemas() -> List[Dict[str, Any]]:
    """
    Get schemas for all available tools.
    
    Returns:
        List of tool schemas (without function implementations)
    """
    schemas = []
    for name, tool in TOOLS.items():
        schemas.append({
            "name": name,
            "description": tool["description"],
            "parameters": tool["parameters"]
        })
    return schemas


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool with given arguments.
    
    Args:
        tool_name: Name of the tool to execute
        arguments: Tool arguments
    
    Returns:
        Tool execution result
    """
    if tool_name not in TOOLS:
        return {
            "success": False,
            "error": f"Tool '{tool_name}' not found. Available tools: {', '.join(TOOLS.keys())}"
        }
    
    tool = TOOLS[tool_name]
    
    try:
        # Execute tool function
        result = tool["function"](**arguments)
        return result
    
    except TypeError as e:
        return {
            "success": False,
            "error": f"Invalid arguments for tool '{tool_name}': {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Tool execution failed: {str(e)}"
        }


if __name__ == "__main__":
    print("Testing tools...\n")
    
    # Test calculator
    print("1. Calculator:")
    print(json.dumps(calculator("add", 5, 3), indent=2))
    print(json.dumps(calculator("multiply", 7, 8), indent=2))
    print(json.dumps(calculator("divide", 10, 0), indent=2))
    
    # Test search
    print("\n2. Search Documents:")
    print(json.dumps(search_docs("Python"), indent=2))
    
    # Test web fetch
    print("\n3. Web Fetch:")
    print(json.dumps(web_fetch("python.org", "title"), indent=2))
