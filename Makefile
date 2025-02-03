
start_api:
	 
	cd src/ &&  python  manage.py runserver

generate_migrations:
	cd src/ && python manage.py makemigrations  
	cd src/ && python -B manage.py migrate

revert_migrations:
	cd src/ && python3 manage.py migrate arch_portal zero

create_superuser:
	cd src/ && python3 manage.py createsuperuser
