Project: Simple website where the user able to login and register. Then post their article in the website. The user able to leave a comment, edit and Delete the post. Other user able to only view other user post and leave a comment. Each user have their dashboard where they could manage their posts and see other people's comment. 

Code Suggested: Python Language

Deployment: Any Free tiered cloud such as Github or Amazon
Extra Point: Containerized the application within Docker
Duration 1 day completion

Python and Flask Environment command:
pip install flask flask-sqlalchemy flask-bcrypt flask-login

Directory Structure:

project/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── post.html
│   │   ├── comment.html
│   ├── static/
│       ├── styles.css
├── docker-compose.yml
├── Dockerfile
├── app.py
└── requirements.txt