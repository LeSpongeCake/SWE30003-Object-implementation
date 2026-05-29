# Getting Started
Before running the commands, ensure your working directory is set to the root folder of the project, the one that contains the main subfolders `frontend/` and `backend/`.

## Backend

### Installing Dependencies
```
pip install -r backend/requirements.txt
```

### Running the FastAPI server
```
cd backend
fastapi dev main.py
```
This will start the backend FastAPI server on your local machine at port 8000.

### API documentation
Once the FastAPI application is running, navigate to http://127.0.0.1:8000/docs in your web browser to view the automatic API documentation.