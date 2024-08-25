To Build and Run Docker Container
docker build -t fastapi-courses .
docker run -p 8000:8000 fastapi-courses

To Run testcases
pytest test_main.py
