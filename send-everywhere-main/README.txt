ZipDrop

Purpose:
ZipDrop is a Django web application designed for simple and efficient file sharing across devices. It allows users to upload files and share them using a generated code, a direct link (for logged-in users), or via email (feature recently added). The application also includes user authentication and automatic cleanup of expired files.

Tech Stack:
- Backend: Python, Django (Web Framework)
- Task Queue: Celery (for background tasks like file cleanup)
- Database: SQLite (configured for local development)
- Frontend: HTML, Tailwind CSS (for styling)
- Dependency Management: pip (using requirements.txt)

Key Features:
- File Upload and Sharing (via code or link)
- Email File Sharing (sends a direct link)
- User Authentication (Login/Register)
- Automatic File Expiration and Cleanup (handled by Celery)
- Simple and Responsive UI 