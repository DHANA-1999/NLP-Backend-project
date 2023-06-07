# NLP-Backend-project
What Is FastAPI?
----------------
FastAPI is a modern, high-performance web framework for building APIs with Python based on standard type hints. It has the following key features:
Fast to run: It offers very high performance, on par with NodeJS and Go, thanks to Starlette and pydantic.
Fast to code: It allows for significant increases in development speed.
Reduced number of bugs: It reduces the possibility for human-induced errors.
Intuitive: It offers great editor support, with completion everywhere and less time debugging.
Straightforward: It’s designed to be uncomplicated to use and learn, so you can spend less time reading documentation.
Short: It minimizes code duplication.
Robust: It provides production-ready code with automatic interactive documentation.
Standards-based: It’s based on the open standards for APIs, OpenAPI and JSON Schema.

prerequisites and installation procedure:
-----------------------------------------
1. python should be installed
2. fastapi and uvicorn should be installed.
 pip install fastapi
 pip install "uvicorn"
 
Example for fastapi:
-------------------
from typing import Union
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
 Command to run fastapi
 uvicorn main:app --reload
 --------------------------

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

We can test our api at  http://localhost:8000
 
