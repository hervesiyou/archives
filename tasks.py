from invoke import task

@task
def runserver(c):
    c.run("cd src/ && python manage.py runserver")

@task
def migrate(c):
    c.run("cd src/ && python manage.py migrate")


@task
def start_api(c):	 
	c.run("cd src/ &&  python  manage.py runserver")

@task
def generate_migrations(c):
	c.run("cd src/ && python manage.py makemigrations")
	c.run("cd src/ && python -B manage.py migrate")

@task
def revert_migrations(c):
	c.run("cd src/ && python3 manage.py migrate arch_portal zero")

@task
def create_superuser(c):
	c.run("cd src/ && python3 manage.py createsuperuser")