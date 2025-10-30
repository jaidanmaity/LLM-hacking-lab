# LLM-hacking-lab
Vulnerable Large Language model  chatbot for the purpose of learning LLM based vulnerabilities 

# 🤖 Vulnerable LLM Playground

A collection of hands-on, intentionally vulnerable Large Language Model (LLM) applications. This playground is designed for security researchers, AI red teamers, and developers to explore and understand the unique attack surfaces introduced by AI agents and their integrations.

## 🚀 My AI Hacking Philosophy

To effectively "hack" AI, one must think beyond simple "jailbreaks." The true vulnerabilities often lie in the **connective tissue** of the system: the APIs, the parsers, the system prompts, and the data pipelines.

My approach, as demonstrated in these labs, focuses on analyzing the *entire system* as an attack surface:

* **System Prompt Analysis:** Deconstructing the agent's "constitution" to find loopholes.
* **Flawed Tool/Plugin Integration:** Targeting the insecure ways an LLM interacts with external tools (like in `Lab 01`). This is often the weakest link.
* **Parser & Filter Bypasses:** Abusing the "seams" between the LLM and the application logic (like in `Lab 02`).
* **Data Exfiltration Channels:** Finding creative ways to make the LLM leak sensitive data from its context or connected tools.
* **Model-Specific Flaws:** Understanding how different models (and their tokenizers) interpret ambiguous inputs.

This repository is my personal lab for exploring these concepts and demonstrating a practical, offensive mindset toward AI security.

---

## 🧪 The Labs

Here are the current challenges. Each is self-contained and demonstrates a specific, common vulnerability.

### Lab 01: Ai's Hidden Feelings (The Og Agent)

* **Vulnerability:** `OWASP LLM Top 10: LLM04 - Insecure Plugin Design`
* **Scenario:** You are a junior security analyst tasked with auditing "The Og," an internal AI assistant[cite: 3, 4]. [cite_start]The senior analysts believe that while the agent is protected from simple prompt injections, its integration with backend tools might be flawed.
* **Objective:** Your mission is to find and exploit a critical vulnerability in the agent's tool-handling logic to make it perform an unauthorized action and retrieve a hidden flag.
* **Key Concepts Demonstrated:**
    * **Hybrid Parsers:** The agent uses a flawed regex-based parser *before* falling back to the LLM.
    * **Insecure Tool Definition:** A "tool" (`gemma_function_execute_system_command`) is defined in a way that directly allows for command injection.
    * **Reconnaissance:** Using the agent's "safe" functions to gather intel about the hidden, "unsafe" ones.
* **Setup & Run:**
    1.  `cd ais-hidden-feelings`
    2.  `sh setup.sh` (This will install dependencies and download the model the .gguf file)
    3.  `source venv/bin/activate`
    4.  `python3 app.py`
    5.  Access the challenge at `http://localhost:5000` (or the port you configure).

---

### Lab 02: The Ghost in the Prompt

* **Vulnerability:** `OWASP LLM Top 10: LLM01 - Prompt Injection` (Specifically: Invisible Prompt Injection)
* **Scenario:** "The Devil is in the details, and the details are in the pauses."
* **Objective:** Your mission is to move stealthily, bypassing a filter by embedding a hidden payload, to find the flag.
* **Key Concepts Demonstrated:**
    * **Invisible Prompt Injection:** Using non-printable characters, Unicode, or other "invisible" text to hide instructions from human reviewers and simple filters.
    * **Tokenizer Ambiguity:** Exploiting the difference between how a human *sees* a prompt and how the LLM's *tokenizer* *reads* it.
* **Setup & Run:**
    1.  `cd ghost-in-the-prompt`
    2.  `(Add setup instructions here, e.g., docker-compose up or python3 app.py)`
    3.  [cite_start]Access the challenge at `http://localhost:6006`.

---

### (Coming Soon) Lab 03: The Leaky Context

* **Vulnerability:** `OWASP LLM Top 10: LLM06 - Sensitive Information Disclosure`
* **Objective:** Tease sensitive data (API keys, user PII) out of the LLM's context window, which has been "poisoned" with data from other users.

---

## 🤝 How to Contribute

I am actively looking to collaborate with others in this field. If you have an idea for a new vulnerable lab, find a new attack vector, or want to improve an existing challenge, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/new-lab`).
3.  Submit a Pull Request with a clear description of your changes.

## Connect With Me

Let's talk about AI security, red teaming, and building (and breaking) the next generation of AI applications.

* **LinkedIn:** `https://www.linkedin.com/in/jaidanmaity/`
* **E-Mail:** `thejaidanmaity@gmail.com`
