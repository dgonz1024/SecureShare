# SecureShare Project

SecureShare is a Django-based file-sharing platform that utilizes AES encryption to ensure secure file transfers. This project allows users to upload, encrypt, and share files securely.

## Features

- AES encryption for secure file storage and sharing.
- User-friendly interface for file uploads and downloads.
- Asynchronous support for improved performance.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd SecureShare
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the development server:
   ```
   python manage.py runserver
   ```

2. Access the application at `http://127.0.0.1:8000/`.


## License

This project is licensed under the MIT License. See the LICENSE file for more details.