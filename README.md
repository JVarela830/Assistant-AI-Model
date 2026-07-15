# AI Robot - Local Assistant with Dynamic Memory (RAG)

This is a local intelligent assistant designed to run on a Virtual Machine (VM - Ubuntu Server 24.04.4) or a Raspberry Pi. It leverages a local Large Language Model (**Qwen 2.5** - for now) and a vector database (**ChromaDB**) to store, search, and recall facts shared by the user during real-time conversations.

---

## 🛠️ Tech Stack

* **Python 3.12+**
* **Ollama** (for running local models)
  * LLM: `ollama pull qwen2.5:3b` (temporaly)
  * Embeddings: `nomic-embed-text` (temporaly)
* **LangChain** (RAG orchestration)
* **ChromaDB** (Vector database for local memory persistence)

---

## 🧠 Intelligent Routing System (How it Works) - (Early Architecture)

Unlike standard RAG systems that query everything simultaneously (clogging the RAM of a Raspberry Pi), this assistant uses a **Zero-Shot Intent Classifier** before processing any query:

```
                  [ User Input ]
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
      [ Intent Classifier (Qwen 2.5:3b) ]
      /                 │                 \
     /                  │                  \
(INTERNET)             (MEMORY)            (CASUAL)
    ▼                     ▼                    ▼
[Web Search RAG]    [ChromaDB Retrieval]   [Direct Response]
(Live & Hist.)       (Personal Facts)      (No context needed)
```

1. **INTERNET:** Triggered for general knowledge, sports, weather, or history (e.g., *"When did the World War II start?"*). It automatically generates keyword-optimized search queries.
2. **MEMORY:** Triggered for personal questions (e.g., *"What is my dog's name?"*). It queries ChromaDB. If the user makes an assertive statement (e.g., *"My favorite color is blue"*), it **automatically saves** it as a new memory.
3. **CASUAL:** For greetings and small talk, saving computation power and bypassing all database queries.

---

## 🚀 How to Run Locally

Follow these steps to set up your environment and run the assistant on your machine.

If you are working with the VM, you can open a terminal in your PC to interact easier with the terminal of the server:
```bash
ssh robot@192.168.1.195 (or the IP that the VM gets)
```


# 1. Set Up the Ollama Server
Make sure Ollama is installed and running on your system, and that you have downloaded both required models:

## Download the Large Language Model (LLM)
```bash
ollama pull qwen2.5:3b
```

## Download the dedicated Embeddings model
```bash
ollama pull nomic-embed-text
```

# 2. Set Up Local Environment

Open a terminal in your VM and run the following commands:

## 1. Navigate to the project directory
```bash
cd ~/robo_ia
```

## 2. Activate the virtual environment
```bash
source venv/bin/activate
```

## 3. Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

# 3. Run the model

With your virtual environment active, run the main script:

```bash
python3 main.py
```
