# Smart Spreadsheet

## Introduction

Smart Spreadsheet is a cutting-edge project designed to enhance the user experience in analyzing spreadsheet data. The primary goal of Smart Spreadsheet is to provide an AI-powered assistant that can help users with their queries related to the provided spreadsheets. By integrating with the OpenAI API, the assistant can analyze user queries, interpret context, and provide accurate and helpful responses.

## Requirements

- Python 3.10 or above
- The following Python libraries:
  - `openpyxl`
  - `python-dotenv`
  - `openai`
  - `fastapi`
  - `uvicorn`
  - `pydantic`
  - `python-multipart`
  - `pandas`


## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/developer-mindpath/Smart-Spreadsheet
   cd Smart-Spreadsheet
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```sh
   python3.10 -m venv ./venv
   source ./venv/bin/activate
   ```

3. **Install the dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up the OpenAI API key:**
   - Create a `.env` file in the root directory of the project with the following content:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```


## Usage

### Step 1: Start the Server
  To use the Assistant, run the below command to start the application:

  ```
  sh start.sh
```

### Step 2: Redirect to the Swagger UI
  To test the Assistant, go to **http://127.0.0.1:8000/docs/**

### Step 3: Upload the files
  Upload the files on Swagger on endpoint ```/api/files/upload``` under **Files** section.

### Step 4: Ask question
  Ask your question related to the uploaded file on Swagger on endpoint ```/api/assistant/ask``` under **Assistant** section.
