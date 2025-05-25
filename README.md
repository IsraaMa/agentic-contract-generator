# Contract Automated Generator (CAG)

Automated contract generation using LLMs, retrieval, and agentic workflows.

## Overview

**CAG** (Contract Automated Generator) is a Python-based system for generating, validating, and finalizing contracts using large language models (LLMs), retrieval-augmented generation, and agentic workflows. It leverages LangChain, LangGraph, and vector search to automate the contract lifecycle, including human-in-the-loop validation and memory.

## Features

- **Automated contract drafting** using LLMs
- **Retrieval-augmented generation** with FAISS vectorstore
- **Agentic workflow orchestration** via LangGraph
- **Human-in-the-loop** and LLM-based validation steps
- **Extensible agent architecture** for custom contract flows

## Project Structure

```
cag/
  agents/           # Agent implementations (graph, contract generation, validation, etc.)
  schemas.py        # Shared state schema for contract workflow
scripts/
  run_contract_graph.py      # Main entry point for contract generation
  export_to_vectorstore.py   # Utility to build the vectorstore from contract data
data/               # (Ignored) Place your contract data here
vectorstore/        # (Ignored) Vectorstore index files
```

## Installation

1. **Clone the repository** and install dependencies (requires Python 3.11+):

   ```bash
   git clone <repo-url>
   cd agentic-contract-generator
   poetry install
   ```

2. **Set up environment variables**:

   - Create a `.env` file in the root directory.
   - Add your OpenAI API key and any other required variables:

     ```
     OPENAI_API_KEY=sk-...
     ```

## Usage

### 1. Prepare the Vectorstore

Before generating contracts, index your contract data for retrieval:

```bash
python scripts/export_to_vectorstore.py
```

- Place your contract documents (PDF, DOCX, etc.) in `data/contracts/`.

### 2. Generate a Contract

Prepare an input JSON file describing the contract requirements. Example (`data/input_example.json`):

```json
{
  "datos_trabajador": {
    "nombre_completo": "Juan Pérez García",
    "nacionalidad": "Mexicana",
    "edad": 30,
    "sexo": "Masculino",
    "estado_civil": "Soltero",
    "curp": "PEGA900101HDFRRN09",
    "rfc": "PEGA900101XXX",
    "domicilio": "Calle Falsa 123, Ciudad de México"
  },
  "datos_patron": {
    "razon_social": "Empresa Ejemplo S.A. de C.V.",
    "rfc": "EES900101XXX",
    "domicilio": "Avenida Siempre Viva 742, Ciudad de México",
    "representante_legal": "María López Torres"
  },
  "condiciones_trabajo": {
    "tipo_contrato": "Indeterminado",
    "puesto": "Desarrollador de Software",
    "funciones": "Desarrollo y mantenimiento de aplicaciones web.",
    "lugar_trabajo": "Remoto",
    "jornada_laboral": "Tiempo completo",
    "horario": "9:00 a 18:00",
    "salario_mensual": 40000,
    "forma_pago": "Transferencia bancaria",
    "dia_lugar_pago": "Último día hábil de cada mes, en la cuenta bancaria proporcionada",
    "periodo_prueba_dias": 30,
    "capacitacion": "Capacitación inicial de 2 semanas sobre procesos internos."
  }
}
```

Run the contract generation workflow:

```bash
python scripts/run_contract_graph.py data/input_example.json
```

- The script will print the final contract or any validation errors.

## Agents & Workflow

- **Graph-based orchestration**: The workflow is defined as a graph of agents in `cag/agents/graph.py`.
- **Validation steps**: Includes LLM-based and human-in-the-loop validators.
- **Extensible**: Add or modify agents in `cag/agents/` to customize the workflow.

## Development

- Run tests with:

  ```bash
  poetry run pytest
  ```

- See `pyproject.toml` for all dependencies.

## Dependencies

- [LangChain](https://python.langchain.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [OpenAI](https://platform.openai.com/)
- [FastAPI](https://fastapi.tiangolo.com/) (for serving, if needed)
- See `pyproject.toml` for the full list.

## License

MIT

## Using the App with LangGraph Server

This project supports running as a LangGraph server and interacting with it via the API. Here's how to use it:

### 1. Start the LangGraph Server

Make sure your server is running (e.g., with `langgraph server run` or your preferred method).

### 2. Create an Assistant

```bash
curl http://localhost:2024/assistants \
  --request POST \
  --header 'Content-Type: application/json' \
  --data '{
    "graph_id": "main",
    "config": {},
    "metadata": {},
    "if_exists": "do_nothing",
    "name": "My Assistant",
    "description": "Test assistant"
  }'
```
- Save the `assistant_id` from the response.

### 3. Create a Thread

```bash
curl http://localhost:2024/threads \
  --request POST \
  --header 'Content-Type: application/json' \
  --data '{}'
```
- Save the `thread_id` from the response.

### 4. Start a Run on the Thread

Replace `<assistant_id>` and `<thread_id>` with your actual values:

```bash
curl http://localhost:2024/threads/<thread_id>/runs \
  --request POST \
  --header 'Content-Type: application/json' \
  --data '{
    "assistant_id": "<assistant_id>",
    "input": {
      "input_data": {
        "datos_trabajador": {
          "nombre_completo": "Juan Pérez García",
          "nacionalidad": "Mexicana",
          "edad": 30,
          "sexo": "Masculino",
          "estado_civil": "Soltero",
          "curp": "PEGA900101HDFRRN09",
          "rfc": "PEGA900101XXX",
          "domicilio": "Calle Falsa 123, Ciudad de México"
        },
        "datos_patron": {
          "razon_social": "Empresa Ejemplo S.A. de C.V.",
          "rfc": "EES900101XXX",
          "domicilio": "Avenida Siempre Viva 742, Ciudad de México",
          "representante_legal": "María López Torres"
        },
        "condiciones_trabajo": {
          "tipo_contrato": "Indeterminado",
          "puesto": "Desarrollador de Software",
          "funciones": "Desarrollo y mantenimiento de aplicaciones web.",
          "lugar_trabajo": "Remoto",
          "jornada_laboral": "Tiempo completo",
          "horario": "9:00 a 18:00",
          "salario_mensual": 40000,
          "forma_pago": "Transferencia bancaria",
          "dia_lugar_pago": "Último día hábil de cada mes, en la cuenta bancaria proporcionada",
          "periodo_prueba_dias": 30,
          "capacitacion": "Capacitación inicial de 2 semanas sobre procesos internos."
        }
      }
    }
  }'
```

### 5. View Interrupts in Agent Inbox UI

If your run hits a human-in-the-loop interrupt, you will see the thread in the Agent Inbox UI (if connected to the same server).

---