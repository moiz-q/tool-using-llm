# Troubleshooting Guide

Common issues and solutions for tool-using LLM.

## Issue: LLM Doesn't Finish (Loops Forever)

**Symptoms:**
```
--- Iteration 1 ---
[Tool Call] calculator(...)
[Tool Result] {...}

--- Iteration 2 ---
[Tool Call] calculator(...)  ← Same tool again!
[Tool Result] {...}

[Max Iterations] Reached 5 iterations
```

**Cause:** LLM not outputting `{"done": true, "answer": "..."}`

**Solutions:**
1. Check prompt clarity - Make sure "done" condition is explicit
2. Try temperature=0.0 for more consistent behavior
3. Add explicit instruction after tool result: "Now finish with your answer"
4. Use a model with better instruction following (llama3.2 works well)

---

## Issue: Invalid JSON Response

**Symptoms:**
```
[Error] Invalid JSON response, retrying...
```

**Cause:** LLM outputting text instead of JSON

**Solutions:**
1. Enable `json_mode=True` in llm.py (forces JSON output)
2. Make prompt clearer: "Respond with ONLY JSON, no other text"
3. Try different temperature (0.0 is most consistent)
4. Check if model supports JSON mode

---

## Issue: LLM Hallucinates Tool Results

**Symptoms:**
```
LLM Response: "The answer is 1175"  ← No tool call!
```

**Cause:** LLM bypassing tool system

**Solutions:**
1. Enforce JSON schema strictly
2. Validate response format before accepting
3. Retry with error message if format is wrong
4. Make prompt explicit: "You MUST call tools, never guess results"

---

## Issue: Tool Not Found

**Symptoms:**
```
[Tool Result] {
  "success": false,
  "error": "Tool 'xyz' not found"
}
```

**Cause:** LLM using wrong tool name

**Solutions:**
1. Check tool name spelling in tools.py
2. Verify tool schemas are passed to LLM
3. Make tool names clear and descriptive
4. Add available tools list to error message

---

## Issue: Invalid Tool Arguments

**Symptoms:**
```
[Tool Result] {
  "success": false,
  "error": "Invalid arguments for tool 'calculator'"
}
```

**Cause:** LLM passing wrong argument types or missing required args

**Solutions:**
1. Check JSON schema in tools.py
2. Make parameter descriptions clearer
3. Add examples to tool descriptions
4. Validate arguments before execution

---

## Issue: Ollama Connection Error

**Symptoms:**
```
Error: LLM call failed after 3 attempts: Connection refused
```

**Cause:** Ollama not running

**Solutions:**
1. Start Ollama: `ollama serve`
2. Check Ollama is running: `ollama list`
3. Verify port 11434 is accessible
4. Check firewall settings

---

## Issue: Model Not Found

**Symptoms:**
```
Error: model 'llama3.2' not found
```

**Cause:** Model not pulled

**Solutions:**
1. Pull model: `ollama pull llama3.2`
2. Check available models: `ollama list`
3. Try different model: Change in tool_agent.py

---

## Issue: Slow Response

**Symptoms:**
- Takes 30+ seconds per iteration
- System feels sluggish

**Causes & Solutions:**

**1. Large model:**
- Use smaller model: `ollama pull llama3.2` (smaller than llama3.1)
- Check model size: `ollama list`

**2. CPU-only inference:**
- Ollama uses GPU if available
- Check GPU usage during inference
- Consider cloud GPU if local is slow

**3. Complex prompts:**
- Simplify tool schemas
- Reduce conversation history
- Use shorter descriptions

---

## Issue: Tool Refusal When It Shouldn't

**Symptoms:**
```
[Refused] Calculator is not appropriate for this task
```
But the task IS appropriate for calculator.

**Cause:** LLM misunderstanding task

**Solutions:**
1. Rephrase question more clearly
2. Make tool descriptions more explicit
3. Add examples to tool schemas
4. Try different temperature

---

## Issue: Multi-Step Fails

**Symptoms:**
```
--- Iteration 1 ---
[Tool Call] calculator(...)
[Tool Result] 50

--- Iteration 2 ---
[Tool Call] search_docs("Python")  ← Should search for "50"!
```

**Cause:** LLM not using previous result

**Solutions:**
1. Make prompt clearer about using results
2. Add explicit instruction: "Use the result from previous tool"
3. Show conversation history more clearly
4. Try temperature=0.0 for consistency

---

## Issue: Max Iterations Reached

**Symptoms:**
```
[Max Iterations] Reached 5 iterations
Could not complete task within 5 iterations
```

**Causes & Solutions:**

**1. Task too complex:**
- Break into simpler questions
- Increase max iterations: `--max-iterations 10`

**2. LLM stuck in loop:**
- Check if calling same tool repeatedly
- Improve prompt to add "done" condition
- Add loop detection logic

**3. Multi-step task:**
- This is normal for complex tasks
- Increase max iterations
- Or simplify the task

---

## Debugging Tips

### 1. Enable Verbose Mode

Already enabled by default. Shows:
- LLM responses
- Tool calls
- Tool results
- Iteration count

### 2. Check Tool Execution

Test tools directly:
```bash
python tools.py
```

### 3. Run Unit Tests

```bash
python test_tools.py
```

### 4. Test with Simple Questions

Start simple, then increase complexity:
```bash
# Simple
python tool_agent.py "What is 5 + 3?"

# Medium
python tool_agent.py "Search for Python"

# Complex
python tool_agent.py "Calculate 10 * 5, then search for that"
```

### 5. Check JSON Parsing

Add debug prints in `_parse_response()`:
```python
print(f"Raw response: {response}")
print(f"Parsed: {parsed}")
```

### 6. Inspect Conversation History

Add print in agent loop:
```python
print(f"Conversation so far: {conversation_history}")
```

---

## Performance Optimization

### Reduce Latency

1. **Use smaller model:**
   ```bash
   ollama pull llama3.2  # Smaller, faster
   ```

2. **Reduce max iterations:**
   ```bash
   python tool_agent.py "question" --max-iterations 3
   ```

3. **Simplify tool schemas:**
   - Remove unnecessary parameters
   - Shorten descriptions
   - Remove examples from schemas

4. **Cache tool results:**
   - Store results of expensive operations
   - Reuse if same tool called with same args

### Improve Accuracy

1. **Use temperature=0.0:**
   - More consistent
   - Less creative but more reliable

2. **Better prompts:**
   - Clearer instructions
   - More examples
   - Explicit format requirements

3. **Validate everything:**
   - Check JSON format
   - Validate tool arguments
   - Verify tool exists

---

## Getting Help

If you're still stuck:

1. **Check examples:** See EXAMPLES.md for working traces
2. **Read README:** Comprehensive documentation
3. **Test tools:** Run `python test_tools.py`
4. **Simplify:** Start with simplest possible question
5. **Check Ollama:** Make sure it's running and model is loaded

## Common Patterns That Work

### Pattern 1: Simple Calculation
```bash
python tool_agent.py "What is X + Y?"
```
✓ Works reliably

### Pattern 2: Document Search
```bash
python tool_agent.py "Search for information about X"
```
✓ Works reliably

### Pattern 3: Multi-Step
```bash
python tool_agent.py "Calculate X, then search for that"
```
✓ Works with clear instructions

### Pattern 4: Error Handling
```bash
python tool_agent.py "Divide X by 0"
```
✓ Handles gracefully with refusal

## Patterns to Avoid

### ✗ Vague Questions
```bash
python tool_agent.py "Tell me something"
```
Too vague, LLM doesn't know which tool

### ✗ Impossible Tasks
```bash
python tool_agent.py "Calculate the meaning of life"
```
No appropriate tool available

### ✗ Too Many Steps
```bash
python tool_agent.py "Do A, then B, then C, then D, then E"
```
May exceed max iterations

---

## Still Having Issues?

1. Check Ollama is running: `ollama serve`
2. Verify model is available: `ollama list`
3. Test tools work: `python test_tools.py`
4. Try simplest question: `python tool_agent.py "What is 2 + 2?"`
5. Check Python version: Python 3.8+ required
6. Reinstall dependencies: `pip install -r requirements.txt`
