# AI Robot - Local Multimodal Assistant with Dynamic Memory (RAG)

A local intelligent assistant designed to run on resource-constrained environments such as a Virtual Machine (Ubuntu Server 24.04.4) or a Raspberry Pi.

The project combines a local Large Language Model (**Qwen 2.5** for now), **Retrieval-Augmented Generation (RAG)**, and a persistent vector database (**ChromaDB**) to create an assistant capable of:

* Answering general knowledge questions using web retrieval.
* Storing and recalling personal information shared by the user.
* Running completely locally without relying on external LLM APIs.
* Evolving toward a multimodal assistant with vision and voice capabilities.

---

# 🛠️ Tech Stack

## Core

* **Python 3.12+**
* **Ollama** - Local model execution
* **LangChain** - LLM orchestration and RAG pipeline management
* **ChromaDB** - Persistent vector database for user memory

## Current Models
* **qwen2.5:3b**

### Large Language Model

```bash
ollama pull qwen2.5:3b
```

Used for:

* Query classification.
* Search query optimization.
* Final response generation.

*(Temporary model selection. Future versions may use different local models depending on hardware constraints.)*

### Embeddings Model

```bash
ollama pull nomic-embed-text
```

Used for:

* Converting user memories into vector embeddings.
* Similarity search inside ChromaDB.

---

# 🧠 Current Architecture

The assistant uses an intelligent routing system before generating responses.

Instead of sending every request through the same retrieval pipeline, the system first performs **zero-shot intent classification using a local LLM**.

The classifier determines whether the user request requires:

* Web knowledge.
* Personal memory retrieval.
* No external context.

```
                    [ User Input ]
                          |
                          v
          [ Zero-Shot Intent Classification ]
                    (Qwen 2.5)
                          |
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼

 [WEB KNOWLEDGE]   [PERSONAL MEMORY]   [NO RETRIEVAL]

        ▼                 ▼                 ▼

 Web Search RAG     ChromaDB RAG       Direct LLM
 (External Data)    (User Facts)       Conversation

        └─────────────────┼─────────────────┘
                          |
                          v

                 [ Context + User Query ]

                          |
                          v

                    [ LLM Response ]
```

---

# 🔎 Retrieval-Augmented Generation (RAG)

The assistant uses RAG to provide the language model with relevant information before generating an answer.

The basic flow:

```
User Question
      |
      v
Retrieve Relevant Information
      |
      v
Add Context to Prompt
      |
      v
Generate Answer
```

The project currently uses two retrieval sources.

---

## 🌐 Web Search RAG

Used for:

* History.
* Sports.
* Weather. (not functional yet)
* Current events.
* General knowledge.

Before searching, the assistant performs query optimization:

Example:

```
User:
"Who won Euro 2004?"

Generated Search Query:
"Euro 2004 final winner"
```

This improves the quality of retrieved information.

Pipeline:

```
User Question
      |
      v
Query Optimization (LLM)
      |
      v
DuckDuckGo Search
      |
      v
Search Context
      |
      v
LLM Response
```

---

## 🧠 Personal Memory RAG

Used for user-specific information:

Examples:

```
"What is my dog's name?"

"What is my favorite color?"
```

The assistant stores user information as vector documents:

```
User Fact
    |
    v
Embedding Model
    |
    v
ChromaDB
    |
    v
Similarity Search
    |
    v
Relevant Memory
    |
    v
LLM Response
```

Example:

User:

```
"My favorite color is blue."
```

The assistant stores this information and can later retrieve it when needed.

---

# 🤖 Agentic RAG (Future Architecture)

The current version uses an intelligent router that selects the appropriate retrieval path.

The next evolution is moving toward an **Agentic RAG architecture**, where the LLM becomes responsible for deciding which tools and knowledge sources are required.

Current architecture:

```
User
 |
Intent Classifier
 |
+--------------+
|              |
Web Search   Memory
 |
LLM Response
```

Future Agentic RAG architecture:

```
                    [ User Input ]

                          |

                          v

                    [ LLM Agent ]

                          |

        ┌─────────────────┼─────────────────┐

        ▼                 ▼                 ▼

 [Memory Tool]     [Web Search Tool]   [Vision Tool]

        |                 |                 |

        └─────────────────┼─────────────────┘

                          |

                          v

                 [ Context Aggregation ]

                          |

                          v

                    [ Final Answer ]
```

The agent will be able to:

* Decide which tools are necessary.
* Search external information when required.
* Retrieve personal memories.
* Analyze images.
* Combine multiple sources before answering.

---

# 👁️ Future Multimodal Capabilities

The long-term goal is to transform this project into a local multimodal assistant.

## Vision Integration

Planned pipeline:

```
Camera / Image Input
        |
        v
     OpenCV
        |
        v
 Vision Language Model
        |
        v
 Image Understanding
        |
        v
 Main Assistant
```

Possible capabilities:

* Image analysis.
* Object recognition.
* Camera-based interaction.
* Visual question answering.

OpenCV will handle image processing and preparation, while a vision-capable LLM will handle understanding.

---

## Voice Interaction

Planned voice pipeline:

### Input

```
Microphone
     |
     v
Speech-to-Text Model
     |
     v
Assistant Pipeline
     |
     v
Response Generation
```

### Output

```
Generated Text
      |
      v
Text-to-Speech Model
      |
      v
Speaker Output
```

The goal is a complete hands-free interaction system.

---

# 🚀 How to Run Locally

## 1. Install and Start Ollama

Make sure Ollama is installed and running.

Download the required models:

### Language Model

```bash
ollama pull qwen2.5:3b
```

### Embeddings Model

```bash
ollama pull nomic-embed-text
```

---

## 2. Setup Environment

Navigate to the project directory:

```bash
cd ~/robo_ia
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Run the Assistant

With the virtual environment active:

```bash
python3 main.py
```

---

# 🗺️ Roadmap

## Completed

* [x] Local LLM inference with Ollama.
* [x] Persistent ChromaDB memory.
* [x] RAG-based personal memory retrieval.
* [x] Web search retrieval.
* [x] Intelligent query routing.
* [x] Streaming responses.

## Planned

* [ ] Agentic RAG architecture.
* [ ] Tool selection by LLM reasoning.
* [ ] Vision model integration.
* [ ] Camera interaction.
* [ ] Speech-to-text interaction.
* [ ] Text-to-speech responses.
* [ ] Raspberry Pi optimization.
* [ ] Improved memory extraction and management.

---

# Project Vision

The goal of this project is to create a fully local personal AI assistant capable of understanding, remembering, seeing, and interacting with the user while maintaining privacy by running locally whenever possible.
