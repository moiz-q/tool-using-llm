"""
Tool-using agent that decides which tools to call and when to stop.
"""

import json
import argparse
from typing import Dict, Any, Optional
from llm import call_llm
from tools import get_tool_schemas, execute_tool, TOOLS


class ToolAgent:
    """
    Agent that uses tools to answer questions.
    """
    
    def __init__(self, max_iterations: int = 5, verbose: bool = True):
        """
        Initialize tool agent.
        
        Args:
            max_iterations: Maximum number of tool calls
            verbose: Print detailed trace
        """
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.tool_schemas = get_tool_schemas()
    
    def run(self, question: str) -> str:
        """
        Run agent to answer question using tools.
        
        Args:
            question: User question
        
        Returns:
            Final answer
        """
        if self.verbose:
            print("="*80)
            print("TOOL-USING AGENT")
            print("="*80)
            print(f"\nQuestion: {question}\n")
        
        # Build initial prompt
        prompt = self._build_prompt(question)
        
        iteration = 0
        conversation_history = []
        last_tool_call = None
        
        while iteration < self.max_iterations:
            iteration += 1
            
            if self.verbose:
                print(f"\n--- Iteration {iteration} ---")
            
            # Get LLM response
            try:
                response = call_llm(prompt, temperature=0.0, json_mode=True)
                
                if self.verbose:
                    print(f"LLM Response: {response[:200]}...")
                
                # Parse response
                parsed = self._parse_response(response)
                
                if parsed is None:
                    # Invalid JSON, retry
                    if self.verbose:
                        print("[Error] Invalid JSON response, retrying...")
                    prompt += f"\n\nError: Your response was not valid JSON. Please respond with valid JSON matching the format specified."
                    continue
                
                # Check if done
                if parsed.get("done"):
                    answer = parsed.get("answer", "Task completed.")
                    if self.verbose:
                        print(f"\n[Done] {answer}")
                    return answer
                
                # Check for tool refusal
                if parsed.get("refuse"):
                    reason = parsed.get("reason", "Tool not appropriate")
                    if self.verbose:
                        print(f"\n[Refused] {reason}")
                    return f"I cannot complete this task: {reason}"
                
                # Execute tool
                tool_name = parsed.get("tool")
                arguments = parsed.get("arguments", {})
                
                if not tool_name:
                    if self.verbose:
                        print("[Error] No tool specified")
                    prompt += f"\n\nError: You must specify a tool name or set 'done': true."
                    continue
                
                # Check for repeated tool calls (loop detection)
                current_call = (tool_name, json.dumps(arguments, sort_keys=True))
                if current_call == last_tool_call:
                    if self.verbose:
                        print(f"\n[Warning] Repeated tool call detected. Forcing completion.")
                    # Force the LLM to finish
                    prompt += f"\n\nYou just called the same tool with the same arguments. You MUST now respond with: {{\"done\": true, \"answer\": \"your final answer using the results you have\"}}"
                    last_tool_call = None
                    continue
                
                last_tool_call = current_call
                
                if self.verbose:
                    print(f"\n[Tool Call] {tool_name}({json.dumps(arguments)})")
                
                # Execute tool
                result = execute_tool(tool_name, arguments)
                
                if self.verbose:
                    print(f"[Tool Result] {json.dumps(result, indent=2)}")
                
                # Add result to conversation
                conversation_history.append({
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": result
                })
                
                # Update prompt with result - be smarter about multi-step
                if result.get("success"):
                    prompt += f"\n\nTool: {tool_name}\nArguments: {json.dumps(arguments)}\nResult: {json.dumps(result)}\n\nNow decide: Is the user's question fully answered? If yes, respond with {{\"done\": true, \"answer\": \"...\"}}. If you need another tool to complete the task, call it now."
                else:
                    prompt += f"\n\nTool: {tool_name}\nArguments: {json.dumps(arguments)}\nResult: {json.dumps(result)}\n\nThe tool returned an error. Respond with: {{\"done\": true, \"answer\": \"explain the error to the user\"}}"
            
            except Exception as e:
                if self.verbose:
                    print(f"[Error] {str(e)}")
                return f"Error: {str(e)}"
        
        # Max iterations reached
        if self.verbose:
            print(f"\n[Max Iterations] Reached {self.max_iterations} iterations")
        
        return f"Could not complete task within {self.max_iterations} iterations. Tool calls made: {len(conversation_history)}"
    
    def _build_prompt(self, question: str) -> str:
        """
        Build initial prompt with tool schemas.
        
        Args:
            question: User question
        
        Returns:
            Formatted prompt
        """
        tools_json = json.dumps(self.tool_schemas, indent=2)
        
        prompt = f"""You are a helpful assistant with access to tools. Your job is to answer the user's question by using the appropriate tools.

Available tools:
{tools_json}

CRITICAL RULES:
1. To use a tool, respond with ONLY this JSON:
   {{"tool": "tool_name", "arguments": {{"param": "value"}}}}

2. After you receive a tool result, you MUST respond with ONLY this JSON:
   {{"done": true, "answer": "your final answer using the tool result"}}

3. If a tool is not appropriate, respond with ONLY this JSON:
   {{"refuse": true, "reason": "explanation"}}

4. NEVER make up tool results - always wait for actual tool execution
5. ALWAYS finish after getting a tool result - do not call the same tool twice

User question: {question}

Respond with JSON only:"""
        
        return prompt
    
    def _parse_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Parse LLM response as JSON.
        
        Args:
            response: LLM response string
        
        Returns:
            Parsed dict or None if invalid
        """
        try:
            # Try to parse as JSON
            parsed = json.loads(response)
            return parsed
        except json.JSONDecodeError:
            # Try to extract JSON from response
            try:
                # Look for JSON object in response
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end > start:
                    json_str = response[start:end]
                    parsed = json.loads(json_str)
                    return parsed
            except:
                pass
            
            return None


def main():
    parser = argparse.ArgumentParser(description="Tool-using agent")
    parser.add_argument("question", help="Question to answer")
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=5,
        help="Maximum tool calls"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress detailed output"
    )
    
    args = parser.parse_args()
    
    # Create agent
    agent = ToolAgent(
        max_iterations=args.max_iterations,
        verbose=not args.quiet
    )
    
    # Run agent
    answer = agent.run(args.question)
    
    # Print final answer
    if not args.quiet:
        print("\n" + "="*80)
        print("FINAL ANSWER")
        print("="*80)
    print(answer)


if __name__ == "__main__":
    main()
