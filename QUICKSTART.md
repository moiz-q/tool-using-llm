# Quick Start Guide

Get up and running with Tool-Using LLM in 5 minutes.

## Prerequisites

1. **Ollama installed and running**
   ```bash
   ollama serve
   ```

2. **Pull required model**
   ```bash
   ollama pull llama3.2
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 5-Minute Demo

### Step 1: Test Tools (30 seconds)

```bash
python tools.py
```

This tests all three tools:
- Calculator (arithmetic operations)
- Search Documents (local document search)
- Web Fetch (mocked web content)

### Step 2: Test Tool Agent (2 minutes)

**Simple calculation:**
```bash
python tool_agent.py "What is 25 * 47?"
```

**Document search:**
```bash
python tool_agent.py "Search for information about Python"
```

**Web fetch:**
```bash
python tool_agent.py "What is the title of python.org?"
```

### Step 3: Multi-Step Tasks (2 minutes)

**Calculation then search:**
```bash
python tool_agent.py "Calculate 10 * 5, then search for that number"
```

**Multiple calculations:**
```bash
python tool_agent.py "What is 15 + 30, then multiply that by 2?"
```

### Step 4: Error Handling (30 seconds)

**Divide by zero:**
```bash
python tool_agent.py "Divide 10 by 0"
```

**Invalid tool use:**
```bash
python tool_agent.py "Use calculator to write a poem"
```

## What You'll See

### Successful Tool Call

```
--- Iteration 1 ---
LLM Response: {"tool": "calculator", "arguments": {"operation": "multiply", "a": 25, "b": 47}}

[Tool Call] calculator({"operation": "multiply", "a": 25, "b": 47})
[Tool Result] {
  "success": true,
  "result": 1175
}

[Done] The answer is 1175
```

### Error Handling

```
--- Iteration 1 ---
[Tool Call] calculator({"operation": "divide", "a": 10, "b": 0})
[Tool Result] {
  "success": false,
  "error": "Cannot divide by zero"
}

[Done] I cannot divide by zero. Division by zero is undefined.
```

## Key Concepts

### 1. Tool Schemas

The LLM sees tool definitions:
```json
{
  "name": "calculator",
  "description": "Performs basic arithmetic operations",
  "parameters": {
    "operation": "add|subtract|multiply|divide",
    "a": "number",
    "b": "number"
  }
}
```

### 2. JSON Enforcement

LLM must respond with valid JSON:
```json
{
  "tool": "calculator",
  "arguments": {"operation": "add", "a": 5, "b": 3}
}
```

### 3. Tool Execution

System executes the tool and returns real results:
```json
{
  "success": true,
  "result": 8
}
```

### 4. Iteration Loop

Agent continues until task is complete:
```json
{"done": true, "answer": "The answer is 8"}
```

## Common Patterns

### Single Tool Call

```bash
python tool_agent.py "What is 100 / 4?"
```
→ Calls calculator once, returns answer

### Multi-Step

```bash
python tool_agent.py "Calculate 5 * 5, then search for that"
```
→ Calls calculator, then search_docs

### Tool Refusal

```bash
python tool_agent.py "Use calculator to predict the weather"
```
→ LLM refuses inappropriate tool use

## Testing

Run the test suite:
```bash
python test_tools.py
```

Tests:
- Calculator operations
- Document search
- Web fetch
- Error handling
- Edge cases

## Next Steps

1. Read the full [README.md](README.md) for detailed explanations
2. Try your own questions
3. Add new tools (see README for examples)
4. Experiment with multi-step tasks

## Troubleshooting

**"Ollama connection error"**
- Make sure Ollama is running: `ollama serve`
- Check model is available: `ollama list`

**"Invalid JSON response"**
- LLM might not be following format
- Try running again (temperature=0.0 helps)
- Check prompt in tool_agent.py

**"Max iterations reached"**
- Task might be too complex
- Increase --max-iterations flag
- Break task into simpler questions

**"Tool not found"**
- Check tool name spelling
- See available tools: `python tools.py`

## Questions?

Check the [README.md](README.md) for comprehensive documentation on:
- How tool calling works
- Preventing hallucination
- Adding new tools
- Advanced patterns
