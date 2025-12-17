⚡ Advanced Code Editor & Runner
A sleek, high-performance web-based environment designed for rapid prototyping and code execution. This tool provides a seamless experience for developers to test snippets across multiple environments without local setup.

🚀 Key Features
Polyglot Support: Native execution for Python, JavaScript (Node.js), C, C++, Java, and Bash.

Professional Editor: Powered by streamlit-ace for high-fidelity syntax highlighting and code formatting.

Flexible Inputs: Support for manual coding, drag-and-drop file uploads (up to 200MB), and sample code loading.

Advanced Control: Granular runner settings including execution timeouts and stderr toggling.

Instant Feedback: Real-time execution status and a dedicated output console.

📸 Interface Preview
1. Multilingual Environment
The sidebar allows for quick switching between languages, instantly updating the execution environment.<br><img width="1904" height="943" alt="Screenshot 2025-12-17 150136" src="https://github.com/user-attachments/assets/710d09f1-ed61-49df-940c-bf42b41e0f7d" />

2. Execution Settings & Output
Fine-tune your runtime parameters and view live output in the integrated terminal. <br> <img width="1909" height="945" alt="Screenshot 2025-12-17 150113" src="https://github.com/user-attachments/assets/fbd0cc7b-9186-451f-89fd-4c208fd9a6d8" />

🛠️ Technology Stack
Frontend: Streamlit


Code Editor: Streamlit Ace (Ace Editor)

Runtime: Subprocess-based execution for local compiled and interpreted languages.

⚠️ Security & Safety
Important: This application executes arbitrary code on the host machine.

Environment: It is strictly recommended to run this within a Docker container or a Sandboxed environment.

Limits: While the app supports timeouts, runtime resource limits (CPU/RAM) are not strictly enforced by default.

📥 Installation & Usage
Clone the repository:

Bash

git clone this repository 
cd this-repo-name
Install dependencies:

Bash

pip install -r requirements.txt
Launch the Editor:

Bash

streamlit run app.py
