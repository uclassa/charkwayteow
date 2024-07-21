### SSA Backend Server!
This is a backend server written in Django connected to a PostgreSQL database.

## Instructions
To run the server, you need to install PostgreSQL and create a database. You can use the settings.sql file to do this.
Clone the repository and cd into it.
```
git clone https://github.com/uclassa/charkwayteow.git
cd charkwayteow
```

You need to set up a virtual environment for the project. Use python 3.10.12:
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Next, run the development server:
```
python3 manage.py runserver
```