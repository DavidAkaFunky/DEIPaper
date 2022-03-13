# DEIPaper

By: **David Belchior** - Instituto Superior Técnico - LEIC-A - Nº 95550

## Dependencies

The dependencies can be found in the `requirements.txt` file, which can be used to install all of them at once.

## Running the server locally

The following steps must be followed:

- Install the dependencies: `pip3 install -r requirements.txt`

- Enter the `src` directory: `cd src`

- Run the server: `python manage.py runserver --insecure` 
    - The `--insecure` flag ensures the static files are loaded, even if `DEBUG` is set to `False`, which shouldn't be a problem, as this server will be run locally.

- Enter the website: `http://127.0.0.1:8000/DEIPaper` (or `http://127.0.0.1:8000/`, which, for now, redirects to DEIPaper, as it's its only app)