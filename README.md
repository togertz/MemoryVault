# MemoryVault
MemoryVault is a Flask-based web application to store an metaphorically *lock up* fond memories users experienced during a specified collection period. During the collection period users can upload little descriptions that can be accompanied by a picture to help them to remember this occasion.
A memory consists of text, date, and optionally an image and/or location coordinates.
When the collection period ends, all collected memories can be revisited in a slideshow view.

## Features
- Upload personal memories with text, date, optional image, and location
- Memories remain hidden until the configured collection period expires
- Slideshow playback of all unlocked memories
- Local and production modes with different storage options:
    - **Development**: images stored locally (`./data/images`)
    - **Production**: images stored in Azure Blob Storage

## Getting Started

### Prerequisites
- **Python** 3.10+
- **PostgreSQL** instance accessible
- **pip** for dependency installation
- (Optional) **Docker** & Docker Compose

---
### Local Setup
The local setup provides a debug mode of the Flask webapp. Changes to the source code will be reloaded during runtime of the flask application.

1. Clone repository
```bash
git clone https://github.com/togertz/MemoryVault.git
cd memoryvault
```

2. Create and activate a virtual environment
```bash
python -m virtualenv .venv
source .venv/Scripts/activate # Linux/MacOS
.venv/Scripts/activate # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
Create a `.env` file in the project root with the following keys:
```ini
SESSION_SECRET=<your-secret>
FLASK_ENV=development # or production

POSTGRES_USER=<db-user>
POSTGRES_PASSWORD=<db-password>
POSTGRES_URL=<db-host>:<db-port>
POSTGRES_DATABASE=<db-name>
```

If `FLASK_ENV=production`, the following environment variable is also required:
```ini
AZURE_STORAGE_CONNECTION_STRING=<your-azure-blob-storage-connection-string>
```

5. Run the app:
```bash
python app.py
```

The app will be available at http://localhost:5000.

---
### Run with Docker Compose
The repository includes a `compose.yaml` file to simplify setup. It provisions both the Flask app and PostgreSQL database. Note that the Flask App will run in **development mode**, but changes to the source code will be not automatically reloaded during runtime.

```bash
docker compose up
```
Once the services are running, the app can be accessed at http://localhost:5000.

---
### Deploy on Azure Cloud
To deploy the Flask application to the Azure Cloud, certain resources need to be configured. After registering, create an [App Service component](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-portal%2Czip-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli) (step **Create a web app in Azure**) and install the Azure CLI.

Next use the scripts in the `azure/` folder:

1. Update `RESOURCE_GROUP_NAME` and `APP_SERVICE_NAME` in both script files.
2. Execute the scripts:
```bash
source azure/build_settings.sh # Run once for configuring settings
source azure/deploy.sh # Run whenever deploying new changes
```



## Running Tests

### Requirements
Installing pytest:
```bash
pip install pytest
```

### Running the Tests
Test cases for the source code in `src/memoryvault` are located in the `tests/` directory. To run all tests, execute:
```bash
pytest test/*
```

## Project Structure
```
MEMORYVAULT/
├── azure/                  # Contains bash scripts for deploying webapp in Azure Cloud
├── data/                   # Folder for saving local data such as uploaded images
├── documentation/          # Draw.io diagrams of the system structure
├── src/memoryvault/        # Source code of the memoryvault Flask app
├── test                    # Pytest test cases
├── .gitignore
├── .pylintrc
├── app.py
├── docker-compose.yaml
├── dockerfile
├── LICENCE
├── README.md
└── requiremnents.txt
```

## Development Notes
- In development mode, debug tools are enabled and images are stored locally
- In production mode, images are stored in Azure Blob Storage