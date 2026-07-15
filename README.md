# AI Robot - Local Assistant with Dynamic Memory (RAG)

This is a local intelligent assistant designed to run on a Virtual Machine (VM) or a Raspberry Pi. It leverages a local Large Language Model (**Qwen 2.5** - for now) and a vector database (**ChromaDB**) to store, search, and recall facts shared by the user during real-time conversations.

---

## 🛠️ Tech Stack

* **Python 3.12+**
* **Ollama** (for running local models)
  * LLM: `qwen2.5:1.5b` (temporaly)
  * Embeddings: `nomic-embed-text` (temporaly)
* **LangChain** (RAG orchestration)
* **ChromaDB** (Vector database for local memory persistence)

---

## 🚀 How to Run Locally

Follow these steps to set up your environment and run the assistant on your machine.

### 1. Set Up the Ollama Server
Make sure Ollama is installed and running on your system, and that you have downloaded both required models:

# Download the Large Language Model (LLM)
ollama pull qwen2.5:1.5b

# Download the dedicated Embeddings model
ollama pull nomic-embed-text


### 2. Set Up Local Environment

Open a terminal in your VM and run the following commands:

# 1. Navigate to the project directory
cd ~/robo_ia

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Ensure all dependencies are installed
pip install -r requirements.txt


### 2. Run the model

With your virtual environment active, run the main script:

python3 main.py
