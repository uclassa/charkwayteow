### SSA Backend Server!
This is a backend server written in Django connected to a PostgreSQL database.

## Instructions
To run the server, you need to install PostgreSQL and create a database. You can use the settings.sql file to do this.
Clone the repository and cd into it.
```
git clone https://github.com/uclassa/charkwayteow.git
cd charkwayteow
```

We need pip to install the required dependencies. Make sure it is installed, and if it's not, do the following:
```
sudo apt update
sudo apt install python3-pip
```

Use venv to set up your virtual environment for the project. Use python 3.10.12, make sure pip is installed:
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Next, cd into ssabackend and run the server:
```
cd ssabackend
python3 manage.py runserver
```