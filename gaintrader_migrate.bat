@rem @set FLASK_APP=./src/server.py
@set FLASK_APP=./src/gaintrader.py
@set FLASK_DEBUG=1
@rem flask db init
flask db migrate
