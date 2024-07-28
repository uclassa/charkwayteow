## SSA Backend Server!
This is a backend server written in Django connected to a PostgreSQL database.

## Getting Started
First and foremost, clone the repo and cd into it:
```
git clone https://github.com/uclassa/charkwayteow.git
cd charkwayteow
```

### Setting up the database
To develop locally, you need to set up a PostgreSQL database and connect the django server to it.

First, install postgresql:
```
sudo apt update
sudo apt install postgresql
```

Postgresql is implemented as a server that accepts connections. Make sure the service is active. Chances are, if you installed postgresql via apt, apt autostarts the service for you:
```
systemctl status postgresql
```

Now, you need to create a database. If you don't know how to do this, you can execute the `settings.sql` file included in the repository:
```
sudo -u postgres psql -f settings.sql
```

This will execute SQL code that creates the database as well as the user to connect to the database. Now, before you start the django server, you need to configure it to actually connect to the database you just created. This django server uses the database url defined in the environment variable `DATABASE_URL`, so be sure to set it properly. The format is as follows:
```
postgresql://<user>:<password>@<host>:<port>/<database>
```

If you used the settings.sql file to create your database, the connection string should be:
```
postgresql://cktadmin:i12eatckt@localhost:5432/charkwayteow
```

### Setting up the virtual environment
Django documentation states that you should use the newest version of python. Make sure python and pip are installed using pyenv, conda or any other method. We can use venv to set up our virtual environment, so that any packages we install are isolated to this project. Create the virtual environment and activate it, then install the required packages.
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Lastly, if you just created the database, it doesn't have the tables that are required by the django server. Django manages the database for you so instead of creating the tables using SQL statements, simply run the following command to execute the SQL:
```
python3 manage.py migrate
```
Next, we need to create a superuser, a user who has admin privileges on the backend server:
```
python3 manage.py createsuperuser
```
Finally, you can run the development server and test it out!
```
python3 manage.py runserver
```