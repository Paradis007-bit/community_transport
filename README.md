1.Community transport  1.o 
this  program helps user to estimate the time the nearest bus will come , it's the first version
so it's not perfect 
2.features:
-a responsive cli 
-list available buses 
-calculate an ETA (estaimated time of arrival)
3.API:
-it uses FastAPI
-uvicorn as ASGI server
-nginx as load balancer
-docker for loacl testing 
4.how it works:
4.1.on local machine you use :python3 app/cli.py
-and if you want to use server locally you can use uvicorn app.main:app --host 0.0.0.0 --port 8000
setting on both servers 01 and 02 : -cloning my github repository (git clone https://github.com/Paradis007-bit/community_transport.git
cd community_transport
)
-use virtual environment (python3 -m venv venv
source venv/bin/activate)
-dependencies (pip install -r requirements.txt
)
-run api (uvicorn app.main:app --host 0.0.0.0 --port 8000
)
4.2.on webserver and load balancer :
-install nginx
-use uvicorn app.main:app --host 0.0.0.0 --port 8000 or curl [http](http://localhost)

