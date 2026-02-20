# Tool-Using LLM Examples

Real examples showing how the agent uses tools.

## Example 1: Simple Calculation

**Command:**
```bash
python tool_agent.py "What is 234 + 567?"
```

**Agent Trace:**
```
================================================================================
TOOL-USING AGENT
================================================================================

Question: What is 234 + 567?

--- Iteration 1 ---
LLM Response: {"tool": "calculator", "arguments": {"operation": "add", "a": 234, "b": 567}}

[Tool Call] calculator({"operation": "add", "a": 234, "b": 567})
[Tool Result] {
  "success": true,
  "result": 801,
  "operation": "add",
  "inputs": {"a": 234, "b": 567}
}

--- Iteration 2 ---
LLM Response: {"done": true, "answer": "The answer is 801"}

[Done] The answer is 801

================================================================================
FINAL ANSWER
================================================================================
The answer is 801
```

**Key Points:**
- LLM correctly identified need for calculator
- Extracted numbers from question
- Used tool result in final answer
- Didn't hallucinate the calculation

---

## Example 2: Document Search

**Command:**
```bash
python tool_agent.py "Search for information about machine learning"
```

**Agent Trace:**
```
================================================================================
TOOL-USING AGENT
================================================================================

Question: Search for information about machine learning

--- Iteration 1 ---
LLM Response: {"tool": "search_docs", "arguments": {"query": "machine learning", "max_results": 3}}

[Tool Call] search_docs({"query": "machine learning", "max_results": 3})
[Tool Result] {
  "success": true,
  "results": [
    {
      "filename": "machine_learning.txt",
      "snippet": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience...",
      "relevance": 3
    }
  ],
  "query": "machine learning",
  "count": 1
}

--- Iteration 2 ---
LLM Response: {"done": true, "answer": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. There are three main types: supervised learning, unsupervised learning, and reinforcement learning."}

[Done] Machine learning is a subset of artificial intelligence...

================================================================================
FINAL ANSWER
================================================================================
Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. There are three main types: supervised learning, unsupervised learning, and reinforcement learning.
```

**Key Points:**
- LLM used search_docs tool
- Extracted relevant information from results
- Synthesized answer from search results

---

## Example 3: Multi-Step Task

**Command:**
```bash
python tool_agent.py "Calculate 10 * 5, then search for that number"
```

**Agent Trace:**
```
================================================================================
TOOL-USING AGENT
================================================================================

Question: Calculate 10 * 5, then search for that number

--- Iteration 1 ---
LLM Response: {"tool": "calculator", "arguments": {"operation": "multiply", "a": 10, "b": 5}}

[Tool Call] calculator({"operation": "multiply", "a": 10, "b": 5})
[Tool Result] {
  "success": true,
  "result": 50
}

--- Iteration 2 ---
LLM Response: {"tool": "search_docs", "arguments": {"query": "50", "max_results": 3}}

[Tool Call] search_docs({"query": "50", "max_results": 3})
[Tool Result] {
  "success": true,
  "results": [],
  "message": "No documents found matching '50'"
}

--- Iteration 3 ---
LLM Response: {"done": true, "answer": "10 * 5 = 50. I searched for '50' in the documents but found no matches."}

[Done] 10 * 5 = 50. I searched for '50' in the documents but found no matches.

================================================================================
FINAL ANSWER
================================================================================
10 * 5 = 50. I searched for '50' in the documents but found no matches.
```

**Key Points:**
- LLM broke task into two steps
- Used calculator result as input to search
- Handled "no results" gracefully

---

## Example 4: Error Handling (Divide by Zero)

**Command:**
```bash
python tool_agent.py "What is 10 divided by 0?"
```

**Agent Trace:**
```
================================================================================
TOOL-USING AGENT
================================================================================

Question: What is 10 divided by 0?

--- Iteration 1 ---
LLM Response: {"tool": "calculator", "arguments": {"operation": "divide", "a": 10, "b": 0}}

[Tool Call] calculator({"operation": "divide", "a": 10, "b": 0})
[Tool Result] {
  "success": false,
  "error": "Cannot divide by zero"
}

--- Iteration 2 ---
LLM Response: {"done": true, "answer": "I cannot divide 10 by 0 because division by zero is undefined in mathematics."}

[Done] I cannot divide 10 by 0 because division by zero is undefined in mathematics.

================================================================================
FINAL ANSWER
================================================================================
I cannot divide 10 by 0 because division by zero is undefined in mathematics.
```

**Key Points:**
- Tool returned error instead of crashing
- LLM understood error and explained it
- Graceful error handling

---

## Example 5: Web Fetch

**Command:**
```bash
python tool_agent.py "What is the title of python.org?"
```

**Agent Trace:**
```
================================================================================
TOOL-USING AGENT
================================================================================

Question: What is the title of python.org?

--- Iteration 1 ---
LLM Response: {"tool": "web_fetch", "arguments": {"url": "python.org", "extract": "title"}}

[Tool Call] web_fetch({"url": "python.org", "extract": "title"})
[Tool Result] {
  "success": true,
  "url": "python.org",
  "extract_type": "title",
  "content": "Welcome to Python.org"
}

--- Iteration 2 ---
LLM Response: {"done": true, "answer": "The title of python.org is 'Welcome to Python.org'"}

[Done] The title of python.org is 'Welcome to Python.org'

================================================================================
FINAL ANSWER
================================================================================
The title of python.org is 'Welcome to Python.org'
```

**Key Points:**
- LLM chose correct tool (web_fetch)
- Specified correct extract type (title)
- Used tool result in answer

---

## Example 6: Tool Refusal

**Command:**
```bash
python tool_agent.py "Use the calculator to write a poem"
```

**Agent Trace:**
```
================================================================================
TOOL-USING AGENT
================================================================================

Question: Use the calculator to write a poem

--- Iteration 1 ---
LLM Response: {"refuse": true, "reason": "The calculator tool is designed for arithmetic operations, not for creative writing tasks like writing poems."}

[Refused] The calculator tool is designed for arithmetic operations, not for creative writing tasks like writing poems.

================================================================================
FINAL ANSWER
================================================================================
I cannot complete this task: The calculator tool is designed for arithmetic operations, not for creative writing tasks like writing poems.
```

**Key Points:**
- LLM recognized inappropriate tool use
- Refused instead of trying to force it
- Explained why refusal was appropriate

---

## Example 7: Complex Multi-Step

**Command:**
```bash
python tool_agent.py "Calculate 15 + 30, then multiply that result by 2, then search for the final number"
```

**Agent Trace:**
```
================================================================================
TOOL-USING AGENT
================================================================================

Question: Calculate 15 + 30, then multiply that result by 2, then search for the final number

--- Iteration 1 ---
[Tool Call] calculator({"operation": "add", "a": 15, "b": 30})
[Tool Result] {"success": true, "result": 45}

--- Iteration 2 ---
[Tool Call] calculator({"operation": "multiply", "a": 45, "b": 2})
[Tool Result] {"success": true, "result": 90}

--- Iteration 3 ---
[Tool Call] search_docs({"query": "90", "max_results": 3})
[Tool Result] {"success": true, "results": [], "message": "No documents found matching '90'"}

--- Iteration 4 ---
[Done] First, 15 + 30 = 45. Then, 45 * 2 = 90. I searched for '90' but found no matching documents.

================================================================================
FINAL ANSWER
================================================================================
First, 15 + 30 = 45. Then, 45 * 2 = 90. I searched for '90' but found no matching documents.
```

**Key Points:**
- LLM planned multi-step execution
- Used intermediate results correctly
- Completed all steps in sequence

---

## Example 8: Invalid Tool Arguments

**Command:**
```bash
python tool_agent.py "Calculate the square root of 16"
```

**Agent Trace:**
```
================================================================================
TOOL-USING AGENT
================================================================================

Question: Calculate the square root of 16

--- Iteration 1 ---
LLM Response: {"refuse": true, "reason": "The calculator tool only supports add, subtract, multiply, and divide operations. It cannot calculate square roots."}

[Refused] The calculator tool only supports add, subtract, multiply, and divide operations. It cannot calculate square roots.

================================================================================
FINAL ANSWER
================================================================================
I cannot complete this task: The calculator tool only supports add, subtract, multiply, and divide operations. It cannot calculate square roots.
```

**Key Points:**
- LLM recognized tool limitations
- Refused instead of trying invalid operation
- Could suggest alternative if tool existed

---

## Testing These Examples

Run all examples:
```bash
# Simple
python tool_agent.py "What is 234 + 567?"

# Search
python tool_agent.py "Search for information about machine learning"

# Multi-step
python tool_agent.py "Calculate 10 * 5, then search for that number"

# Error handling
python tool_agent.py "What is 10 divided by 0?"

# Web fetch
python tool_agent.py "What is the title of python.org?"

# Refusal
python tool_agent.py "Use the calculator to write a poem"

# Complex
python tool_agent.py "Calculate 15 + 30, then multiply that result by 2"
```

## Key Takeaways

1. **LLM decides which tool** - Not hardcoded logic
2. **JSON enforcement prevents hallucination** - Must call tools, can't fake results
3. **Error handling is graceful** - Tools return errors, LLM explains them
4. **Multi-step works** - LLM can chain tool calls
5. **Refusal is smart** - LLM knows tool limitations
6. **Results are real** - No hallucinated calculations or data
