# Notes Web Flask Application 

## Install Flask
* Flask is necessary for this project to function correctly. 
* [Install Flask Link](https://code.visualstudio.com/docs/python/tutorial-flask)


### Can also be downloaded using a package manager such as pip: 
 
MacOS / Linux / Windows
```bash
$ pip install flask 
```

## Create Virtual Environment
* A virtual environment is necessary to run the flask project in
* [Info found here](https://flask.palletsprojects.com/en/3.0.x/installation)

MacOS / Linux
```bash
$ mkdir myproject
$ cd myproject
$ python3 -m venv .venv
```
Windows 
```bash
> mkdir myproject
> cd myproject
> py -3 -m venv .venv
```

## Activate Virtual Environment 

MacOS / Linux
```bash
$ . .venv/bin/activate
```

Windows 
```bash
> .venv\Scripts\activate
```

## Other Necessary Packages

* [Waitress Documentation](https://pypi.org/project/waitress)
```bash
$ pip install waitress
```
* [Pillow Documentation](https://pypi.org/project/pillow/)
```bash
$ pip install pillow
```
* [sqlite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
```bash
$ pip install sqlite3
```
* [numpy Documentation](https://numpy.org/doc/)
```bash
$ pip install numpy 
```
* [Flask-login](https://flask-login.readthedocs.io/en/latest/)
```bash
$ pip install flask-login
```


## Running the flask project: 
* Run the server.py file and enter whatever local host number you want
* go into a browser and in the search bar,type in localhost:(Number), ex: localhost:8000
* The project will be started from that link. 

## IDE Used 
* Whichever application you may be using to run the code, we used VS Code or PyCharm, make sure to install the necessary frameworks, including Flask, waitress and any other import you might see in the code above.

**That's all it takes to be able to run our program so far. Enjoy!**