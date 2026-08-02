# 💻 AI Coding Tutor

An intelligent AI-powered Coding Tutor built using **LangGraph**, **LangChain**, **Ollama**, **ChromaDB**, **LangSmith**, and **Streamlit**. The application helps users solve Data Structures & Algorithms (DSA) problems by generating optimized C++ solutions, explaining the approach, analyzing complexity, and providing an interactive AI tutor for follow-up questions.

---

## 🚀 Features

* 🧠 **AI Problem Understanding**

  * Explains the problem in simple language.
  * Describes the goal, inputs, outputs, and algorithm.

* 💻 **Optimal C++ Code Generation**

  * Generates clean and optimized C++17 solutions.
  * Produces code without unnecessary explanations.

* 📈 **Complexity Analysis**

  * Calculates Time Complexity.
  * Calculates Space Complexity.
  * Explains the reasoning behind the analysis.

* 🤖 **Interactive AI Coding Tutor**

  * Ask unlimited follow-up questions.
  * Request line-by-line code explanations.
  * Understand algorithms with examples.
  * Get debugging assistance.
  * Learn optimization techniques.

* 💾 **Persistent Chat Memory**

  * Stores tutor conversations using ChromaDB.
  * Session-based memory.
  * Resume previous discussions anytime.

* 📚 **Session Management**

  * Automatically saves coding sessions.
  * Displays previous sessions in the sidebar.
  * Reloads previous solutions and conversations.

* 🔍 **LangSmith Observability**

  * Tracks every LangGraph node.
  * Monitors tutor interactions.
  * Provides end-to-end execution traces.

* 🎨 **Modern Streamlit Interface**

  * Clean and responsive UI.
  * Code highlighting.
  * Download generated solutions.
  * Interactive chat interface.

---

# 🏗️ Architecture

```text
                  User
                    │
                    ▼
          Streamlit Frontend
                    │
                    ▼
          LangGraph Workflow
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
 Explain Problem  Generate Code  Analyze Complexity
        │           │           │
        └───────────┴───────────┘
                    │
                    ▼
           AI Coding Tutor
                    │
         Session Memory (ChromaDB)
                    │
                    ▼
               LangSmith Tracing
```

---

# 🛠️ Tech Stack

| Category        | Technologies                       |
| --------------- | ---------------------------------- |
| Language        | Python                             |
| LLM             | Ollama (Phi-3 / Llama 3 / Mistral) |
| Agent Framework | LangGraph                          |
| LLM Framework   | LangChain                          |
| Memory          | ChromaDB                           |
| Observability   | LangSmith                          |
| Frontend        | Streamlit                          |
| Environment     | Python Virtual Environment         |

---

# 📂 Project Structure

```text
AI-Coding-Tutor/
│
├── frontend.py          # Streamlit UI
├── backend.py           # LangGraph workflow
├── tutor.py             # AI Tutor
├── memory.py            # ChromaDB memory manager
├── requirements.txt
├── .env
├── chroma_db/
└── README.md
```

---

# ⚙️ LangGraph Workflow

The workflow consists of three AI nodes:

### 1. Explain Problem

* Understands the problem statement.
* Produces a beginner-friendly explanation.

### 2. Generate Code

* Creates an optimal C++17 solution.
* Uses the most efficient algorithm.

### 3. Analyze Complexity

* Calculates time complexity.
* Calculates space complexity.
* Explains the reasoning.

---

# 🤖 AI Tutor

After generating a solution, users can continue learning through an interactive AI tutor.

The tutor can:

* Explain algorithms.
* Explain code line by line.
* Solve doubts.
* Help debug code.
* Suggest optimizations.
* Maintain context across the conversation.

---

# 💾 Memory System

The project uses **ChromaDB** for persistent storage.

It stores:

* User questions
* AI responses
* Session IDs
* Timestamps
* Problem titles
* Generated solutions

Users can revisit any previous session from the sidebar.

---

# 📊 LangSmith Tracing

The project integrates LangSmith for observability.

Each execution traces:

* LangGraph workflow
* Explain Problem node
* Generate Code node
* Complexity Analysis node
* Tutor interactions
* Memory operations

This makes debugging and monitoring AI workflows significantly easier.

---

# ▶️ Installation

## Clone the repository

```bash
git clone https://github.com/your-username/AI-Coding-Tutor.git
cd AI-Coding-Tutor
```

## Create a virtual environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Install and run Ollama

Install Ollama from the official website and pull your preferred model:

```bash
ollama pull phi3
```

or

```bash
ollama pull llama3
```

or

```bash
ollama pull mistral
```

Start the Ollama server:

```bash
ollama serve
```

## Configure environment variables

Create a `.env` file:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=YOUR_LANGSMITH_API_KEY
LANGCHAIN_PROJECT=AI-Coding-Tutor
```

## Run the application

```bash
streamlit run frontend.py
```

---

# 📸 Screenshots

Add screenshots here:

* Home Page
* Solution Generation
* Code Output
* Complexity Analysis
* AI Tutor Chat
* LangSmith Traces

---

# 🌟 Future Enhancements

* Multi-Agent architecture
* Automatic code execution
* Test case generation
* Debugging agent
* Code review agent
* Multi-language support
* Docker deployment
* FastAPI backend
* User authentication
* Cloud deployment
* Leaderboard and coding history
* Retrieval-Augmented Generation (RAG) for documentation support

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Vedant Agnihotri**

If you found this project helpful, consider giving it a ⭐ on GitHub.
