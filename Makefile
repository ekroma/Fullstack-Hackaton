run:
	python3 manage.py runserver

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

celery:
	celery -A config worker -l info
daemon:
	celery -A config multi start worker1 \
    --pidfile="$HOME/run/celery/%n.pid" \
    --logfile="$HOME/log/celery/%n%I.log"
stop:
	celery multi stopwait worker1 --pidfile="$HOME/run/celery/%n.pid"
