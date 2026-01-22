# How to Run the RAG Demo Application

This tutorial guides you through setting up and running the Learning RAG Demo application, a FastAPI-based Retrieval-Augmented Generation (RAG) service.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+** — [Download here](https://www.python.org/downloads/)
- **pip** (Python package manager) — Usually comes with Python
- **Git** (optional, for version control)

### Check Your Installations

Open a terminal (PowerShell, Command Prompt, or bash) and verify:

```bash
python --version
pip --version
```

You should see Python 3.8 or higher and pip installed.

---

## Step 1: Clone or Download the Project

If you haven't already, download the project folder to your local machine:

```bash
cd path/to/your/projects
git clone <repository-url>
cd "Rag Demo"
```

Or simply navigate to your downloaded folder:

```bash
cd c:\Users\UniPin\Downloads\Rag Demo
```

---

## Step 2: Set Up a Virtual Environment

Creating a virtual environment isolates this project's dependencies from other Python projects.

### On Windows (PowerShell or Command Prompt):

```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

If using Command Prompt instead of PowerShell:

```bash
python -m venv venv
venv\Scripts\activate.bat
```

### On macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

You'll see `(venv)` appear in your terminal prompt when activated.

---

## Step 3: Install Dependencies

The application requires several Python packages. Install them using pip:

```bash
pip install fastapi uvicorn langraph qdrant-client
```

**Alternatively**, if a `requirements.txt` file exists, install all dependencies at once:

```bash
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables (Optional)

The application uses a Qdrant vector database. By default, it points to:

```
http://localhost:6333
```

If you have Qdrant running on a different host, set the environment variable:

### Windows (PowerShell):

```bash
$env:QDRANT_URL = "http://your-qdrant-host:6333"
```

### Windows (Command Prompt):

```bash
set QDRANT_URL=http://your-qdrant-host:6333
```

### macOS/Linux:

```bash
export QDRANT_URL=http://your-qdrant-host:6333
```

If you don't set this, the application will fall back to in-memory storage.

---

## Step 5: Run the Application

Start the FastAPI server with uvicorn:

```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Explanation of flags:**

- `src.main:app` — Tells uvicorn where to find the FastAPI app instance
- `--reload` — Automatically restarts the server when you make code changes (dev mode)
- `--host 0.0.0.0` — Makes the API accessible from any network interface
- `--port 8000` — Runs the server on port 8000

You should see output like:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

---

## Step 6: Test the API

### Option A: Using the Interactive Docs (Recommended)

Open your browser and navigate to:

```
http://localhost:8000/docs
```

This opens the **Swagger UI**, where you can test endpoints interactively.

### Option B: Using cURL

Add a document:

```bash
curl -X POST "http://localhost:8000/add" \
  -H "Content-Type: application/json" \
  -d '{"text": "FastAPI is a modern web framework for Python."}'
```

Ask a question:

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is FastAPI?"}'
```

Check status:

```bash
curl "http://localhost:8000/status"
```

### Option C: Using Python Requests

Create a test script, e.g., `test_api.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

# Add a document
response = requests.post(f"{BASE_URL}/add", json={
    "text": "Machine Learning is a subset of AI."
})
print("Add Document:", response.json())

# Ask a question
response = requests.post(f"{BASE_URL}/ask", json={
    "question": "What is machine learning?"
})
print("Ask Question:", response.json())

# Check status
response = requests.get(f"{BASE_URL}/status")
print("Status:", response.json())
```

Run it:

```bash
pip install requests
python test_api.py
```

---

## API Endpoints

### POST `/add` — Add a Document

**Request:**

```json
{
  "text": "Your document text here"
}
```

**Response:**

```json
{
  "status": "success",
  "id": "doc_123"
}
```

### POST `/ask` — Ask a Question

**Request:**

```json
{
  "question": "Your question here"
}
```

**Response:**

```json
{
  "question": "Your question here",
  "answer": "Generated answer based on stored documents"
}
```

### GET `/status` — Check Application Status

**Response:**

```json
{
  "status": "running",
  "documents_count": 5
}
```

---

## Stopping the Server

To stop the application, press **CTRL+C** in the terminal where the server is running.

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'fastapi'`

**Solution:** Ensure your virtual environment is activated and dependencies are installed:

```bash
# Activate venv
venv\Scripts\Activate.ps1  # Windows PowerShell
source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install fastapi uvicorn langraph qdrant-client
```

### Issue: Port 8000 Already in Use

**Solution:** Run on a different port:

```bash
python -m uvicorn src.main:app --reload --port 8001
```

Then access the app at `http://localhost:8001`.

### Issue: Cannot Connect to Qdrant

**Solution:** The application has a built-in fallback to in-memory storage. If you want to use Qdrant, ensure it's running:

```bash
# Using Docker (if you have Docker installed)
docker run -d -p 6333:6333 qdrant/qdrant
```

---

## Development Tips

- **Auto-reload:** The `--reload` flag watches file changes and restarts the server automatically—great for development.
- **Debug mode:** Add `print()` statements or use a debugger to inspect values.
- **Logs:** Check the terminal output for detailed logs and error messages.
