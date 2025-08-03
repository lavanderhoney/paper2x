Of course\! Here is an updated README for your Paper2X project, reflecting the current structure and functionality based on the files you've provided.

-----

# Paper2X: AI-Powered Research Paper Transformer

Paper2X is an intelligent tool designed to make academic research more accessible and engaging. By leveraging Large Language Models with a sophisticated agentic workflow built on LangGraph, it transforms dense research papers into two digestible formats: professional PowerPoint presentations and conversational audio podcasts.

The project is built with a decoupled frontend-backend architecture, featuring a Streamlit web interface and a FastAPI backend, making it scalable and easy to use.

A basic e-mail based authentication is setup using Appwrite. It only performs login/sign-up, and doesn't yet store/cache any data for user. That's an upcoming feature.

----
## Live Demo
You can try Paper2X live here:

➡️ [Paper2X on Streamlit](https://lavanderhoney-paper2x.streamlit.app/)

Important Note: The backend is deployed on Render's free tier. If the application is not active, the backend service may take a minute or two to spin up. If you encounter an error on the first try, please wait a moment and then reload the page.

----
## Project Motivation

Comprehending and disseminating research findings is often a time-consuming and challenging task for students, educators, and professionals alike. Paper2X was created to streamline this process by automating the creation of high-quality presentation materials and audio summaries. This not only saves significant time but also helps in making complex information more accessible to a broader audience.

This project is also a continuation of a solution developed for the Research Remix track sponsored by Cactus Communications during the MineD Hackathon 2025.

## Table of Contents

  - [Features](#features)
  - [Architecture](#architecture)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Contributing](#contributing)
  - [License](#license)

## Features

  - **Automated Presentation Generation**: Upload a research paper in PDF format and receive a well-structured PowerPoint (`.pptx`) presentation.
      - Extracts text and images automatically from the PDF document.
      - Intelligently generates slide content, including titles, bullet points, and speaker notes for key sections like Introduction, Methods, Results, and Conclusion.
      - Identifies and embeds relevant figures and tables from the paper into a dedicated "Graphics" slide.
      - Offers multiple presentation themes (`modern`, `vintage`, `corporate`, etc.) for aesthetic customization.
  - **Automated Podcast Generation**: Converts the research paper into an engaging, conversational audio podcast.
      - Generates a summary of the paper tailored for a conversational format.
      - Creates a podcast script with two personas, "Katherine" (the expert) and "Clay" (the inquirer), to explain the paper's concepts in an easy-to-understand dialogue.
      - Uses a Text-to-Speech service (Murf AI) to generate high-quality audio clips for each line of dialogue.
      - Stitches the audio clips together into a final MP3 file, complete with pauses between speakers.
  - **Web Interface**: A user-friendly frontend built with Streamlit allows for easy file uploads, option selection (PPT or Podcast), and downloading of the final output.
  - **Agentic Backend**: The core logic is powered by an agentic workflow using LangGraph, which orchestrates multiple steps like PDF parsing, content generation, and file creation in a robust and stateful manner.
  - **User Authentication**: The frontend includes a simple login and registration system to manage user access with Appwrite.

## Architecture

The application is split into a frontend and a backend, which can be run independently.

1.  **Frontend (`frontend/app.py`)**:

      * A **Streamlit** application provides the user interface.
      * Handles user authentication, file uploads, and interaction with the backend API.
      * It allows users to upload a PDF, choose between generating a presentation or a podcast, and then download the resulting file.

2.  **Backend (`backend/app2.py`)**:

      * A **FastAPI** server exposes an API endpoint (`/generate`) to handle file processing requests.
      * It receives the PDF and a flag indicating whether to create a PPT or a podcast.
      * The core logic resides in an agentic workflow (`backend/agent.py`).

3.  **Agentic Workflow (`backend/agent.py`)**:

      * Built using **LangGraph**, it defines a stateful graph that processes the research paper.
      * **State (`ResPaperExtractState`)**: A Pydantic model holds the data as it flows through the graph, including the PDF path, extracted text/images, generated content, and final file paths.
      * **Nodes**: Each step in the process is a node in the graph:
          * `load_pdf`: Extracts text and images from the uploaded PDF using `PyMuPDF`.
          * `get_data`: (For PPTs) Calls a Large Language Model (LLM) to generate structured JSON content for the presentation slides. It then uses the `python-pptx` library to create the `.pptx` file.
          * `generate_summary`: (For Podcasts) Calls the LLM to create a conversational summary of the paper.
          * `generate_conversation`: Uses the summary to generate a two-person dialogue script. It then calls utility functions in `podcast_utils.py` to convert the script to an audio file.
      * **Conditional Edges**: The graph uses a conditional edge (`check_ppt`) to decide which path to take (PPT or Podcast) based on the user's request.

## Project Structure

The repository is organized into distinct backend and frontend directories, as shown in the file `image_fe7a2d.png`.

```
📂 paper2x/
├── 📄 LICENSE.md
├── 📄 README.md
├── 📄 todo.md
├── 📂 backend/
│   ├── 📄 agent.py              # Core LangGraph agentic workflow
│   ├── 📄 app2.py               # FastAPI application
│   ├── 📄 podcast_utils.py      # Utilities for podcast generation
│   ├── 📄 ppt_utils.py          # Utilities for PPT generation
│   ├── 📄 requirements.txt
│   ├── 📄 test_convo.json       # Sample conversation output
│   ├── 📄 workflow_testing.ipynb # Notebook for testing the agent
│   ├── 📂 extracted_images/    # Stores images extracted from PDFs
│   ├── 📂 static/               # Stores generated PPT files
│   └── 📂 uploaded_pdfs/       # Stores uploaded PDF files
└── 📂 frontend/
    ├── 📄 app.py                # Streamlit frontend application
    └── 📄 requirements.txt
```

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/lavanderhoney/paper2x.git
    cd paper2x
    ```

2.  **Set up the Backend:**

    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3.  **Set up the Frontend:**

    ```bash
    cd ../frontend
    pip install -r requirements.txt
    ```

## Usage

1.  **Configure Environment Variables**: Create a `.env` file in the `backend` directory and add your API keys. See the [Configuration](#configuration) section for details.

2.  **Run the Backend Server**:
    From the `backend` directory, run:

    ```bash
    uvicorn app2:app --reload
    ```

    The API will be available at `http://127.0.0.1:8000`.

3.  **Run the Frontend Application**:
    From the `frontend` directory, run:

    ```bash
    streamlit run app.py
    ```

    The web interface will open in your browser. You can register a new account or log in, then upload a PDF to generate a presentation or podcast.

## Configuration

Create a `.env` file in the `backend/` directory with the following keys:

```dotenv
# For Google Generative AI
GOOGLE_API_KEY="your_google_api_key"

# For Murf AI (Text-to-Speech)
MURF_API_KEY="your_murf_api_key"

# For LangSmith (Optional, for tracing)
LANGSMITH_API_KEY="your_langsmith_api_key"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_PROJECT="your_project_name"
LANGSMITH_TRACING="true"
```

You will also need to configure your Streamlit secrets for the Appwrite and backend URL variables used in `frontend/app.py`.

## License

This repository is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License**.
(see `LICENSE.md` for details) [License](LICENSE.md)

© 2025 Milap Patel. All rights reserved.