"""
Entry point script
"""

import subprocess
import sys
import threading


def run_fastapi_server(port=8000):
    cmd = [sys.executable, "weekly_mileage_modelling/api/run.py", "--port", str(port)]
    subprocess.Popen(cmd)


def run_streamlit_app(port=8501):
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "frontend/interface.py",
        "--server.port",
        str(port),
    ]
    subprocess.Popen(cmd)


if __name__ == "__main__":
    # Run FastAPI server on port 8000 in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi_server, kwargs={"port": 8000})
    fastapi_thread.start()

    # Run Streamlit app on port 8501 in a separate thread
    streamlit_thread = threading.Thread(target=run_streamlit_app, kwargs={"port": 8501})
    streamlit_thread.start()

    # Join threads to prevent the main thread from exiting
    fastapi_thread.join()
    streamlit_thread.join()
