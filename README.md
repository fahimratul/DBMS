#Installation Guide
### Step-1: Clone the repo
Using git,
```
git clone --branch oneLast --single-branch https://github.com/fahimratul/DBMS.git
```
Download zip through browser
```
https://github.com/fahimratul/DBMS/archive/refs/heads/final.zip
```
### Step-2: Navigate to the downloaded/cloned folder
Unzip if you have downloaded the zip file. Open the the folder regardless of the case. 
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
user : flaskuser,
password : flask,
database : project2
```
If you wish to use different set of credentials, you have to make changes in '__init__.py' file . To initialize database run,
```
flask --app rapid init-db
```
### Step-6: Run the app
```
flask --app rapid run
```
The app should be running now.