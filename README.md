# 🤖 Blog Generation Agentic AI

An end-to-end **Agentic AI** application that generates structured, SEO-friendly blog posts on any topic — with optional multilingual translation — powered by **LangGraph**, **LangChain**, **Groq LLM**, and served via a **FastAPI** REST API. Supports visual graph debugging through **LangGraph Studio**.

---

## 🧠 How It Works

The application uses a **stateful LangGraph pipeline** with two modes:

1. **Topic-only mode** — Generates a blog title and content for a given topic.
2. **Topic + Language mode** — Does everything above, then conditionally routes to a language-specific translation node (Hindi, French, or Spanish).

The graph is built around a `BlogState` TypedDict and each step (title creation, content generation, translation) is an independent node, making the workflow modular and easy to extend.

---

## 📁 Project Structure

```
Blog-Generation-Agentic-AI/
│
├── app.py                    # FastAPI application entry point
├── main.py                   # Project entry point (uv managed)
├── langgraph.json            # LangGraph Studio configuration
├── request.json              # Sample API request payload
├── pyproject.toml            # Project metadata and dependencies (uv)
├── requirements.txt          # pip-compatible dependencies
├── .env                      # Environment variables (not committed)
├── .python-version           # Python version pin
├── .gitignore
│
└── src/
    ├── graphs/
    │   └── graph_builder.py  # LangGraph graph construction & compilation
    ├── llms/
    │   └── groqllm.py        # Groq LLM initialization wrapper
    ├── states/
    │   └── blogstate.py      # BlogState TypedDict & Blog Pydantic model
    └── node/
        └── blog_node.py      # Node logic: title, content, translation, routing
```

---

## 🔁 Graph Architecture

### Topic-Only Graph

```
START → title_creation → content_generation → END
```

### Topic + Language Graph

```
START → title_creation → content_generation → route
                                                  ├─(hindi)──→ hindi_translation → END
                                                  ├─(french)─→ french_translation → END
                                                  └─(spanish)→ spanish_translation → END
```

---

## ⚙️ Tech Stack

| Component        | Technology                                                                     |
| ---------------- | ------------------------------------------------------------------------------ |
| LLM Provider     | [Groq](https://groq.com/) (`openai/gpt-oss-120b`)                              |
| Orchestration    | [LangGraph](https://github.com/langchain-ai/langgraph)                         |
| LLM Framework    | [LangChain](https://www.langchain.com/)                                        |
| API Server       | [FastAPI](https://fastapi.tiangolo.com/) |
| Package Manager  | [uv](https://github.com/astral-sh/uv)                                          |
| Observability    | [LangSmith](https://smith.langchain.com/)                                      |
| Studio Debugging | [LangGraph Dev Studio](https://docs.langchain.com/langgraph/studio)            |
| Python Version   | 3.13+                                                                          |

---

## 🚀 Getting Started

### 1. Install `uv` (recommended)

```bash
pip install uv
```

### 2. Initialize and create a virtual environment

```bash
uv init
uv venv
```

Activate the virtual environment:

- **Windows:** `.venv\Scripts\activate`
- **macOS/Linux:** `source .venv/bin/activate`

### 3. Install dependencies

```bash
uv add langchain langgraph langchain-groq langchain-community langchain-classic fastapi uvicorn python-dotenv watchdog langchain-cli
```

Or using pip:

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
```

---

## ▶️ Running the Application

### Start the FastAPI server

```bash
python app.py
```

The server will start at `http://127.0.0.1:8000`.

---

## 📬 API Usage

### Endpoint

```
POST http://127.0.0.1:8000/blogs
```

### Request Body — Topic + Language

```json
{
  "topic": "Agentic AI",
  "language": "hindi"
}
```

Supported languages: `hindi`, `french`, `spanish`

### Sample Response

```json
{
  "data": {
    "topic": "Agentic AI",
    "blog": {
      "title": "# The Rise of Agentic AI: ...",
      "content": "## Introduction\n\nAgentic AI refers to..."
    },
    "current_language": "hindi"
  }
}
```

---

## 🖥️ LangGraph Studio (Visual Debugging)

LangGraph Studio allows you to visually inspect, run, and debug your graph.

### Start the dev server

```bash
langgraph dev
```

> **Note:** Run both `python app.py` and `langgraph dev` simultaneously for full functionality.

The `langgraph.json` configuration file points Studio to the compiled graph:

```json
{
  "dependencies": ["."],
  "graphs": {
    "blog_generator_agent": "./src/graphs/graph_builder.py:graph"
  },
  "env": "./.env"
}
```

- `"dependencies": ["."]` — refers to the current project directory
- `"graphs"` — maps the agent name to the compiled `graph` object exported from `graph_builder.py`

---

## 🧩 Module Overview

### `src/states/blogstate.py`

Defines the shared state passed across all graph nodes.

```python
class Blog(BaseModel):
    title: str
    content: str

class BlogState(TypedDict):
    topic: str
    blog: Blog
    current_language: str
```

### `src/llms/groqllm.py`

Initializes and returns a `ChatGroq` LLM instance using the API key from `.env`.

### `src/node/blog_node.py`

Contains all node logic:

- `title_creation` — Prompts the LLM to generate a creative, SEO-friendly title
- `content_generation` — Generates detailed Markdown blog content
- `translation` — Translates content into the specified language, preserving tone and formatting
- `route` / `route_decision` — Reads `current_language` from state and routes to the correct translation node

### `src/graphs/graph_builder.py`

Constructs and compiles LangGraph `StateGraph` instances:

- `build_topic_graph()` — Linear graph for topic-only generation
- `building_language_graph()` — Extended graph with conditional routing for translation
- `setup_graph(usecase)` — Entry point used by `app.py` to select the right graph

---

## 🧪 Testing with Postman

1. Set method to `POST`
2. URL: `http://127.0.0.1:8000/blogs`
3. Set `Body > raw > JSON` and paste:

```json
{
  "topic": "Agentic AI",
  "language": "hindi"
}
```

---

## 📌 Notes

- All blog content is generated in **Markdown format** for easy rendering.
- The translation nodes adapt cultural references and idioms, not just raw text.
- The `langgraph.json` `graph` export at the bottom of `graph_builder.py` is specifically for LangGraph Studio and runs the language graph by default.

---

## 📄 License

This project is open-source and available for educational and development purposes.
