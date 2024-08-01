
start_api:
	# @read -p "Enter migration name (e.g., add_new_action_log_type): " name; \
	# cd src/ && python3 manage.py makemigrations auth_portal --name $$name
	cd src/ && PYTHONDONTWRITEBYTECODE=1 python3 -B manage.py runserver

generate_migrations:
	cd src/ && python3 manage.py makemigrations  
	cd src/ && python3 -B manage.py migrate

revert_migrations:
	cd src/ && python3 manage.py migrate arch_portal zero

create_superuser:
	cd src/ && python3 manage.py createsuperuser
