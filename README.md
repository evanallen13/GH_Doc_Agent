# GitHub Documentation Agent

A Retrieval-Augmented Generation (RAG) system that provides intelligent answers to questions about GitHub documentation using local LLMs and vector embeddings.

## Overview

This project creates a question-answering system that:
- Fetches and processes GitHub's official documentation
- Generates embeddings for document chunks using local Ollama models
- Stores embeddings in a PostgreSQL vector database
- Provides contextually relevant answers to GitHub-related questions

## Architecture

The system consists of several key components:

### Core Components

- **`src/llama.py`**: Interface for Ollama LLM operations (text generation and embeddings)
- **`src/postgres_db.py`**: PostgreSQL vector database operations using pgvector
- **`load.ipynb`**: Data loading pipeline that fetches and processes GitHub docs
- **`main.ipynb`**: Query interface for asking questions and getting answers

### Docker Services

The project uses Docker Compose with the following services:
- **Ollama**: Local LLM server for text generation and embeddings
- **PostgreSQL with pgvector**: Vector database for similarity search

## Getting Started

This project is designed to run in a **VS Code Dev Container** with all dependencies and services pre-configured.

### Prerequisites

- Docker and Docker Compose
- VS Code with the Dev Containers extension
- Git

### Installation

#### Option 1: Dev Container (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Dev-Container-Compose
   ```

2. **Open in VS Code**
   ```bash
   code .
   ```

3. **Reopen in Container**
   - VS Code will prompt to "Reopen in Container"
   - Or use Command Palette: `Dev Containers: Reopen in Container`

The dev container will automatically:
- Start all required services (Ollama, PostgreSQL with pgvector)
- Install Python dependencies
- Configure the development environment
- Open `main.ipynb` for immediate use

#### Option 2: Manual Setup

If you prefer to run without dev containers:

1. **Clone and navigate to the repository**
   ```bash
   git clone <repository-url>
   cd Dev-Container-Compose
   ```

2. **Start the services**
   ```bash
   docker-compose -f .devcontainer/docker-compose.yml up -d ollama db
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Note: You'll need to adjust the host configurations in the notebooks to connect to the services.

### Usage

#### 1. Load GitHub Documentation

Run the `load.ipynb` notebook to:
- Clone the GitHub docs repository
- Fetch documentation content via GitHub's API
- Process and chunk documents
- Generate embeddings and store in vector database

Key configuration:
- **Embedding Model**: `granite-embedding:30m` (384 dimensions)
- **Chunk Size**: 5000 characters with 100 character overlap

#### 2. Ask Questions

Use the `main.ipynb` notebook to:
- Submit questions about GitHub features
- Retrieve relevant documentation chunks
- Generate contextual answers using LLM

Example query:
```python
prompt = "How much do github actions cost for linux?"
```

## Configuration

### Environment Variables

- `OLLAMA_HOST`: Ollama server URL (default: `http://ollama:11434`)
- `POSTGRES_HOST`: PostgreSQL server host (default: `vector-postgres`)

### Models

- **Text Generation**: `llama3.2:1b` 
- **Embeddings**: `granite-embedding:30m`

Find more models at [Ollama Library](https://ollama.com/library)

## Project Structure

```
.
├── README.md
├── requirements.txt
├── main.ipynb              # Query interface
├── load.ipynb             # Data loading pipeline
├── AVAILABLE_MODELS.md    # Model documentation
├── src/
│   ├── llama.py          # Ollama LLM interface
│   └── postgres_db.py    # Vector database operations
└── data/                 # GitHub documentation storage
```

## Features

### Data Loading (`load.ipynb`)
- **GitHub Docs Cloning**: Automatically clones the latest GitHub docs repository
- **API Content Fetching**: Retrieves rendered documentation via GitHub's API
- **Document Processing**: Splits documents into manageable chunks for embedding
- **Batch Processing**: Efficiently processes large document collections

### Query System (`main.ipynb`)
- **Semantic Search**: Finds relevant documentation using vector similarity
- **Contextual Answers**: Generates responses using retrieved context
- **Flexible Models**: Easy switching between different Ollama models

### Vector Database
- **pgvector Integration**: Uses PostgreSQL with vector extensions
- **Similarity Search**: Cosine similarity search for document retrieval
- **Scalable Storage**: Handles large document collections efficiently

## Technical Details

### Document Processing Pipeline
1. Clone GitHub docs repository
2. Extract markdown files
3. Fetch rendered content via API
4. Split into 5000-character chunks
5. Generate 384-dimensional embeddings
6. Store in PostgreSQL with pgvector

### Query Processing Pipeline
1. Generate embedding for user question
2. Search for top-k similar document chunks
3. Combine relevant context
4. Generate response using LLM with context

## Performance Considerations

- **Rate Limiting**: API requests are throttled to avoid GitHub rate limits
- **Batch Processing**: Documents are processed in batches with progress tracking
- **Memory Efficiency**: Large documents are chunked to fit model context windows

## Troubleshooting

### Common Issues

1. **Ollama Connection**: Ensure Ollama service is running and accessible
2. **Model Downloads**: First-time model usage requires downloading (may take time)
3. **PostgreSQL**: Verify pgvector extension is installed and enabled
4. **API Rate Limits**: GitHub API has rate limits; increase delays if needed


