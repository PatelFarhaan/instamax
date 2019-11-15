# Install Python3 Client:

    sudo apt-get install python3-pip -y


# install vir- env

    sudo apt-get install virtualenv -y

# Install virtual env:

    sudo apt-get install python-virtualenv

## It time to create to virtual environment flask-env, where we will install flask.

    virtualenv venv




# install PSQL :
	sudo apt install postgresql-client-common

## Install Psql Client:
	sudo apt install postgresql-client-9.5 -y

## Install Psql verions :
	sudo apt-get install postgresql postgresql-contrib -y

## Now create a superuser for PostgreSQL

    sudo -u postgres createuser --superuser **name_of_user**
    sudo -u postgres createuser --superuser postgres
    sudo -u postgres createuser --superuser instamax_user


## And create a database using created user account

    sudo -u postgres createdb instamax
    sudo -u instamax_user createdb instamax

## You can access created database with created user by,

    psql -U name_of_user -d name_of_database


    ex: psql -U postgres -d instamax
    ex: psql -U instamax_user -d instamax




## Switch over to the postgres account on your server by typing:
	sudo -i -u postgres

	Or

## Accessing a Postgres Prompt Without Switching Accounts
	sudo -u postgres psql

	sudo service postgresql status


## start psql client using 
	psql

    createdb -h localhost -p 5432 -U postgres instamax



## Change postgres User password

    login to database

    $ sudo -u postgres psql instamax

	update Password

	-> ALTER USER postgres WITH PASSWORD 'Farees143k'
    -> ALTER USER postgres PASSWORD "webapp_password"



# Install unzip:

    sudo apt-get install unzip

# Unzip chrome file:
    unzip chromedriver_linux64.zip

-  Move extracted file to /usr/local/bin/chromedriver

    sudo mv chromedriver /usr/local/bin/chromedriver

# Install Memcached on Ubuntu

    sudo apt-get update

    sudo apt-get install memcached

    Check if service is installed

        ps aux | grep memcached





# Install Fix Version of Chrome: link [https://www.ubuntuupdates.org/pm/google-chrome-stable]

| Name    |   Release    |   Repository    |   Level    |   Version    |   PPA   |
|---- |----|----| ----| ----| ---- |
| google-chrome-unstable    |   stable    |   main    |   base    |   80.0.3964.0-1    |   Google Chrome   |
| google-chrome-beta    |   stable    |   main    |   base    |   79.0.3945.36-1    |   Google Chrome   |
| google-chrome-stable    |   stable    |   main    |   base    |   78.0.3904.97-1    |   Google Chrome   |


    Ex: Take version: 78.0.3904.97

### Here are the steps to select the version of ChromeDriver to download:

* First, find out which version of Chrome you are using. Let's say you have Chrome 78.0.3904.97.

* Take the Chrome version number, remove the last part, and append the result to URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_".
    For example, with Chrome version 78.0.3904.97, you'd get a URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_78.0.3904".

* Use the URL created in the last step to retrieve a small file containing the version of ChromeDriver to use.
    For example, the above URL will get your a file containing "78.0.3904.70".(GOT THIS NUMBER) -> (The actual number may change in the future, of course.)

* Use the version number retrieved from the previous step to construct the URL to download ChromeDriver.
    With version 78.0.3904.70, the URL would be "https://chromedriver.storage.googleapis.com/index.html?path=78.0.3904.70/".

* After the initial download, it is recommended that you occasionally go through the above process again to see if there are any bug fix releases.

### We always provide ChromeDriver for the current Stable and Beta versions of Chrome.

  However, if you use Chrome from Dev or Canary channel, or build your own custom version of Chrome, It is possible that there is no available ChromeDriver that officially supports it.
  In this case, please try the following:

* First, construct a LATEST_RELEASE URL using Chrome's major version number.
    For example, with Chrome version 73.0.3683.86, use URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_73".
    Try to download a small file from this URL.
    If it successful, the file contains the ChromeDriver version to use.

* If the above step failed, reduce the Chrome major version by 1 and try again.
    For example, with Chrome version 75.0.3745.4, use URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_74" to download a small file, which contains the ChromeDriver version to use.
* You can also use ChromeDriver Canary build.

### In addition, the version of ChromeDriver for the current stable release of Chrome can be found at https://chromedriver.storage.googleapis.com/LATEST_RELEASE. However, using on this file may be less reliable than methods described above.

    1. download Chrome Browser

        wget -q http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_78.0.3904.97-1_amd64.deb

        sudo dpkg -i google-chrome-stable_78.0.3904.97-1_amd64.deb

    Download ChromeDriver:

        wget -q https://chromedriver.storage.googleapis.com/78.0.3904.70/chromedriver_linux64.zip

        unzip chromedriver_linux64.zip

        sudo mv chromedriver /usr/local/bin/chromedriver


    2. # Add Google public key to apt
    
        wget -q -O - "https://dl-ssl.google.com/linux/linux_signing_key.pub" | sudo apt-key add -

    # Add Google to the apt-get source list
    # echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list
    #   -- didn't have permission for this, even w/ sudo; but could do it w/ vim
            
            sudo vim /etc/apt/sources.list

    # Add in the echo line above to bottom of file

    # Update apt-get
        
        sudo apt-get update

    # Get stable chrome
        
        sudo apt-get -y install google-chrome-stable

    # get xvfb
        
        sudo apt-get -y install xvfb

    # get unzip
        
        sudo apt-get -y install unzip

    # Get the CORRECT version of chromedriver
    #   -- as stupid as it might be, I kept trying to figure out bugs that had to do w/
    #      using the OS X build that I copied from my laptop to my EC2 instance
    wget https://chromedriver.storage.googleapis.com/2.32/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    mv chromedriver to/where/ever/you/want



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


    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extentions')
    options.add_argument('--enable-popup-blocking')
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    driver.get("https://www.instagram.com/")
    login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
    login_button.click()
    user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
    user_name_elem.clear()
    user_name_elem.send_keys("hdhakernk")
    passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
    passworword_elem.clear()
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    passworword_elem.send_keys("nkdhaker@123")
    passworword_elem.send_keys(Keys.RETURN)
    item = driver.find_element_by_xpath('/html/body/div[3]')
    button_1 = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]')
    dir(driver)
    driver.get_screenshot_as_png("error.png")
    driver.get_screenshot_as_png()
    dir(driver)
    driver.save_screenshot("abc.png")
    driver.save_screenshot("abc.png")
    button_1 = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]')
    button_2=driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]')
    button_3 = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/a')
    driver.find_element_by_xpath('//a[@href="/explore/"]')
    butn driver.find_element_by_xpath('//a[@href="/explore/"]')
    butn =  driver.find_element_by_xpath('//a[@href="/explore/"]')
    butn.click()
    driver.save_screenshot("abc_2.png")
    dir(butn)
    butn.is_displayed()
    butn.is_displayed
    driver.back()
    driver.save_screenshot("abc_3.png")
    butn.is_displayed
    butn.is_displayed()
    butn =  driver.find_element_by_xpath('//a[@href="/explore/"]')
    butn.id
    dir(butn)
    butn.size()
    butn.size
