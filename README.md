# Paper-2X

Paper2X is an AI-powered tool that leverages Gemini 1.5 Flash and LangGraph, to transform research papers into engaging presentations and audio summaries. The project provides a backend service to process document inputs and convert them into structured PPTs.

## Project Motivation

Understanding and presenting research papers can be time-consuming. Paper2X streamlines this process by automating content extraction, slide creation, and audio generation, making research more accessible to students, educators, and professionals.

Also, this project is a continuation from my team's partial solution for the Research Remix track sponserd by Cactus Communications during the MineD Hackathon 2025, where some features of this project were the expected outcomes.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the API](#running-the-api)
  - [Frontend Integration](#frontend-integration)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

The goal of Paper-2-X is to streamline the creation of presentation slides from academic papers or long-form documents. By combining the power of FastAPI with state-of-the-art language models (via LangChain and its ecosystem), the application parses input documents, extracts key points, and generates a coherent slide deck.

## Features

- **Research Paper to Presentation:** Automatically generates PowerPoint presentations (in .pptx) from academic papers.
    Uses:
    - `PyMuPDFLoader` to extract text and images from the research articles
    -  Gemini 1.5 Flash to generate slides' content for the PPT
    - `pptx` library for creating the PPT from text. Includes support for a few themes, which are created using pptx library itself.
- **Research Paper to Podcast Transcript:** Converts the research paper content into a transcripts for a narrated-like podcast.
- **API Deployment:** This entire LangGraph workflow is deployed as a FastAPI app, and has endpoints to get the specific content (check [Running The API](#running-the-api) section)


## Architecture

The application follows a modular design:
- **API Layer:** Implemented with FastAPI and served using Uvicorn.
- **Processing Agents:** Under the `agents` directory, different agents handle subtasks such as text extraction, summarization, and PPT slide creation.
- **Configuration:** Environment variables (using [python-dotenv](https://pypi.org/project/python-dotenv/)) allow configuration for API keys and other secrets.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/lavanderhoney/paper2x.git
   cd paper2x
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

This project contains an API which serves the langgraph workflow, but not the PPT generation and the podcast. The API is experimental only.

To use the features, run the `agents\workflow_testing.ipynb` notebook.

### Running the API

```bash
uvicorn app.main:app --reload
```
Access the API at `http://127.0.0.1:8000/docs`

#### Endpoints
You can test these endpoints using Postman (as there's no front-end, yet).
- `POST /generate_ppt`
    - Upload the research paper as a form data in the body of POST request in the Postman API interface.
    - This will execute the langgraph workflow, and return a `file_id`. Save this id, as it will be required for further GET requests.
- `GET/ppt/{file_id}`
    - Hitting this endpoint, using the `file_id` obtained from the POST request, will return the textual contents for creating the PPT 
- `GET/summary/{file_id}`
    - Returns the summary of the research paper, in a form useful for generating the podcast transcript.
- `GET/convo/{file_id}`
    - Returns the transcript of the podcast, in a JSON containing lists of dialagoues of two personas: Katherine, and Clay, and a list specifying the order of their dialogues. The datamodel is specified in the `agents\agent.py` as the `Conversation` class.

**NOTE**: The purpose behind using the `file_id` thing, is to have a way to store the graph's state in-memory of the API. This violates the property of RESTful API being stateless, but I've implemented this as a temporary way to circumvent executing the graph mutliple times by the same user.

## File Structure
```
📂 paper2x
├── agents
│   ├── extracted_images # Stores the images extracted from the pdf
│   ├── static # For storing the generated ppts
│   ├── uploaded_pds # Research papers to be used
│   ├── agent.py        # Python script for the agentic workflow
│   ├── app2.py  # FastAPI app entry point
│   └── workflow_testing.ipynb # Jupyter notebook for agentic workflow testing
├── requirements.txt
└── README.md
```

## Configuration

Create a `.env` file and add the following keys:

```dotenv
GOOGLE_API_KEY=your_gemini_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_ENDPOINT=your_langsmith_endpoint
LANGSMITH_PROJECT=paper2x_project
LANGSMITH_TRACING=true
```

## Dependencies

The project depends on a number of Python packages:

- **Backend & API:**
  - `fastapi`
  - `uvicorn`
- **AI Agents:**
  - `langchain`
  - `langgraph`
  - `langchain_google_genai`
  - `langchain_core`
- **Utilities:**
  - `pydantic`
  - `python-dotenv`
  - `python-multipart`
  - `PyMuPDF`
  - `typing-extensions`
  - `uuid`

See [requirements.txt](https://github.com/lavanderhoney/paper2x/blob/main/requirements.txt) for the complete list.

## Contributing

Contributions are welcome! If you’d like to help improve Paper-2-X:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Open a pull request detailing your changes.

Please follow the existing code style and include tests for new functionality.

## Contact

For questions, suggestions, or contributions, please open an issue on GitHub or contact the repository owner at your preferred communication channel.
