# Installation Guide
### Step-1: Clone the repo
Using git,
```
git clone https://github.com/fahimratul/DBMS.git
```
Download zip
```
https://github.com/fahimratul/DBMS/archive/refs/heads/main.zip
```
### Step-2: Navigate to the downloaded/cloned folder
### Step-3: Create a python virtual environment
This step assumes you have python installed.
Create a virtual environment,
```
python -m venv env
```
### Step-4: Activate the environment
On linux, from terminal
```
source env/bin/activate
```
On Windows, from cmd
```
env\Scripts\activate.bat
```

### Step-5:  Install necessary dependencies
```
pip install -r requirements.txt
```

### Step-5: Initialize the database
This step assumes you have *mysql* installed and accessible via cmd/terminal. You have to create user and set password for the user as well. Default credentials for this project,
```
'host':'localhost',
'user':'flaskuser',
'password':'flask',
'database':'project2'
```
You can change them in '__init__.py' file . To initialize database run,
```
flask init-db
```
### Step-6: Run the app
```
flask --app rapid run
```
