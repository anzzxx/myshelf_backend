Myshelf Backend
A backend API for Myshelf, a book management and contribution platform. Built with Django, it provides endpoints for managing books, user authentication, and contributions.

Tech Stack
Python: 3.12+

Django: 5.x

Database: SQLite (default)

Environment Management: python-decouple

Dependency Management: pip, requirements.txt

Project Setup
Clone the repository

git clone https://github.com/your-username/myshelf_backend.git

cd myshelf_backend

2. Create and activate a virtual environment
   
python -m venv venv
venv\Scripts\activate   # On Windows


3. Install dependencies

pip install -r requirements.txt

Environment Configuration

1. Create a .env file in your root directory:

DEBUG=True
SECRET_KEY=your-django-secret-key
ALLOWED_HOSTS=[]
You can access these in settings.py using python-decouple:

#settings
from decouple import config
DEBUG = config('DEBUG', cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')


 Run the Server

python manage.py runserver

You can now access the API at:

http://127.0.0.1:8000/


# Make database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser
.gitignore Note



