## Getting Started

### Prerequisites
Before you begin, make sure you have the following installed on your machine:

- Python 3.11
- Git
- PostgreSQL 15 or latest

### Clone the Repository
```bash
git clone https://github.com/Story-Of-My-Health/backend-fastapi.git
```

### Set Up Virtual Environment
Navigate to the project directory and create a virtual environment.

```bash
cd backend-fastapi
python3 -m venv env # Mac OS / Linux
python -m venv env # Windows
```

### Activate the Virtual Environment
```bash
source env/bin/activate # Mac OS / Linux
.\env\Scripts\activate # Windows
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment Variables
Rename the env.example file to .env. This file contains environment variables used by the project. You may need to customize these variables based on your local configuration.

```bash
mv env.example .env  # Mac OS / Linux
ren env.example .env  # Windows
```
### Run migrations
```bash
alembic upgrade head
```

### Running the Project
```bash
uvicorn main:app --reload
```

The project will be accessible at http://localhost:8000.
The project documentation will be accessible at http://localhost:8000/docs.
