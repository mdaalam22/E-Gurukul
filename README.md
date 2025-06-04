# E-Gurukul: Course Management System

E-Gurukul is a web-based platform designed to provide a user-friendly interface for both instructors and students. The system allows instructors to easily create and manage course content, while students can track their progress, interact with peers and instructors, and receive certificates upon completion. A built-in **course chat room** facilitates real-time communication, enhancing the learning experience. 

The platform was developed using **Django**, **HTML**, **CSS**, **JavaScript**, and **Bootstrap**.

## Key Features:
- **Instructor Dashboard**: Easily create and manage courses
- **Student Progress Tracker**: Track course progress in real-time
- **Automated Certificate Generation**: Certificates issued upon course completion
- **Course-specific Chat Room**: Real-time communication between students and instructors
- **Secure Authentication**: Registration, email confirmation, and password management
- **Password Reset**: Password reset functionality with email notifications
- **Responsive Design**: Built using Bootstrap for mobile and desktop responsiveness

## Technologies Used:
- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Authentication**: Django’s built-in user authentication system
- **Database**: SQLite (or specify if using PostgreSQL, MySQL, etc.)

## Setup Instructions:

### Prerequisites:
- Python 3.x
- Django 3.x or above

### Installation:

1. Clone the repository:

    ```bash
    git clone https://github.com/mdaalam22/E-Gurukul.git
    cd E-Gurukul
    ```

2. Set up a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser to access the admin panel:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

7. Access the platform in your browser at `http://127.0.0.1:8000/`.


