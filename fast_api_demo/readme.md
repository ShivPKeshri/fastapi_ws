# Main Notes:

Taken the reference from below blogs:
https://fastapi.tiangolo.com/
https://github.com/pixegami/simple-fastapi-example/blob/main/main.py

Required libraries to install using pip : fastapi, uvicorn

to launch the app by hitting the below command inside the project directory: uvicorn main:app --reload

to launch the app in browser http://127.0.0.1:8000/

and swagger http://127.0.0.1:8000/docs/ and http://127.0.0.1:8000/redoc

Here the official documentation for fastapi : https://fastapi.tiangolo.com/tutorial/


# SETUP the env:

Need to install below libraries:
```
pip install fastapi
pip install uvicorn
```

we have got the below exception while installing the fastapi:

Cargo, the Rust package manager, is not installed or is not on PATH. This package requires Rust and Cargo to compile extensions. Install it through the system's package manager or via https://rustup.rs/

to fix this, we have install the rust by below command:
```
brew install rust
```

To execute this function hit the below command:
```
uvicorn main:app --reload
```