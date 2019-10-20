# install PSQL :
	sudo apt install postgresql-client-common

## Install Psql Client:
	sudo apt install postgresql-client-9.5 -y

## Install Psql verions :
	sudo apt-get install postgresql postgresql-contrib -y

## Switch over to the postgres account on your server by typing:
	sudo -i -u postgres

	Or
## Accessing a Postgres Prompt Without Switching Accounts
	sudo -u postgres psql

## start psql client using 
	psql

## Change postgres User password 

	-> ALTER USER postgres PASSWORD 'NEW PASSWORD';

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



