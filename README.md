# RDI-TASK

## Description

API for a document processing service. Users can upload images and PDF files to the API, and the API can perform some operations on the files and return the results.

## Installation

### Using Docker

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/rdi-task.git
   ```
2. Navigate to the project directory:
   ```sh
   cd rdi-task
   ```
3. Build and run the Docker container:
   ```sh
   docker build -t rdi-task .
   docker run -p 8000:8000 rdi-task
   ```

### Normal Django Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/mostafanasser2000/RDI-TASK
   ```
2. Navigate to the project directory:
   ```sh
   cd rdi-task
   ```
3. Create a virtual environment:
   ```sh
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```
5. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
6. Apply migrations:
   ```sh
   python manage.py migrate
   ```
7. Run the development server:
   ```sh
   python manage.py runserver
   ```
