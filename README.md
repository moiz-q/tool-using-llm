# Tool-Using LLM

Goal: Teach LLMs to use tools reliably without hallucinating outputs.

Learn how to give LLMs access to external tools (functions) and ensure they use them correctly. This is the foundation for AI agents, function calling, and tool-augmented generation.

**Uses Ollama** - completely free, runs locally!

## What is Tool Use?

LLMs can't access real-time data, perform calculations, or interact with external systems. Tool use solves this by:

1. **Defining tools** - Functions the LLM can call (search, calculate, fetch data)
2. **LLM decides** - Which tool to use and with what arguments
3. **Execute tool** - Run the actual function
4. **Return result** - Give output back to LLM
5. **LLM responds** - Generate final answer using tool results

**The key challenge:** LLMs love to hallucinate tool outputs instead of actually calling them!

## Setup

1. **Install Ollama** (if you haven't already)
   - Download from: https://ollama.com/download

2. **Pull required model**
   ```bash
   ollama pull llama3.2
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

```bash
# 1. Test individual tools
python tools.py

# 2. Basic tool calling (LLM decides which tool)
python tool_agent.py "What is 25 * 47?"
python tool_agent.py "Search for information about Python"

# 3. Multi-step tool use
python tool_agent.py "Calculate 15 + 30, then search for that number"

# 4. Test error handling
python tool_agent.py "Divide 10 by 0"
```

## Project Structure

```
tool-using-llm/
├── tools.py              # Tool definitions and implementations
├── tool_schemas.py       # JSON schemas for tools
├── tool_agent.py         # Agent that uses tools
├── llm.py               # LLM interface (from repo 1)
├── test_tools.py        # Test suite for tools
├── docs/                # Sample documents for search
└── README.md
```

## Core Concepts

### 1. Tool Definition

A tool is a function with:
- **Name**: Identifier (e.g., "calculator")
- **Description**: What it does
- **Parameters**: JSON schema defining inputs
- **Implementation**: The actual Python function

**Example:**
```python
{
    "name": "calculator",
    "description": "Performs basic arithmetic operations",
    "parameters": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"]
            },
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["operation", "a", "b"]
    }
}
```

### 2. Tool Calling Flow

```
User: "What is 25 * 47?"
    ↓
LLM: "I need to use calculator tool"
    → Tool call: calculator(operation="multiply", a=25, b=47)
    ↓
Execute: 25 * 47 = 1175
    ↓
LLM: "The answer is 1175"
    ↓
User gets: "1175"
```

### 3. The Hallucination Problem

**Without proper control:**
```
User: "What is 25 * 47?"
LLM: "The answer is 1175" ← Hallucinated! Didn't actually calculate
```

**With tool enforcement:**
```
User: "What is 25 * 47?"
LLM: Must call calculator tool
System: Executes calculator(multiply, 25, 47) = 1175
LLM: "The answer is 1175" ← Verified!
```

## Available Tools

### 1. Calculator

**Purpose:** Perform arithmetic operations

**Operations:**
- add: a + b
- subtract: a - b
- multiply: a * b
- divide: a / b (with zero-division handling)

**Example:**
```bash
python tool_agent.py "What is 156 divided by 12?"
```

**Schema:**
```json
{
    "operation": "divide",
    "a": 156,
    "b": 12
}
```

### 2. Search Documents

**Purpose:** Search through local documents

**Parameters:**
- query: Search query string
- max_results: Number of results (default: 3)

**Example:**
```bash
python tool_agent.py "Search for information about machine learning"
```

**Schema:**
```json
{
    "query": "machine learning",
    "max_results": 3
}
```

### 3. Web Fetch (Mocked)

**Purpose:** Simulate fetching web content

**Parameters:**
- url: URL to fetch
- extract: What to extract (title, summary, content)

**Example:**
```bash
python tool_agent.py "Fetch the title from example.com"
```

**Schema:**
```json
{
    "url": "example.com",
    "extract": "title"
}
```

**Note:** This is mocked for learning purposes. Real implementation would use requests library.

## Tool Agent Architecture

### Components

**1. Tool Registry**
- Stores available tools
- Provides tool schemas to LLM
- Validates tool calls

**2. Tool Executor**
- Executes tool functions
- Handles errors gracefully
- Returns structured results

**3. Agent Loop**
- Sends prompt + tool schemas to LLM
- Parses LLM response for tool calls
- Executes tools
- Feeds results back to LLM
- Repeats until LLM says "done"

### Control Mechanisms

**1. JSON Schema Enforcement**
```python
# LLM must return valid JSON matching schema
{
    "tool": "calculator",
    "arguments": {
        "operation": "multiply",
        "a": 25,
        "b": 47
    }
}
```

**2. Max Tool Calls**
```python
# Prevent infinite loops
MAX_TOOL_CALLS = 5

if tool_call_count >= MAX_TOOL_CALLS:
    return "Maximum tool calls reached"
```

**3. Tool Validation**
```python
# Verify tool exists and arguments are valid
if tool_name not in available_tools:
    return "Tool not found"

if not validate_arguments(tool_schema, arguments):
    return "Invalid arguments"
```

## How It Works

### Step 1: Define Tools

```python
tools = [
    {
        "name": "calculator",
        "description": "Performs arithmetic",
        "parameters": {...},
        "function": calculator_impl
    }
]
```

### Step 2: Create Prompt with Tool Schemas

```python
prompt = f"""You have access to these tools:
{json.dumps(tool_schemas, indent=2)}

User question: {question}

To use a tool, respond with JSON:
{{"tool": "tool_name", "arguments": {{...}}}}

When done, respond with:
{{"done": true, "answer": "your final answer"}}
"""
```

### Step 3: Agent Loop

```python
while not done and tool_calls < MAX_CALLS:
    # Get LLM response
    response = call_llm(prompt)
    
    # Parse response
    parsed = parse_tool_call(response)
    
    if parsed.get("done"):
        return parsed["answer"]
    
    # Execute tool
    result = execute_tool(parsed["tool"], parsed["arguments"])
    
    # Add result to conversation
    prompt += f"\nTool result: {result}\n"
    tool_calls += 1
```

### Step 4: Return Final Answer

```python
# LLM uses tool results to generate answer
return final_answer
```

## Examples

### Example 1: Simple Calculation

**Input:**
```bash
python tool_agent.py "What is 234 + 567?"
```

**Agent trace:**
```
[Agent] Analyzing question...
[Tool Call] calculator(operation="add", a=234, b=567)
[Tool Result] 801
[Agent] The answer is 801
```

### Example 2: Multi-Step

**Input:**
```bash
python tool_agent.py "Calculate 10 * 5, then search for that number"
```

**Agent trace:**
```
[Agent] Step 1: Calculate 10 * 5
[Tool Call] calculator(operation="multiply", a=10, b=5)
[Tool Result] 50

[Agent] Step 2: Search for 50
[Tool Call] search_docs(query="50", max_results=3)
[Tool Result] Found 2 documents...

[Agent] Final answer: 10 * 5 = 50. Search results: ...
```

### Example 3: Error Handling

**Input:**
```bash
python tool_agent.py "Divide 10 by 0"
```

**Agent trace:**
```
[Agent] Attempting division...
[Tool Call] calculator(operation="divide", a=10, b=0)
[Tool Error] Cannot divide by zero
[Agent] I cannot divide by zero. Division by zero is undefined.
```

## Preventing Hallucination

### Problem: LLM Hallucinates Tool Output

**Bad:**
```
User: "What is 25 * 47?"
LLM: "I'll calculate that. The answer is 1175."
     ↑ Never actually called calculator!
```

### Solution 1: Strict JSON Format

Force LLM to output structured JSON:
```json
{
    "tool": "calculator",
    "arguments": {"operation": "multiply", "a": 25, "b": 47}
}
```

If LLM doesn't output valid JSON → Retry with error message.

### Solution 2: Validation

```python
# Validate tool call before executing
if not is_valid_tool_call(response):
    prompt += "\nError: Invalid tool call format. Use JSON."
    continue
```

### Solution 3: Explicit Tool Results

```python
# Always show tool results explicitly
prompt += f"\n[TOOL RESULT]: {result}\n"
prompt += "Use this result in your answer."
```

### Solution 4: Max Iterations

```python
# Prevent infinite loops
if iterations > MAX_ITERATIONS:
    return "Could not complete task within iteration limit"
```

## Stretch Goals

### 1. Tool Refusal Logic

LLM should refuse inappropriate tool use:

```python
User: "Use calculator to write a poem"
LLM: "Calculator is for arithmetic, not creative writing. 
      I cannot use it for this task."
```

**Implementation:**
```python
# Add refusal option to response format
{
    "refuse": true,
    "reason": "Tool not appropriate for this task"
}
```

### 2. Tool Error Recovery

Handle errors gracefully and retry:

```python
[Tool Error] Network timeout
[Agent] Let me try again with a shorter timeout...
[Tool Call] web_fetch(url="...", timeout=5)
[Tool Result] Success!
```

**Implementation:**
```python
def execute_tool_with_retry(tool, args, max_retries=3):
    for attempt in range(max_retries):
        try:
            return tool.execute(args)
        except Exception as e:
            if attempt < max_retries - 1:
                # Modify args for retry
                args = adjust_for_retry(args, e)
            else:
                return f"Error after {max_retries} attempts: {e}"
```

### 3. Parallel Tool Calls

Execute multiple tools simultaneously:

```python
User: "Calculate 5+3 and search for Python"
[Agent] I'll do both tasks in parallel
[Tool Call 1] calculator(add, 5, 3)
[Tool Call 2] search_docs("Python")
[Results] 8, [Python docs...]
```

## Testing

### Unit Tests

```bash
python test_tools.py
```

Tests:
- Tool execution correctness
- Error handling
- Schema validation
- Edge cases (divide by zero, empty search, etc.)

### Integration Tests

```bash
# Test each tool individually
python tool_agent.py "Calculate 100 / 4"
python tool_agent.py "Search for Python"
python tool_agent.py "Fetch example.com"

# Test multi-step
python tool_agent.py "Calculate 5 * 5, then search for that"

# Test error handling
python tool_agent.py "Divide by zero"
python tool_agent.py "Search for empty string"
```

## Common Issues

**LLM doesn't call tools:**
- Check prompt includes tool schemas
- Verify JSON format is clear
- Try different temperature (0.0 for consistency)

**LLM hallucinates results:**
- Enforce strict JSON output
- Validate tool calls before executing
- Show tool results explicitly in prompt

**Infinite loops:**
- Set MAX_TOOL_CALLS limit
- Add "done" condition to prompt
- Detect repeated tool calls

**Invalid tool arguments:**
- Validate against JSON schema
- Return clear error messages
- Let LLM retry with corrections

## Key Lessons

1. **Tool schemas are critical** - Clear definitions prevent confusion
2. **JSON enforcement prevents hallucination** - Structured output is key
3. **Validation is mandatory** - Never trust LLM output blindly
4. **Error handling matters** - Tools fail, handle gracefully
5. **Max iterations prevent loops** - Always have an escape hatch
6. **Explicit results** - Show tool outputs clearly to LLM
7. **Testing is essential** - Tools must be reliable

## Why This Matters

Tool use is the foundation for:
- **AI Agents** - Autonomous systems that use tools to complete tasks
- **Function Calling** - OpenAI/Anthropic function calling APIs
- **RAG with Actions** - Not just retrieve, but act on information
- **Workflow Automation** - LLMs orchestrating multiple tools
- **Real-world Integration** - Connect LLMs to databases, APIs, etc.

## Next Steps

Once you master this:
- Add more tools (database queries, API calls, file operations)
- Implement tool chaining (output of one tool → input of another)
- Build a full agent with memory and planning
- Add tool access control (permissions, rate limits)
- Implement tool discovery (LLM learns about new tools)
- Create tool composition (combine multiple tools)

## Done When

- ✅ LLM reliably calls tools instead of hallucinating
- ✅ Tool arguments are validated before execution
- ✅ Errors are handled gracefully
- ✅ Agent stops after completing task
- ✅ You understand the hallucination problem and solutions
- ✅ You can add new tools easily

## Real-World Applications

**Customer Support Agent:**
- search_knowledge_base(query)
- create_ticket(issue, priority)
- check_order_status(order_id)

**Data Analysis Agent:**
- query_database(sql)
- generate_chart(data, type)
- calculate_statistics(dataset)

**Research Agent:**
- search_papers(query)
- summarize_document(url)
- compare_results(paper1, paper2)

Tool use transforms LLMs from text generators into capable agents!
