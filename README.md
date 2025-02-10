# PDF Generation Service

## Overview

This project is a FastAPI-based microservice for generating PDFs from dynamic HTML templates. It utilizes **WeasyPrint** for PDF generation and **Jinja2** for template rendering. The project supports template management, user authentication, and role-based permissions to control access to different functionalities.

## Features

- **User Authentication & Permissions**: Secure endpoints using JWT authentication.
- **Template Management**: Create, update, and delete templates stored in the database.
- **Dynamic PDF Generation**: Generate PDFs based on user-provided data.
- **Asynchronous Background Processing**: Handle PDF generation efficiently.
- **Download Endpoint**: Force the download of generated PDFs.
- **Faker Data Generator**: Generate random data for testing.

## Technologies Used

- **FastAPI**: High-performance web framework.
- **WeasyPrint**: HTML to PDF conversion.
- **Jinja2**: Templating engine.
- **Beanie**: Async ODM for MongoDB.
- **MongoDB**: NoSQL database.
- **JWT Authentication**: Secure API access.

## Installation

### Prerequisites

- Python 3.13
- Pip package manager

### Steps

1. Clone the repository:

   ```sh
   git clone https://github.com/samuelfrutuoso/PDFReport.git
   cd PDFReport
   ```

2. Create a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run the FastAPI application:

   ```sh
   fastapi dev app.py
   ```

5. Access the API documentation at:
   - **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   <!-- - **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) -->

## TODO List (Pending Tasks)

- Create Exceptions
- Create logs
- *document_service.create_document()*: Extract all from zip path and genereate PDF
- *document_service.download()*: Download PDF
- *config.Settings.BACKEND_CORS_ORIGNS*: Load values from *.ini*
- *template_service.upload_template*: Add content check (only index.html, images and css)
- *template_service.TemplateService.upload_template()*: Add Upload to cloud services  (also to documents)
- *template_service.TemplateService.delete_template()*: Add delete from cloud services (also to documents)

## Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests.

## License

This project is licensed under the MIT License.
