# Jenkins - Pipeline: FastAPI App

[Back](../README.md)

- [Jenkins - Pipeline: FastAPI App](#jenkins---pipeline-fastapi-app)
  - [Create FastAPI App](#create-fastapi-app)
    - [Create Env](#create-env)
    - [Create App](#create-app)
    - [Create Unit test](#create-unit-test)
    - [Collect Dependencies](#collect-dependencies)
    - [Dockerize](#dockerize)
  - [Create Jenkins Pipeline](#create-jenkins-pipeline)

---

## Create FastAPI App

### Create Env

```sh
mkdir fastapi-app
cd fastapi-app

python -m venv venv
venv\Scripts\activate

python.exe -m pip install --upgrade pip
pip install fastapi uvicorn
```

---

### Create App

- `main.py`

```py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for POST request data


class GreetingRequest(BaseModel):
    name: str
    age: int


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/greet/{name}")
def greet_name(name: str):
    return {"message": f"Hello, {name}!"}


@app.post("/greet")
def create_greeting(request: GreetingRequest):
    if request.age < 0:
        raise HTTPException(status_code=400, detail="Age cannot be negative")
    return {"message": f"Hello, {request.name}! You are {request.age} years old."}

```

- Test the App Locally

```sh
uvicorn main:app --reload
```

---

### Create Unit test

```sh
pip install pytest
```

- Create a Test File

- `test_main.py`

```py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test the GET root endpoint


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

# Test the GET greet endpoint


def test_greet_name():
    response = client.get("/greet/Alice")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Alice!"}

# Test the POST greet endpoint with valid data


def test_create_greeting_valid():
    response = client.post(
        "/greet",
        json={"name": "Bob", "age": 30}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Bob! You are 30 years old."}

# Test the POST greet endpoint with invalid age (negative)


def test_create_greeting_negative_age():
    response = client.post(
        "/greet",
        json={"name": "Charlie", "age": -5}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Age cannot be negative"}

# Test the POST greet endpoint with missing data


def test_create_greeting_missing_field():
    response = client.post(
        "/greet",
        json={"name": "David"}  # Missing 'age'
    )
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()
    assert any("age" in error["loc"] for error in response.json()["detail"])

```

- Run Pytest

```sh
pytest -v
# ======================================================== test session starts ========================================================
# platform win32 -- Python 3.11.0rc2, pytest-8.3.5, pluggy-1.5.0 -- C:\Users\simon\OneDrive\Tech\Github\Jenkins-Tutorial\module-pipeline-fastapi\fastapi-app\venv\Scripts\python.exe
# cachedir: .pytest_cache
# rootdir: C:\Users\simon\OneDrive\Tech\Github\Jenkins-Tutorial\module-pipeline-fastapi\fastapi-app
# plugins: anyio-4.9.0
# collected 5 items

# test_main.py::test_read_root PASSED                                                                                            [ 20%]
# test_main.py::test_greet_name PASSED                                                                                           [ 40%]
# test_main.py::test_create_greeting_valid PASSED                                                                                [ 60%]
# test_main.py::test_create_greeting_negative_age PASSED                                                                         [ 80%]
# test_main.py::test_create_greeting_missing_field PASSED                                                                        [100%]

# ========================================================= 5 passed in 0.34s =========================================================
```

---

### Collect Dependencies

```sh
pip freeze > requirements.txt
```

---

### Dockerize

- Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /fastapi-app
RUN useradd -m -r appuser && chown appuser:appuser /fastapi-app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
USER appuser
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- Build and Run the Docker Container

```sh
docker build -t fastapi-app .
docker run -d -p 8000:8000 --name fastapi-app fastapi-app

# run Run Pytest in a Container
docker run --rm fastapi-app pytest
```

---

## Create Jenkins Pipeline

- Create a Jenkinsfile

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'docker build -t fastapi-app .'
            }
        }
        stage('Test') {
            steps {
                script {
                    // Run tests and capture the exit code
                    def testResult = sh(script: 'docker run --rm fastapi-app pytest', returnStatus: true)
                    if (testResult != 0) {
                        // Tests failed
                        currentBuild.result = 'FAILURE'
                        error "Tests failed, stopping pipeline."
                    } else {
                        // Tests passed
                        echo "Tests passed successfully!"
                    }
                }
            }
        }
        stage('Deploy') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh 'docker stop fastapi-app || exit 0'
                sh 'docker rm fastapi-app || exit 0'
                sh 'docker run -d --name fastapi-app -p 8000:8000 fastapi-app'
            }
        }
    }
    post {
        failure {
            mail to: 'abc@gmail.com',
                 subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The tests failed in ${env.JOB_NAME} build #${env.BUILD_NUMBER}. Check Jenkins for details: ${env.BUILD_URL}"
        }
        success {
            mail to: 'abc@gmail.com',
                 subject: "Build Succeeded: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The build and tests passed for ${env.JOB_NAME} build #${env.BUILD_NUMBER}. App deployed successfully! Check Jenkins: ${env.BUILD_URL}"
        }
    }
}
```

```sh
docker run -d --restart=always -p 2376:2375 --network jenkins -v /var/run/docker.sock:/var/run/docker.sock alpine/socat tcp-listen:2375,fork,reuseaddr unix-connect:/var/run/docker.sock
docker inspect <container_id> | grep IPAddress
```

```sh
sudo chmod 666 /var/run/docker.sock
```