# Install

```bash
sudo apt install vim gnupg2 -y

sudo apt-get install curl

curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg

sudo apt-get install lsb-release

sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

sudo apt update

sudo apt install postgresql-16

sudo systemctl start postgresql@16-main.service && sudo systemctl enable postgresql@16-main.service
```

## Config files
```bash
sudo nano /etc/postgresql/16/main/postgresql.conf
#Find and change the following line
#listen_addresses = '*'


sudo sed -i '/^host/s/ident/md5/' /etc/postgresql/16/main/pg_hba.conf

sudo sed -i '/^local/s/peer/trust/' /etc/postgresql/16/main/pg_hba.conf

sudo nano /etc/postgresql/16/main/pg_hba.conf
#Ipv4 local connections, add following line
#host    all             all             0.0.0.0/0           scram-sha-256
#Ipv6 local connections, add following line
#host    all             all             0.0.0.0/0                md5
````
```bash
sudo systemctl restart postgresql
```

# Create database and user
```bash
psql -h localhost -U postgres

create database bdd_archi;
create user username with encrypted password 'password';
grant all privileges on database bdd_archi to username;
alter user username with superuser;
```
