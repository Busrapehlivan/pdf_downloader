import os
import subprocess

# Set environment variable to disable Docker
os.environ["AUTOGEN_USE_DOCKER"] = "False"

# Run the main script
subprocess.run(["python", "pdf_downloader.py"])
