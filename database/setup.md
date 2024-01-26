sudo apt install vim gnupg2 -y

sudo apt-get install curl

curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg

sudo apt-install lsb-release

sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

sudo apt update

sudo apt install postgresql-16

sudo systemctl start postgresql@16-main.service && sudo systemctl enable postgresql@16-main.service

