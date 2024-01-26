## Install
```bash
sudo apt-get install git

git clone -b back --single-branch https://github.com/alxesv/L2_PARIS_ARCHI.git

sudo apt install python3 python3-pip

cd backend

pip3 install -r "requirements.txt"
```

# Create .env according to exemple in README
```bash
touch .env
nano .env
```
```bash

python3 database.py

#If there are path issues

#in home directory
sudo nano .bashrc

# add to last line
export PATH=$PATH:/your/directory 
# with /your/directory being what you want to add to path
```
## You can start the app with 
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```