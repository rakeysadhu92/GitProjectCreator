#!/usr/bin/env python3

"This Project is to give a command and the script should be able to create a new project in the location"

import os
import logging
import argparse
import sys
from github import Github
from six.moves import configparser

##############################CONFIGURATION FILE##################################
config = configparser.ConfigParser()
script_location = os.path.dirname(os.path.realpath(__file__))
config.read(script_location+'/gitcreate.ini')

path = config.get('DEFAULT','local_path')
username = config.get('DEFAULT','git_username')
password = config.get('DEFAULT','git_password')
account_name = config.get('DEFAULT','git_account_name')
log_location = config.get('DEFAULT','logging_location')
ProjName = str(sys.argv[1])

##############################lOGGING RULES#########################################
# create an eventlogger
logger=logging.getLogger('PROJECTCREATE')
logger.setLevel(logging.DEBUG)
#set formatter
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
#creating a file handler
fh = logging.FileHandler(log_location+'gitcreate.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
#Adding Handler
logger.addHandler(fh)

##############################FUNCTIONS#########################################

######################FUNCTION TO HANDLE CHANGES IN CLI#########################
def Cli_Git_Creator():
        ProjectPath = path + ProjName
        os.chdir(ProjectPath)
        open("README.md", 'a').close()
        os.system('git init')
        link='git@github.com:'+account_name+'/'+ProjName+'.git'
        os.system('git remote add origin '+link)
        os.system('git add -A')
        os.system('git status')
        os.system('git commit -m "commit"')
        os.system('git push -u origin master')
        print ("Your Initial commit is Done Successfully")

#####################FUNCTION TO CREATE GIT REPO IN GIT ACCOUNT#################
def Ui_Git_Creator_Api():
    g = Github(username, password)
    logging.info('Successfully loged into the Git account')
    user = g.get_user()
    New_repo = user.create_repo(ProjName)
    logging.info("Successfully Created a new Repo in Git Account")
    print (New_repo)

################################MAIN FUNCTION###################################
def create():
    try:
        if not os.path.exists(path + ProjName):
            print (path+ProjName)
            os.mkdir(path + ProjName)
            logging.info('New Project Folder {} is created '.format(ProjName))
        Ui_Git_Creator_Api()
        Cli_Git_Creator()
    except Exception as e:
        logging.error('There is an Error Occured: {}'.format(e))
        raise

if __name__ == '__main__':
    create()
