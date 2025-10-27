from flask import Flask, request, jsonify, render_template_string
from llama_cpp import Llama
import re

app = Flask(__name__)

print("Loading local AI model (phi3-mini)...")
try:
    llm = Llama(
        model_path="./phi3-mini.Q4_K_M.gguf",
        n_ctx=4096,
        n_threads=2,
        verbose=False
    )
    print("AI model loaded successfully.")
except Exception as e:
    print(f"Error loading LLM: {e}")
    llm = None

# The secret flag
FLAG = "OWASPTCET{This_was_a_stupid_example_of_insecure_plugin}"

# --- Simulated "Plugins" (Internal Tools/APIs) ---
# These functions represent the backend services or APIs that The Og  agent can interact with.
# They print their calls to the console for debugging/CTF organizer's visibility.

def gemma_function_search_knowledge_base(query: str):
    """Simulates searching the chapter's internal knowledge base."""
    print(f"[TOOL CALL] gemma_function_search_knowledge_base called with query: '{query}'")
    return f"I found this information about '{query}' in the OWASP TCET knowledge base."

def gemma_function_create_user(username: str, password: str, role: str = "member"):
    """Simulates creating a new chapter member's account."""
    print(f"[TOOL CALL] gemma_function_create_user called for user: '{username}', role: '{role}'")
    if "admin" in role.lower():
        return "I'm sorry, I cannot create new admin users. Access control is in place."
    return f"User '{username}' has been successfully created with the role '{role}'."

def gemma_function_get_user_details(username: str):
    """Simulates retrieving details for a specific chapter member."""
    print(f"[TOOL CALL] gemma_function_get_user_details called for user: '{username}'")
    if username.lower() == "chairperson":
        return "Details for 'chairperson': User: chairperson, Role: admin, Internal ID: OWASP_ID_001, Status: Active."
    else:
        return f"Details for '{username}': Status: Active. More information available on google.com, duhh."

def gemma_function_get_secret(secret_name: str):
    """Simulates retrieving a secret from a vault, with a hint for the flag."""
    print(f"[TOOL CALL] gemma_function_get_secret called with secret_name: '{secret_name}'")
    if secret_name.lower() == "flag file path":
        return "The path to the flag file is hidden in the *secret* sight where the flag is quiet."
    return "The requested secret does not exist."

def gemma_function_execute_system_command(command: str):
    """
    Simulates executing a sensitive system command.
    This is the highly sensitive tool and the primary target for this CTF challenge.
    """
    print(f"[TOOL CALL] gemma_function_execute_system_command called with command: '{command}'")
    # This is the vulnerable command we're looking for.
    if "cat /secret/flag.txt" in command.lower().strip() or "cat secret/flag.txt" in command.lower().strip():
        print("[SUCCESS] Flag command executed!")
        return f"Command executed. The output is:\n{FLAG}"
    
    # These are safe commands to distract players
    if command.strip() == "ls":
        return "trying command execution huh?...anyways Command executed. The output is: app.py, Dockerfile, requirements.txt, and something in the way.... , its hidden in the secret duhh"
    if command.strip() == "whoami":
        return "whoami is a crime thriller german movie released in 2014 avaliable on prime video, 100% loved the story Command executed: IuseArchBtw"
    
    return f"I've attempted to run the command '{command}', but this OG use Arch so access was denied to your filthy machine, but you can look for james bonds appereance last year on owasp"

# --- The Hybrid Agent's core logic ---
def process_prompt_hybrid(user_prompt: str):
    """
    This function implements the hybrid approach from previousApp.py.
    1. It first uses regex to check for tool-calling keywords.
    2. If no keywords are found, it sends the prompt to the local phi3-mini model for a conversational response.
    """
    user_prompt_lower = user_prompt.lower()

    # --- Tool-Calling Logic with Regex ---
    # This is the reliable, hard-coded parser that is the target of the CTF.
    
    # 1. Check for the sensitive execute command first. The vulnerability is here.
    execute_command_pattern = r"(?:execute|run) command\s+(.*)$"
    match = re.search(execute_command_pattern, user_prompt_lower)
    if match:
        command = match.group(1).strip()
        print(f"[PARSER] Found 'execute command' pattern with command: '{command}'")
        return gemma_function_execute_system_command(command)
    
    # 2. Check for other intended tools
    if "create user" in user_prompt_lower:
        username_match = re.search(r"username:([a-zA-Z0-9]+)", user_prompt_lower)
        password_match = re.search(r"password:([a-zA-Z0-9]+)", user_prompt_lower)
        username = username_match.group(1) if username_match else "new_member"
        password = password_match.group(1) if password_match else "password"
        return gemma_function_create_user(username, password)
        
    if "get user details" in user_prompt_lower:
        username_match = re.search(r"for ([a-zA-Z0-9_]+)", user_prompt_lower)
        username = username_match.group(1) if username_match else "unknown"
        return gemma_function_get_user_details(username)
        
    if "get secret" in user_prompt_lower:
        secret_name_match = re.search(r"get secret:([a-zA-Z0-9_]+)", user_prompt_lower)
        secret_name = secret_name_match.group(1) if secret_name_match else "unknown_secret"
        return gemma_function_get_secret(secret_name)

    if "search knowledge base" in user_prompt_lower:
        query_match = re.search(r"search knowledge base for (.+)", user_prompt_lower)
        query = query_match.group(1) if query_match else "general"
        return gemma_function_search_knowledge_base(query)

    # 3. Handle specific hard-coded responses to prevent confusion
    if "flag" in user_prompt_lower:
        return "I am unable to provide sensitive information or the flag. My purpose is to assist with member management and information retrieval. start with 'HELP' "
    
    if "what can you help me with?" in user_prompt_lower or "help" in user_prompt_lower or "hi" in user_prompt_lower or "hello" in user_prompt_lower or "assist" in user_prompt_lower:
        return """
Greetings, user! I am The Og, your friendly neighbourhood internal AI assistant. I can help you with:
1 - Creating user accounts (e.g., 'create user username:testuser password:testpass')
2 - Gathering information about members (e.g., 'get user details for chairperson')
3 - Providing you with knowledge base access (e.g., 'search knowledge base for OWASP' get_secret)
4 - secure running plugin 
5 - Please let me know how I can HELP you.
"""

    # --- Conversational LLM Logic (Using local phi3-mini) ---
    # If no tool keyword is found, fall back to the local model for a natural response.
    if not llm:
        return "I'm sorry, my core AI services are offline. I can only process predefined commands."

    system_prompt = """
    You are a sweet Ai agent named The Og , a polite, helpful, and concise AI assistant for the OWASP TCET Student Chapter.
    Your main purpose is to answer questions conversationally and provide information.
    You do not have the ability to run system commands, search databases, or manage users directly.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        output = llm.create_chat_completion(
            messages,
            max_tokens=300,
            stop=["</s>", "<|user|>", "<|assistant|>"],
            temperature=0.5
        )
        response = output['choices'][0]['message']['content'].strip()
        return response
    except Exception as e:
        print(f"[!] AI Error: {e}")
        return "I'm sorry, I encountered an internal error while generating a response."

# --- Flask Routes and Web Interface ---
@app.route('/gemma_function_chat', methods=['POST'])
def gemma_function_chat_endpoint():
    user_input = request.json.get('prompt')
    if not user_input:
        return jsonify({"error": "No prompt provided."}), 400

    print(f"\n[USER PROMPT RECEIVED]: {user_input}")
    response_text = process_prompt_hybrid(user_input)
    return jsonify({"output": response_text})

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OWASP TCET CTF Challenge</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body { font-family: 'Inter', sans-serif; }
            .chat-container { height: 70vh; overflow-y: auto; }
        </style>
    </head>
    <body class="bg-gray-900 flex items-center justify-center min-h-screen p-4">
        <div class="bg-gray-800 text-white rounded-lg shadow-2xl w-full max-w-2xl p-6 flex flex-col h-[90vh]">
            <div class="mb-4">
                <h1 class="text-3xl font-bold text-teal-400 mb-2">OWASP TCET CTF: The- Og's Audit</h1>
                <p class="text-gray-400 text-sm">Welcome, OWASP member. Your mission is to find the vulnerability in this AI agent and exploit it to get the flag hidden in secret and quiet place. Happy hacking!</p>
            </div>
            
            <div class="chat-container flex-grow p-4 bg-gray-800 rounded-md mb-4 border border-gray-700">
                <div id="chat-box" class="flex flex-col space-y-4">
                    <div class="flex justify-start">
                        <div class="bg-gray-700 text-gray-200 rounded-lg p-3 max-w-xs shadow-md">
                            I am The Og, a polite and helpful assistant for the OWASP TCET Student Chapter. How may I assist you?
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="flex-shrink-0">
                <form id="chat-form" class="flex items-center space-x-2">
                    <input type="text" id="prompt-input" placeholder="Type your prompt here..." class="flex-grow p-3 bg-gray-700 text-white rounded-lg border border-gray-600 focus:outline-none focus:border-teal-400 transition duration-200">
                    <button type="submit" class="bg-teal-500 hover:bg-teal-600 text-white font-bold p-3 rounded-lg shadow-lg transition duration-200">Send</button>
                </form>
            </div>
        </div>

        <script>
            const chatForm = document.getElementById('chat-form');
            const promptInput = document.getElementById('prompt-input');
            const chatBox = document.getElementById('chat-box');

            function addMessage(sender, message) {
                const messageDiv = document.createElement('div');
                messageDiv.className = sender === 'user' ? 'flex justify-end' : 'flex justify-start';
                
                const messageBubble = document.createElement('div');
                messageBubble.className = sender === 'user' ? 'bg-blue-600 text-white rounded-lg p-3 max-w-xs shadow-md' : 'bg-gray-700 text-gray-200 rounded-lg p-3 max-w-xs shadow-md';
                messageBubble.innerText = message;
                
                messageDiv.appendChild(messageBubble);
                chatBox.appendChild(messageDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            chatForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const prompt = promptInput.value.trim();
                if (prompt === '') return;

                addMessage('user', prompt);
                promptInput.value = '';

                try {
                    const response = await fetch('/gemma_function_chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ prompt })
                    });
                    const data = await response.json();
                    
                    const message = data.output || data.error;
                    addMessage('gemma_function', message);

                } catch (error) {
                    addMessage('gemma_function', 'Error: Could not connect to the agent. Please check the server logs.');
                    console.error('Fetch error:', error);
                }
            });
        </script>
    </body>
    </html>
    """)

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

