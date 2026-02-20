# Tool-Using LLM - Project Summary

## Overview

This is the 6th repository in a series teaching LLM and RAG fundamentals. It focuses on controlled tool calling where LLMs decide which tools to use, with what arguments, and when to stop - without hallucinating outputs.

## Learning Progression

1. **llm-basics-playground** - LLM fundamentals, prompting, structured outputs
2. **vector-store-from-scratch** - Embeddings, vector search, similarity
3. **rag-from-scratch** - Basic RAG pipeline from first principles
4. **rag-with-frameworks** - LangChain vs LlamaIndex comparison
5. **rag-quality-lab** - Production-quality RAG improvements
6. **tool-using-llm** ← You are here - Controlled tool calling

## What This Project Teaches

### Core Concepts

1. **Tool Definition**
   - JSON schemas for tools
   - Parameter validation
   - Clear descriptions for LLM

2. **Tool Calling Flow**
   - LLM decides which tool to use
   - Extracts arguments from user question
   - System executes tool
   - LLM uses results in answer

3. **Hallucination Prevention**
   - JSON schema enforcement
   - Strict output format
   - Validation before execution
   - Explicit tool results

4. **Control Mechanisms**
   - Max iterations (prevent infinite loops)
   - Tool refusal logic
   - Error handling and recovery
   - Done condition

### Available Tools

1. **Calculator** - Arithmetic operations (add, subtract, multiply, divide)
2. **Search Documents** - Local document search with keyword matching
3. **Web Fetch** - Mocked web content fetching (title, summary, content)

### Key Features

- **JSON Enforcement**: LLM must output valid JSON matching schema
- **Max Iterations**: Prevents infinite loops (default: 5)
- **Error Handling**: Tools return errors, LLM explains them
- **Tool Refusal**: LLM can refuse inappropriate tool use
- **Multi-Step**: LLM can chain multiple tool calls
- **Validation**: Arguments validated against schema

## Project Structure

```
tool-using-llm/
├── README.md              # Comprehensive documentation
├── QUICKSTART.md         # 5-minute getting started
├── EXAMPLES.md           # Real execution traces
├── PROJECT_SUMMARY.md    # This file
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
│
├── Core Components
├── llm.py               # LLM interface (Ollama)
├── tools.py             # Tool implementations
├── tool_agent.py        # Main agent loop
│
├── Testing
├── test_tools.py        # Unit tests for tools
│
└── Data
    └── docs/            # Sample documents (auto-created)
```

## Usage Examples

### Simple Calculation
```bash
python tool_agent.py "What is 25 * 47?"
```

### Document Search
```bash
python tool_agent.py "Search for information about Python"
```

### Multi-Step
```bash
python tool_agent.py "Calculate 10 * 5, then search for that number"
```

### Error Handling
```bash
python tool_agent.py "Divide 10 by 0"
```

### Tool Refusal
```bash
python tool_agent.py "Use calculator to write a poem"
```

## Technical Highlights

### The Hallucination Problem

**Without tool enforcement:**
```
User: "What is 25 * 47?"
LLM: "The answer is 1175"  ← Hallucinated! Never called calculator
```

**With tool enforcement:**
```
User: "What is 25 * 47?"
LLM: {"tool": "calculator", "arguments": {"operation": "multiply", "a": 25, "b": 47}}
System: Executes → 1175
LLM: "The answer is 1175"  ← Verified!
```

### Agent Loop

```python
while not done and iterations < MAX:
    # 1. Get LLM response (JSON)
    response = call_llm(prompt)
    
    # 2. Parse and validate
    parsed = parse_json(response)
    
    # 3. Check if done
    if parsed.get("done"):
        return parsed["answer"]
    
    # 4. Execute tool
    result = execute_tool(parsed["tool"], parsed["arguments"])
    
    # 5. Add result to conversation
    prompt += f"\nTool result: {result}\n"
```

### Control Mechanisms

**JSON Schema:**
```json
{
  "tool": "calculator",
  "arguments": {
    "operation": "multiply",
    "a": 25,
    "b": 47
  }
}
```

**Max Iterations:**
```python
MAX_ITERATIONS = 5  # Prevent infinite loops
```

**Tool Refusal:**
```json
{
  "refuse": true,
  "reason": "Tool not appropriate for this task"
}
```

**Done Condition:**
```json
{
  "done": true,
  "answer": "The answer is 1175"
}
```

## Key Lessons

1. **JSON enforcement prevents hallucination** - LLM can't fake tool results
2. **Validation is critical** - Check tool exists and arguments are valid
3. **Error handling matters** - Tools fail, handle gracefully
4. **Max iterations prevent loops** - Always have escape hatch
5. **Tool refusal is smart** - LLM should know tool limitations
6. **Multi-step works** - LLM can chain tool calls
7. **Explicit results** - Show tool outputs clearly to LLM

## Comparison: With vs Without Tools

### Without Tools (Pure LLM)
```
User: "What is 25 * 47?"
LLM: "The answer is 1175"
     ↑ Might be wrong! No verification
```

### With Tools
```
User: "What is 25 * 47?"
LLM: Calls calculator(multiply, 25, 47)
System: Returns 1175
LLM: "The answer is 1175"
     ↑ Verified! Actual calculation
```

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

## Success Metrics

The project is successful when:
- ✅ LLM calls tools instead of hallucinating
- ✅ Tool arguments are validated
- ✅ Errors are handled gracefully
- ✅ Agent stops after completing task
- ✅ Multi-step tasks work correctly
- ✅ Tool refusal works appropriately

## Repository Stats

- **Lines of Code**: ~800
- **Python Files**: 5
- **Documentation**: 4 markdown files
- **Tools Implemented**: 3
- **Dependencies**: 1 package (requests)
- **Estimated Learning Time**: 1-2 hours

## Next Steps

After mastering this:
1. Add more tools (database, API calls, file operations)
2. Implement tool chaining (output → input)
3. Add tool access control (permissions, rate limits)
4. Build full agent with memory and planning
5. Implement parallel tool execution
6. Add tool discovery (LLM learns new tools)

## Credits

Part of a comprehensive LLM/RAG learning series:
1. llm-basics-playground
2. vector-store-from-scratch
3. rag-from-scratch
4. rag-with-frameworks
5. rag-quality-lab
6. tool-using-llm ← Current

Built with Ollama for free, local, private LLM access.

## Why This Matters

Tool use is the foundation for:
- **AI Agents** - Autonomous systems that complete tasks
- **Function Calling** - OpenAI/Anthropic function calling APIs
- **RAG with Actions** - Not just retrieve, but act
- **Workflow Automation** - LLMs orchestrating tools
- **Real-world Integration** - Connect LLMs to systems

Tool use transforms LLMs from text generators into capable agents!
