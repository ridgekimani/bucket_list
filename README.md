# Bucket List
This  your everyday bucket list, a place to keep and discover things that will enrich your life.

[![Build Status](https://travis-ci.org/ridgekimani/bucket_list.svg?branch=master)](https://travis-ci.org/ridgekimani/bucket_list)[![Coverage Status](https://coveralls.io/repos/github/ridgekimani/bucket_list/badge.svg?branch=testing)](https://coveralls.io/github/ridgekimani/bucket_list?branch=master)

### Getting Started
  #### Prerequisites
  1. Ensure you have a python interpreter installed, preferably python3.5 or python3.6
  2. Ensure you have git installed
  3. For running tests, it is prefarable to run them using nosetests, install using pip install nose 
  
  ###Setup and Installation
   Open the terminal or command prompt on your machine
  1. Since pip is installed, install a virtual environment using  sudo pip install virtualenv on linux machines, pip install virtualenv  on windows and mac based machines.
  2. Navigate to your working directory.
  3. Create a virtual environment by typing virtualenv [name], for example ~$ virtualenv env
  4. Navigate to your project directory
  5. Clone the project via git, using ~$git clone https://github.com/ridgekimani/bucket_list.git or download the zipped file from https://github.com/ridgekimani/bucket_list
  6. Change directory to the virtual environment directory
  7. Type ~$ source bin/activate to activate to your virtual environment
  8. Install the packages from the requirements.txt file by typing ~$ pip install -r requirements.txt
     1. You can test whether the correct packages have been installed by opening the python shell and importing the package and testing its version
     2. Example
        >>> import flask
        >>> print (flask.__version__)
        '0.12.2'            
  9. Run tests using (env)~$  nosetests

 The project is running at http://ridge-bucket-list.herokuapp.com/ 
