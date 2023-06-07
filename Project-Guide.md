## NLP-Backend-project
## What Is FastAPI?
FastAPI is a modern, high-performance web framework for building APIs with Python based on standard type hints. It has the following key features:

1.Fast to run: It offers very high performance, on par with NodeJS and Go, thanks to Starlette and pydantic.

2.Fast to code: It allows for significant increases in development speed.

3.Reduced number of bugs: It reduces the possibility for human-induced errors.

4.Intuitive: It offers great editor support, with completion everywhere and less time debugging.

5.Straightforward: It’s designed to be uncomplicated to use and learn, so you can spend less time reading documentation.

6.Short: It minimizes code duplication.

7.Robust: It provides production-ready code with automatic interactive documentation.

8.Standards-based: It’s based on the open standards for APIs, OpenAPI and JSON Schema.

## prerequisites and installation procedure:

1. python should be installed

3. fastapi and uvicorn should be installed.
 
 `pip install fastapi`
 
 `pip install "uvicorn"`
 
## Example for fastapi:

from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def read_root():

    return {"Hello": "World"}

@app.get("/items/{item_id}")

def read_item(item_id: int, q: Union[str, None] = None):

    return {"item_id": item_id, "q": q}
    
`Command to run fastapi`
`uvicorn main:app --reload`
 

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

INFO:     Started reloader process [28720]

INFO:     Started server process [28722]

INFO:     Waiting for application startup.

INFO:     Application startup complete.

We can test our api at ` http://localhost:8000`

## FastApi in Docker:

To use fastapi in docker we need Dockerfile and requirements.txt and src files as shown in repo.

*Source files should contain python file for nlp model with fastapi.

`FastAPI URL: @app.get("/filedata/{start_date}&{end_date}")`

`Building Docker image:`
Go to path where dockerfile is locating.
`docker build -t <image-name> .`

`Creating Docker container from docker image:`
 
 `docker run --name=<container name> -d -p 8000:8000 <image-name>`
 
 Accessing application using Fastapi:
 `http://<server IP ADDRESS >:8000/filedata/02-06-2023&04-06-2023**`
 
 `Here:`
 filedata - end point for fastapi
 02-06-2023&04-06-2023 -  query parameters (start & end dates)
 
 
