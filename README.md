# My Digital Portfolio
Welcome to the repository for my solution for the **Web Technology Course** where I built my portfolio website, applying the web development skills learned throughout the course.
## Project Overview

In this project, I created a personal portfolio website using the **Django** framework. The website serves as a showcase for my skills, projects, and achievements in which I applied the fundamental principles of web development, including:

- Setting up Django
- Building dynamic web pages
- Creating a database-driven website
- Styling with HTML, CSS, and JavaScript

## Getting Started
### Dev
1. clone repo
2. `cd digital-portfolio`
3. run `docker-compose -f docker-compose.dev.yml up`
4. apply changes and 
5. open `localhost:8000` to see the changes

### Staging
1. clone repo
2. `cd digital-portfolio`
3. run `docker-compose -f docker-compose.staging.yml up`
4. open `localhost:8000` to test the application

## Development
Several checks should be performed before merging code into the main branch because there are CI Pipelines in place.
Performing the following checks locally ensure a successful pipeline execution:
- `isort ./app`
- `black --config pyproject.toml ./app`
- `flake8 ./app`
- `djlint ./app --reformat`
- `./app/manage.py test`
## Testing
Blog posts and projects an be maintained using the admin platform of django. In order to do so you need to create a superuser, which you can then use to log into the platform:
- `python manage.py createsuperuser`
- the admin platform can then be accessed under `localhost:8000/admin`

## Structure of the Repository
- app/portfolio/: This is the Django project directory.
- app/templates/: HTML files for the portfolio page.
- app/static/: Static files like CSS, JavaScript, and images.
- app/about/: The «About me» page
- app/blog/: The «Blog» page
- app/projects/: The «Projects» page