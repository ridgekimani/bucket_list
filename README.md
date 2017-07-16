# Bucket List
This  your everyday bucket list, a place to keep and discover things that will enrich your life.

[![Build Status](https://travis-ci.org/ridgekimani/bucket_list.svg?branch=master)](https://travis-ci.org/ridgekimani/bucket_list)

### How to set up the project
  #### Downloading the project and installing required packages
      1. Ensure you have a python interpreter installed, preferably python3
      2. Ensure you have git installed
      3. Open the terminal or command prompt on your machine
      4. Since pip is installed, install a virtual environment using  sudo pip install virtualenv on linux machines, pip install virtualenv  on windows and mac based machines.
      5. Navigate to your working directory.
      6. Create a virtual environment by typing virtualenv [name], for example ~$ virtualenv env
      7. Navigate to your project directory
      8. Clone the project via git, using ~$git clone https://github.com/ridgekimani/bucket_list.git or download the zipped file from https://github.com/ridgekimani/bucket_list
      9. Change directory to the virtual environment directory
      10. Type ~$ source bin/activate
      11. Install the packages from the requirements.txt file by typing ~$ pip install -r requirements.txt
         1. You can test whether the correct packages have been installed by opening the python shell and importing the package and testing its version
         2. Example
            >>> import flask
            >>> print (flask.__version__)
            '0.12.2'            
      12. Run tests using ~$ python tests/unit_tests.py
     
