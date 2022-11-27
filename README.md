# Corsearch Technical Challenge - Urlcounts

For more details about the requirements,
please refer to [TechnicalChallenge.pdf](TechnicalChallenge.pdf)

## Prerequisites

Before running the app,
please check if your local machine meets the following requirements:

1. Python 3.8 or later is installed. 
2. The below paths are added to the system path:
   ```shell script
   <Python installation root>/
   <Python installation root>/Scripts/
   ```
3. Node.js 18.12.1 LTS is installed.
4. Node.js installation root is added to the system path.
5. Ports 3000 and 5000 are available.

## Steps for Running on Windows

Assumption: Git repository is cloned to your local path `C:\tmp\corsearch\`.

1. Open a command prompt dedicated for **backend server** and run the following commands:
   ```commandline
   > cd C:\tmp\corsearch\backend
   > python -m venv venv
   > cd venv/Scripts
   > activate.bat
   > pip install -U pip
   > cd C:\tmp\corsearch\backend
   > pip install -r requirements.txt
   > flask run
   ```
   To view OpenAPI Document, please access http://127.0.0.1:5000/swagger-ui

2. Open another command prompt dedicated for **frontend server** and run the following commands:
   ```commandline
   > cd C:\tmp\corsearch\frontend
   > npm install
   > npm start
   ```
   
3. Open a browser tab if it does not open automatically. Enter URL http://127.0.0.1:3000

4. To run **unittest**, open another command prompt and run the following commands:
   ```commandline
   > cd C:\tmp\corsearch\backend
   > cd venv/Scripts
   > activate.bat
   > cd C:\tmp\corsearch\backend
   > tox
   ```
    
## Steps for Running on Linux

Assumption: Git repository is cloned to your local path `/c/tmp/corsearch/`.

1. Open a terminal session dedicated for **backend server** and run the following commands:
   ```shell script
   $ cd /c/tmp/corsearch/backend
   $ python -m venv venv
   $ source venv/Scripts/activate
   $ pip install -U pip
   $ pip install -r requirements.txt
   $ flask run
   ```
   To view OpenAPI Document, please access http://127.0.0.1:5000/swagger-ui

2. Open another terminal session dedicated for **frontend server** and run the following commands:
   ```shell script
   $ cd /c/tmp/corsearch/frontend
   $ npm install
   $ npm start
   ```

3. Open a browser tab if it does not open automatically. Enter URL http://127.0.0.1:3000

4. To run **unittest**, open another terminal session and run the following commands:
   ```shell script
   $ cd /c/tmp/corsearch/backend
   $ source venv/Scripts/activate
   $ tox
   ```
    
## Technology Stack

**Frontend**:

| Framework       | Version     |
|-----------------|-------------|
| React           | 18.2.0      |
| React Bootstrap | 2.6.0       |
| Axios           | 1.2.0       |
| Node.js         | 18.12.1 LTS |

**Backend**:

| Framework | Version |
|-----------|---------|
| Flask     | 2.0.3   |
| Pytest    | 7.1.2   |
| tox       | 3.27.1  |

## Quick Reference of Code Locations

| Component         | Code Locations                                                                         |
|-------------------|----------------------------------------------------------------------------------------|
| Frontend page     | [frontend/src/Urlcounts.tsx](frontend/src/Urlcounts.tsx)                               |
| Frontend packages | [frontend/package.json](frontend/package.json)                                         |
| Backend unittest  | [backend/corsearch/tests/test_urlcounts.py](backend/corsearch/tests/test_urlcounts.py) |
| Backend env vars  | [backend/.env](backend/.env)                                                           |
| Backend endpoints | [backend/corsearch/urlcounts.py](backend/corsearch/ulcounts.py)                        |

## ToDo

1. Implement automatic testing on frontend pages using cypress.
2. Arrange React pages more structural into `pages/`, `services/` and `components/`.
3. Externalize API endpoint root to environment variables instead of hardcoded inside React pages.
4. Implement pylint on Python code to minimize runtime error and standardize coding style.
5. Enable HTTPS on both frontend and backend servers.

