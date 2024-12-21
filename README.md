# Managy

# Managy Execution

We have the system deployed.
- The data base is deployed in Neon.
- The front and the back servers are running in applications of Cloud Run at Google Cloud Platform (GCP).

So to access to our system, you just need to click the following links:

- Backend, Django App: https://managy-404252599785.us-central1.run.app
- Frontend, Node App: https://managy-front-404252599785.us-west2.run.app

If you want to install the system and run it in a local way, go below.

# Installation Steps

## 1. Clone the Repository
Download the project files by cloning the repository:

```bash
git clone https://git.cs.usask.ca/elr490/managy.git
cd managy
```

# Backend Installation

If you want to install just the frontend, you can do it. Go to "Frontend Installation" section. Otherwise, continue.

## Prerequisites

Ensure you have the following installed on your system:
- Python 3.8+ (check version: `python --version` or `python3 --version`)
    - Better: python:3.12.3-slim-bullseye
- Git
- Virtualenv (`pip install virtualenv`)

## Installation Steps

- Go inside managy/backend/

### 1. Create a Virtual Environment
Set up a virtual environment to isolate project dependencies:

```bash
python -m venv .venv
```

Activate the virtual environment:
- **Windows**:
    ```bash
    .venv\Scripts\activate
    ```
- **macOS/Linux**:
    ```bash
    source .venv/bin/activate
    ```

---

### 2. Install Requirements
Install the required Python packages specified in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

### 3. Download the secret files
Install the files that have secret variable configurations of the project and the key for cloud storage (2 files).

- Download the ".env" and "cloudstoragekey.json" files from https://usaskca1-my.sharepoint.com/:f:/g/personal/elr490_usask_ca/EuSwUTqdvElFo8EtODabirsBvnykjuGG-5Q-KOzxei4Sog?e=aT3tQX
- Save them inside managy/backend/

---

### 4. Run the Server
Start the development server:

```bash
python manage.py runserver
```

The server will be running at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Additional Notes

- To deactivate the virtual environment, run:
    ```bash
    deactivate
    ```



# Frontend Installation

## Prerequisites

Ensure you have the following installed on your system:
- [Node.js](https://nodejs.org/) (v16+ recommended, check version: `node --version`)
    - Better: Last Version
- [npm](https://www.npmjs.com/) (comes with Node.js, check version: `npm --version`)
- Git

---

## Installation Steps

### 1. Download secret files
Install the files that have secret variable configurations of the project and the key for cloud storage (2 files).

- Download the ".env" and "cloudstoragekey.json" files from https://usaskca1-my.sharepoint.com/:f:/g/personal/elr490_usask_ca/Eg4bKM2JgZ9HtY49jNU314sBeUmVz3sm24vX-_g1vYvBtg?e=HF1nDI
- Save them inside managy/frontend/

---

### 2. Choose API Version
You can either choose to use the deployed backend version or the local version that you have installed.

1. Navigate to managy/frontend/src/api.js.
2. Around lines 7–8, you will find the following code:

```javascript
const apiUrl = "https://managy-404252599785.us-central1.run.app";
const apiUrl = "http://127.0.0.1:8000";
```

3. If you want to use the deployed version, comment out the second apiUrl. If you want to use the local version, comment out the first apiUrl.

---

### 3. Install Dependencies
Install all the required dependencies using npm:

```bash
npm install
```

### 4. Run the Development Server
Start the development server:

```bash
npm run dev
```

The application will be running locally. By default, it can be accessed at [http://localhost:3000/](http://localhost:3000/).

---

## Additional Notes

- To stop the development server, press `Ctrl+C` in the terminal.
- If you encounter issues with missing dependencies, try:
    ```bash
    npm install
    ```

- For production builds, run:
    ```bash
    npm run build
    npm start
    ```

---


## License
University of Saskatchewan, CMPT-370 Course Project
