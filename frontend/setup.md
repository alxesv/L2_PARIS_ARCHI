# Déployement du front
## Installation 
Installation d'apache et de php
```bash
sudo apt install apache2
sudo apt install libapache2-mod-php curl-php
```
Cloner le projet
```bash
- git clone -b front --single-branch https://github.com/alxesv/L2_PARIS_ARCHI.git
```
## Configuration
Accéder au fichier de configuration 000-default.conf.
```bash
sudo nano /etc/apache2/sites-available/000-default.conf
```
Modifier l'url de DocumentRoot : mettre le chemin d'accès au dossier frontend (où se trouve les pages de notre application).
```bash
<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot cheminVersLeDossierFrontend
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
Accéder au fichier de configuration apache2.conf.
```bash
sudo nano /etc/apache2/apache2.conf
```
Comme au dessus, mettre le chemin d'accès vers le dossier du front.
```bash
<Directory cheminVersLeDossierFrontend >
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>
```
et rajouter ce morceau de code afin qu'apache puisse afficher le fichier index.php correctement. 
```bash
<FilesMatch \.php$>
        SetHandler application/x-httpd-php
</FilesMatch>
```
Aller dans le dossier frontend et créer un fichier .env avec la variable d'environnement suivante :
```bash
BASE_URL=("url de l'api")
```

Enfin redémarrer le serveur apache 
```bash
sudo service apache2 restart
```

## Lancement
Le site est accessible sur le navigateur via l'ip de la machine virtuelle.

```bash
sudo service apache2 start
```
