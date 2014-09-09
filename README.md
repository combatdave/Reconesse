Reconesse
=========

Reconesse website


Setup
=====

#### Setting up a virtual environment

Make sure `virtualenv` is installed

    pip install virtualenv

We create a new virtualenv called `venv` in the root of the project

    virtualenv venv

We `source` the new environment

    source venv/bin/activate    # If using Bash
    . venv/bin/activate.fish    # If using Fish
    venv/scripts/activate.bat   # If on Windows (For shame, Dave, for shame!)

Now we can install the dependencies, and they will stay local to the virtual environment

    pip install -r requirements.txt

To leave the virtual environment run

    deactivate

#### Setting up Honcho + Postgres

Install Honcho

    brew install honcho        # OSX
    apt-get install honcho     # *nix
    
*Note:* Apparently, you can `pip install honcho`. Haven't tried this.

Grab a full Postgres installation, e.g. [http://postgresapp.com/](http://postgresapp.com/), and run it.

Create a database

    createdb reconesse

Create a file called `.env` which holds a uri to our database. Locally, this would be something like

    echo "DATABASE_URL=postgres:///reconesse" > .env

The `.env` file should also contain other settings that should not be kept in `settings.py` such as secret keys, etc. Also, if we want to, we can have the application read the `DEBUG` variable from `.env`. That way, the production instance of the site would have a `.env` file with `DEBUG=False` and development instances would have `DEBUG=True`. Because of this, we do not want to sync these files, and they should be added to `.gitignore`

Now we can sync our database

    honcho run python manage.py syncdb

And then we can run our server

    honcho run python manage.py runserver
