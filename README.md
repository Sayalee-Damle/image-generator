## Description

This tool uses Dall-E to generate images based on user requirements. 

## Installation instructions


```pip install poetry
poetry shell
poetry build
poetry install
```




This creates a specific environment with all the libraries in need!

``` To specify configurations use .env file ```

## Configuration
The .env file might be configured like this:
```
OPENAI_API_KEY= <openai api key...>
OPENAI_MODEL = <model to be used>
IMAGE_PATH_DISC = /ImagesDall-E/
PROJECT_ROOT =  <root folder of project>
REQUEST_TIMEOUT = 300
LLM_CACHE = False
VERBOSE_LLM = True
TOKEN_LIMIT = 13000
```
