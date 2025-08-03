"""Class to configure the test_speed program
Using json (sigh)"""


import json
import os
import sys
import platform
import socket
import inspect
from loguru import logger

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class MyConfig():

    def __init__(self,config_file):
        """ config_file contains all the infor for calory program"""

        logger.info("Setting up configuration \n \n")
       
        
        # Open config file
        #print('Directory Name:     ', os.path.dirname(config_file))
       

        if os.path.exists(config_file) :
            self.ReadJson(config_file)
        else:
            logger.error(" Config file does not exist, exiting   %s  " % config_file)
            sys.exit(0)

    def ReadJson(self,file_path):

        logger.info("reading config file %s \n" % file_path)    
        with open(file_path, "r") as f:
            myconf = json.load(f)

            self.DecodeVariables(myconf)

    def DecodeVariables(self,jsondict):
        """decodes the json dictionary in to variables"""

        #bold face begin and end
        bfb = '\033[1m'
        bfe = '\033[0m'
        TX = color
        #these are depending on the operating system
        #however the structure below the hoe directory is alsways the same
        #topdir
        #-src,
        #-data,
        #-log
        #-doc
        #-confidir
        mysystem = platform.system()
        self.topdir = jsondict[mysystem]['topdir']
        self.srcdir = self.topdir+jsondict[mysystem]['srcdir']
        self.datadir = self.topdir+jsondict[mysystem]['datadir']
        self.logdir = self.topdir+jsondict[mysystem]['logdir']
        self.doc_dir =self.topdir+jsondict[mysystem]['doc_dir']
        self.conf_dir = self.topdir+jsondict[mysystem]['conf_dir']

        self.debug = jsondict["Control"]["debug"]
        cryptofile = jsondict["Control"]["cryptofile"]
        #decode cryptofile
        self.cryptofile = self.conf_dir+cryptofile

        if os.path.exists(self.cryptofile):
                with open(self.cryptofile, 'r') as file:
                    password = file.read().rstrip()
                    self.db_pwd = password
        else:
            logger.error("crypto file %s  does not exist" % self.cryptofile)
            sys.exit(0)


        self.db_user = jsondict["Control"]["db_user"]
        self.db_name = jsondict["Control"]["db_name"]
        self.db_address = jsondict["Control"]["db_address"]
        #currently only QPSQL is supported
        self.db_system = jsondict["Control"]["db_system"]
        # the next two vaiables are only used if we run in "both" mode
            #test if first key is working
        self.ingred_table = jsondict["Control"]["ingred_table"] #choices are currently ingredients or swiss_food
 
        self.ingredients_suppress_columns = jsondict["graphics"]["ingredients_suppress_columns"]
        self.swiss_food_suppress_columns = jsondict["graphics"]["swiss_food_suppress_columns"]
        self.recipes_suppress_columns = jsondict["graphics"]["recipes_suppress_columns"]

        self.disk_table = jsondict["disk_table"]["column"]
        self.directory_table = jsondict["directory_table"]["column"]
        self.file_table = jsondict["file_table"]["column"]
       
        #Possible loglevels
        # DEBUG
        # INFO
        # WARNING
        # ERROR
        # CRITICAL
        
        #Output choices
        # screen
        # outfile
        # both

        if "loglevel" in jsondict["logging"].keys() :
            self.log_level = jsondict["logging"]["loglevel"] 
        else:
            self.log_level = "INFO"

        
        self.log_output = jsondict["logging"]["output"] 
 
        if "log_conf_file" in jsondict["logging"].keys() :
            self.log_conf_file = self.conf_dir+jsondict["logging"]["log_conf_file"] 
        else:
            frame = inspect.currentframe()
            prefix = TX.BOLD +TX.RED+'|'+frame.f_code.co_name+'>'+'no logger config file'+TX.END
            print(prefix)
            sys.exit(0)
             
        #here we get the logging varaibles:
                

        print('\n\n ***************** configuration**************\n')
        print(' We are running on platform ' , mysystem, '\n')

        print('Sourcedir            ',self.srcdir)
        print('Datadir              ',self.datadir)
 
        print('***************************** end of configuration***************\n\n')





if __name__ == '__main__':
    mysystem = platform.system()

    if mysystem == 'Darwin':
        conf_dir = '/Users/klein/git/diskdb/config/'
    elif mysystem == 'Linux':
        conf_dir = '/home/klein/git/diskdb/config/'
    else:
        print(' Thios os is not supported %s' % mysystem)
    config_file = conf_dir + 'config_disk_db.json'
    MyC = MyConfig(config_file)
