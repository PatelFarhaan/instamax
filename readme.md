# install PSQL :
	sudo apt install postgresql-client-common

## Install Psql Client:
	sudo apt install postgresql-client-9.5 -y

## Install Psql verions :
	sudo apt-get install postgresql postgresql-contrib -y
## Now create a superuser for PostgreSQL

    sudo -u postgres createuser --superuser **name_of_user**
    sudo -u postgres createuser --superuser postgres


## And create a database using created user account

    sudo -u postgres createdb instamax

## You can access created database with created user by,

    psql -U name_of_user -d name_of_database


    ex: psql -U postgres -d instamax




## Switch over to the postgres account on your server by typing:
	sudo -i -u postgres

	Or

## Accessing a Postgres Prompt Without Switching Accounts
	sudo -u postgres psql

	sudo service postgresql status

## Password change ;
    ALTER USER postgres WITH PASSWORD Farees143k

## start psql client using 
	psql

    createdb -h localhost -p 5432 -U postgres instamax



## Change postgres User password

    login to database

    $ sudo -u postgres psql instamax

	update Password

	-> ALTER USER postgres WITH PASSWORD 'Farees143k';

# Install Python3 Client:

    sudo apt-get install python3-pip

# Install virtual env:

    sudo apt-get install python-virtualenv

## It time to create to virtual environment flask-env, where we will install flask.

    virtualenv venv




# Install unzip:

    sudo apt-get install unzip

# Unzip chrome file:
    unzip chromedriver_linux64.zip

-  Move extracted file to /usr/local/bin/chromedriver

    mv chromedriver /usr/local/bin/chromedriver

# Install Memcached on Ubuntu

    sudo apt-get update

    sudo apt-get install memcached

    Check if service is installed

        ps aux | grep memcached





# Install Fix Version of Chrome: link [https://www.ubuntuupdates.org/pm/google-chrome-stable]
    3rd Party Repository: Google Chrome

    Setup key with:

        wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

	Setup repository with:

	    sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

	- Setup package with:
		sudo apt-get update 
		sudo apt-get install <package name>

		ex: sudo apt install google-chrome-stable=77.0.3865.120-1



	sudo apt-get install nginx uwsgi uwsgi-plugin-python
