@call venv/Scripts/activate.bat
@rem @set FLASK_APP=./src/server.py
@set FLASK_APP=./src/gaintrader.py
@set FLASK_DEBUG=1
flask db upgrade
flask run