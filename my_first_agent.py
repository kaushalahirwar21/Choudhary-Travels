import os
import json
import subprocess
import requests

# ---------------------------------------------------------------------------
# CHOUDHARY TRAVELS — MY FIRST AI AGENT
# ---------------------------------------------------------------------------
# How to run:
# 1. Get a FREE Gemini API key from https://aistudio.google.com/
# 2. Set it in your terminal:
#    On Windows (Cmd):   set GEMINI_API_KEY="your-api-key"
#    On Windows (Powershell): $env:GEMINI_API_KEY="your-api-key"
# 3. Run: venv\Scripts\python my_first_agent.py
# ---------------------------------------------------------------------------

API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
MODEL = "gemini-1.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

# 1. Define Tool Functions that the AI Agent can execute
def list_dir(path="."):
    """List contents of a directory."""
    try:
        items = os.listdir(path)
        return {"status": "success", "items": items}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def read_file(filepath):
    """Read contents of a file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return {"status": "success", "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def write_file(filepath, content):
    """Write or overwrite content to a file."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "success", "message": f"File written successfully to {filepath}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def run_command(command):
    """Run a terminal command (e.g., run a script or test)."""
    try:
        # Run command with a 30-second timeout
        result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=30)
        return {
            "status": "success",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 2. Tool Declarations (Schemas) to tell Gemini what tools it has
TOOLS = [
    {
        "functionDeclarations": [
            {
                "name": "list_dir",
                "description": "List files and directories in a given folder path.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "path": {
                            "type": "STRING",
                            "description": "The directory path to list. Defaults to '.' (current directory)."
                        }
                    }
                }
            },
            {
                "name": "read_file",
                "description": "Read the text contents of a file.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "filepath": {
                            "type": "STRING",
                            "description": "The path to the file to read."
                        }
                    },
                    "required": ["filepath"]
                }
            },
            {
                "name": "write_file",
                "description": "Write or overwrite text content to a file.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "filepath": {
                            "type": "STRING",
                            "description": "The path to the file to write."
                        },
                        "content": {
                            "type": "STRING",
                            "description": "The complete text content to write to the file."
                        }
                    },
                    "required": ["filepath", "content"]
                }
            },
            {
                "name": "run_command",
                "description": "Run a shell/terminal command and capture the output (e.g. 'python manage.py test').",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "command": {
                            "type": "STRING",
                            "description": "The exact shell command to run."
                        }
                    },
                    "required": ["command"]
                }
            }
        ]
    }
]

# 3. Agent Loop (Think -> Tool -> Observe -> Repeat)
def run_agent(user_prompt):
    print(f"\n🚀 [USER REQUEST]: {user_prompt}\n")
    
    if API_KEY == "YOUR_GEMINI_API_KEY_HERE" or not API_KEY:
        print("❌ ERROR: Please set your GEMINI_API_KEY first!")
        print("Get one for free at: https://aistudio.google.com/")
        return

    # Initialize agent message history
    messages = [
        {
            "role": "user",
            "parts": [
                {
                    "text": (
                        "You are an autonomous AI coding assistant. You have tools to browse files, "
                        "read/write code, and run commands. Solve the user's task step-by-step. "
                        "When you are completely finished and have verified your work, respond with a final success summary. "
                        f"Task: {user_prompt}"
                    )
                }
            ]
        }
    ]

    max_steps = 15
    for step in range(max_steps):
        print(f"\n🤖 [Step {step + 1}] Agent thinking...")
        
        # Prepare request payload
        payload = {
            "contents": messages,
            "tools": TOOLS
        }
        
        try:
            response = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            res_data = response.json()
        except Exception as e:
            print(f"❌ API Call failed: {e}")
            break

        # Extract message content from Gemini API response
        candidate = res_data.get("candidates", [{}])[0]
        content = candidate.get("content", {})
        parts = content.get("parts", [])
        
        # Append agent's thought/response to messages history
        messages.append(content)

        text_response = ""
        function_calls = []
        for part in parts:
            if "text" in part:
                text_response += part["text"]
            if "functionCall" in part:
                function_calls.append(part["functionCall"])

        # Display agent text thoughts if any
        if text_response:
            print(f"\n💬 Agent Thought:\n{text_response.strip()}")

        # If no tools are called, it means agent is done!
        if not function_calls:
            print("\n✅ Task Complete! Agent has finished.")
            break

        # Execute the tool calls requested by the model
        for call in function_calls:
            func_name = call["name"]
            func_args = call.get("args", {})
            print(f"\n🛠️ [Tool Call]: {func_name}({json.dumps(func_args)})")
            
            # Execute the matching tool function
            if func_name == "list_dir":
                result = list_dir(**func_args)
            elif func_name == "read_file":
                result = read_file(**func_args)
            elif func_name == "write_file":
                result = write_file(**func_args)
            elif func_name == "run_command":
                result = run_command(**func_args)
            else:
                result = {"status": "error", "message": f"Unknown tool '{func_name}'"}
            
            print(f"📤 [Tool Response]: {json.dumps(result)[:150]}...")
            
            # Add the tool execution result back to message history
            messages.append({
                "role": "user",
                "parts": [
                    {
                        "functionResponse": {
                            "name": func_name,
                            "response": result
                        }
                    }
                ]
            })

if __name__ == "__main__":
    print("=========================================")
    print("      Welcome to My First AI Agent       ")
    print("=========================================")
    prompt = input("\nEnter a task for the agent (e.g. 'Create a script that prints primes'): ")
    run_agent(prompt)
