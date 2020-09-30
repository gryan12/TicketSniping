#!/usr/bin/bash
cd /code/backend

set -e

until PGPASSWORD=$DB_PASSWORD psql -v ON_ERROR_STOP=1 --host "$DB_HOST" --port "$DB_PORT" --username "$DB_USER" --password "$PGPASSWORD" --dbname "$DB_NAME" -c '\q'; do
  >&2 echo "[PSQL::WAITING] Listening via $DB_USER@$DB_HOST:$DB_PORT/$DB_NAME"
  sleep 3
done

>&2 echo "[PSQL::SUCCESS] Connected via $DB_USER@$DB_HOST:$DB_PORT/$DB_NAME"

python manage.py migrate --noinput --verbosity 0
python manage.py collectstatic --noinput --verbosity 0

if [ $USE_VSCODE_DEBUGGER = 1 ]; then
  python manage.py runserver 0.0.0.0:8000 --noreload --nothreading --verbosity 0
else
  python manage.py runserver 0.0.0.0:8000 --verbosity 0
fi


exec "$@"
