FROM python:3.14.7-slim
WORKDIR /app
# The program is split across several modules, so copy every Python file
COPY *.py .
# inventory.json lives in /data, which is mounted as a volume so it survives the container
WORKDIR /data
CMD ["python", "/app/inventory_manager.py"]
