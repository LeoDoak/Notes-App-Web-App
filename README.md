# OneDrive Flask Web Application: 

### Purpose: 
* Project was created in _**Dr.Layman's Spring 2024 CSC-450 Software Engineering class at UNCW**_
* Semester long group project that aimed to teach us how to work as a software engineering team and better our  understanding of software and git principles. 
* Group members: 
	*  Leo Doak (me) - Project Leader
	*  Cole Thibault - Lead Developer 
	*  Mason Romant  - Developer
	*  Krishna Bommireddy - Developer
	*  Bala Sri Santosh Bikkina - Developer


## Ways to view Project:
1. Locally, running the flask project on personal machine
2. Accessing the Flask Application via Server URL (pythonanywhere)

### Method 1: 
1. Cloning/Downloading github folder to local machine 
2. Create Virtual Environment:
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

3. Activate Virtual Environment 

	MacOS / Linux
	```bash
	$ . .venv/bin/activate
	```

	Windows 
	```bash
	> .venv\Scripts\activate
	```
4. Install All Packages into virtual Environment 

	```bash
	$ pip install -r requirements.txt
	```

5. Run the Web Application 
	* Run the server.py file 
	* Go to web browswer at http://localhost:8000/ to view application 
	```bash 
	$ cd flasknotesapp
	$ python3 server.py 
	```
6. Will need to also register the application with Microsoft Graph in order to utilize OneDrive
	1. go here, https://portal.azure.com/
	2. Click on App Registration 
	3. Click New registration 
	4. Put down a name for the registration and select "Accounts in any identity provider or organizational directory (for authenticating users with user flows)" for the supported accoount types, enter in a rederict URI
	5. Click Register
	6. For API Permissions, go to the dropdown and select "Files.ReadWrite.All"
	7. Copy the client ID and redirect URI from the azure portal into the onedrive method in the server file (line 412)

### Method 2: View on Server 

* Deployed on python anywhere
URL: https://ldoak.pythonanywhere.com/

## Other Information: 

### Packages Included and their Documentation:

* [Waitress Documentation](https://pypi.org/project/waitress)
* [Pillow Documentation](https://pypi.org/project/pillow/)
* [sqlite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
* [numpy Documentation](https://numpy.org/doc/)
* [Flask-login Documentation](https://flask-login.readthedocs.io/en/latest/)
* [msal Documentation](https://pypi.org/project/msal/)
* [requests Documentation](https://pypi.org/project/requests/)
* [ipython Documentation](https://ipython.org/)
* [Flask_wtf Documentation](https://flask-wtf.readthedocs.io/en/1.2.x/)

### Executing Tests:

* How to install testing library:

```bash
$ pip install pytest
```

### Command to execute tests

* Run this in your terminal with the name of the test file you want to check and it will display test cases and if they succeeded or not.
```bash
$ pytest test_myfile.py
```
* Executing user_test.py (Registration Test)
```bash
$ cd flasknotesapp
$ python3 user_test.py 
```

### Sources: 
* Used https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python for a lot of the methods and with modifying the authentication process. 

### Powerpoint
* In the github there is a powerpoint that was used to present our project to the class and the Professor in which we recieved overall positive feedback. 

### Notes:
* This code differs slightly than the code that was used to deploy, sa instead of using local host we use the web aplication addresss.

**Thanks for looking at my web application, Enjoy!** 