#This is a little play program to start using psycopg
# it needs to have a running osptgres server


import sys
import psycopg as PG
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from loguru import logger
import config_disk_db as CD
import disk_info as DI


class MY_DB(object):
    def __init__(self,Title =  None,db_name = None, db_user = None, db_pwd = None, db_system = None , db_host = None, config_file = None):
        super().__init__()

        self.config_file = config_file


# start logger system
        self.SetupSystem()



    def add_columns(self,table_name = None, columns = None):

        if(self.check_table_exists(table_name=table_name)):
            sql_command =''
            test = self.column_command(columns)
            temp = self.column_command(columns)
            for k in range(len(temp)):
                sql_command = '''ALTER TABLE '''+table_name +' ADD COLUMN ' +temp[k]
                print(sql_command)
                self.MyCurs.execute(sql_command)
                self.MyConn.commit()
                
            
        else:
            logger.error(' table %s does not exist' % table_name)

 
        return
    
    def alter_table(self,command):
        """altesr the given table with the given command
        The command has to be already ready to pass to the psycogg system
        and is typical
        ALTER TABLE disk_table ADD CONSTRAINT name_constraint UNIQUE ('disk_name')
        """
        try:
            self.MyCurs.execute(command)
            self.MyConn.commit()
        except Exception as e:
            logger.error(e)
        
        return


    def check_table_exists(self,table_name = None, schemaname = 'public'):
        """ a psql check if table exists"""

        sql_command = '''SELECT EXISTS ( SELECT 1 FROM pg_tables WHERE schemaname =  \''''+schemaname+  '''\' AND tablename = \''''+table_name +'''\')''' 
        self.MyCurs.execute(sql_command)
        if self.MyCurs.fetchone()[0]:
            logger.info("table %s exists" % table_name)
            return True
        else:
            logger.info("table %s does not exist" % table_name)
            return False
 

        return

    def close_system(self):
         self.MyConn.commit()
         self.MyCurs.close()
         self.MyConn.close()
         logger.info('all closed')



    def column_command(self,columns):
        mycommand = []
        sql_command = ''
        print(len(columns))
        for k in range(0,len(columns)-1,3):
            mycommand.append(columns[k]+' '+columns[k+1]+' '+columns[k+2])

 
        return mycommand
 

    def connect_db(self,dbname = None, password = None , user = None, host = None):
        """Establish connection to database"""



        try:
            MyConn = PG.connect(dbname = self.db_name, password = self.db_pwd , user = self.db_user , host = self.db_host)
            self.MyCurs = MyCurs = MyConn.cursor()
            #MyConn.autocommit = True

        except:
            MyConn = PG.connect( password = self.db_pwd , user = self.db_user , host = self.db_host)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!important!!!!!!!!!!!!!!!!
        # to get rid of the "cannot run in a transaction block"
            ISOLATION_LEVEL_AUTOCOMMIT = True #contary to AI; needs to be set to True
            MyConn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            MyConn.autocommit = True
            self.MyCurs = MyCurs = MyConn.cursor()

            self.MyCurs.execute(f"CREATE DATABASE {self.db_name};")
        
        self.MyConn = MyConn

        # check if database exists:

        stat =  '''select exists(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower(\''''+self.db_name+'\'))''';

        MyCurs.execute(stat)


        if MyCurs.fetchone()[0]:
            logger.info("database %s exists" % self.db_name)
            return True
        else:
            logger.info("database %s does not exist" % self.db_name)
            return False
 
        return
    
    def create_db(self,db_name = None,db_user = None):
        """ Creates database"""

        stat = '''CREATE DATABASE '''+db_name

        self.MyCurs.execute(stat)

        return
    
   



    def create_table(self,table_name = None, columns = None):
        """ create a table with 2 dimensional list columns, 
        is of the form [variable name,type,constraint]"""
        sql_command_new = ''
        sql_command = ''
        if(table_name == 'disk_table'):
            temp = self.column_command(self.CD.disk_table)
        elif(table_name == 'directory_table'):
            temp = self.column_command(self.CD.directory_table)
        elif(table_name == 'file_table'):
            temp = self.column_command(self.CD.file_table)
        else:
            logger.error("table %s not known" % table_name)
           
             
    
        
 #       sql_command_new = 'CREATE TABLE IF NOT EXISTS '+table_name+'  ('+self.column_command(columns)+' )'
        for k in range(len(temp)-1):
            sql_command =sql_command + temp[k] +','
            sql_command_new ='CREATE TABLE IF NOT EXISTS '+table_name+' ( '+sql_command+temp[k+1]+' );'
        self.MyCurs.execute(sql_command_new)
        
        self.MyConn.commit()
        return
    


    def create_columns(self,conf_column = None):
        """this takes the json columns and form it again into lists for the create Table"""
        #conf_column = self.CD.disk_table
        temp_column = []

        a = []

        for k in range(0,len(conf_column)-1,3):
            a= conf_column[k], conf_column[k+1], conf_column[k+2]
            temp_column.append(a)

        return temp_column

    def delete_db(self,db_name = None):

        stat = '''DROP DATABASE IF EXISTS '''+db_name 
        logger.warning("You are deleting database %s" % db_name)
        #self.MyCurs.close()
        self.MyCurs.execute(stat)
        return

   
    
    def fill_tables(self):
        """fills the related tables of the disk database. There are currently three tables, namely
        disk_table: disk_id,disk_name,filesystem,size,used,free
        dir_table: id, disk_id(connected to id from disk_table) directory,level
        file_table: id, dir_id(connected to id from dir_table),filename,size
        
        
        example:

        # 1. Insert into the parent table (authors)
        author_name = "J.K. Rowling"
        cur.execute("INSERT INTO authors (name) VALUES (%s) RETURNING author_id;", (author_name,))
        author_id = cur.fetchone()[0]  # Get the newly generated author_id

        # 2. Insert into the child table (books) using the retrieved author_id
        book_title_1 = "Harry Potter and the Sorcerer's Stone"
        book_title_2 = "Harry Potter and the Chamber of Secrets"

        cur.execute("INSERT INTO books (title, author_id) VALUES (%s, %s);", (book_title_1, author_id))
        cur.execute("INSERT INTO books (title, author_id) VALUES (%s, %s);", (book_title_2, author_id))

        
        
        """
        disk = "samsung4"
        fs = "afps"
        si = 2000
        us = 500
        fr = 1500



 
        sql_statement = """INSERT INTO disk_table (disk_name , filesystem , size, used, free   ) VALUES (%s , %s, %s,%s,%s )  RETURNING disk_id ;"""
        data = (disk,fs,si,us,fr)


        try:
            self.MyCurs.execute(sql_statement,data)
            self.MyCurs.fetchone() 

            # don't forget to commit changes to database
            self.MyConn.commit()
        except Exception as e:
            logger.error(e)
        return

    def find_drives(self):
        """this calls the find_drives ind disk info"""

        self.DI.find_drives()

        logger.info('external drives %s ' % self.DI.external_drives)
        
        return


    def get_directories(self):
        a = self.DI.get_dir_entries(path=k)
        
        return
    
    def get_all_dirs(self,path=None):
        """finds all directories and file to max_depth"""

        #first get max level
        max_depth = self.DI.get_max_directory_level(path)

        #max_depth = self.CD.max_depth
        myroot,dir_list,files = self.DI.find_all_dirs(path=path,max_depth=max_depth)
        return
    
    def SetupLogger(self):


        #logger.remove(0)
        #now we add color to the terminal output
        logger.add(sys.stdout,
                colorize = True,format="<green>{time}</green>    {function}   {line}    {level}     <level>{message}</level>" ,
                level = "DEBUG")



        fmt =  "{time} - {name}-   {function} -{line}- {level}    - {message}"
        logger.add('info.log', format = fmt , level = 'INFO',rotation="1 day")


        # set the colors of the different levels
        logger.level("INFO",color ='<black>')
        logger.level("WARNING",color='<green>')
        logger.level("ERROR",color='<red>')
        logger.level("DEBUG",color = '<blue>')
 
        return
 

    def SetupSystem(self):
        """instantiates and starts all the config stuff"""

        logger.info('starting up system')

        # first get configuration
        self.CD = CD.MyConfig('/Users/klein/git/diskdb/config/config_disk_db.json')
        self.db_name    = self.CD.db_name
        self.db_user    = self.CD.db_user
        self.db_system  = self.CD.db_system
        self.db_host    = self.CD.db_address
        self.db_pwd     = self.CD.db_pwd


        #instantiate the disk info system
        
        self.DI = DI.disk_info()


    

if __name__ == "__main__":
    db_name = 'disk'
    #test = MY_DB(db_name = db_name,db_user = 'klein',db_host = 'localhost' , db_system = 'PSQL')
    test = MY_DB()
    test.connect_db()

    # exapmple for altering table
    #alter_command = "ALTER TABLE disk_table ADD CONSTRAINT name_constraint UNIQUE (disk_name);"  
    #test.alter_table(alter_command)
 
 
    #test.create_db(db_name = 'disk',db_user = 'klein')

    
    #columns1=[['disk_test2','varchar[30]',''],['name2','varchar[40]','NOT NULL'],['size2','NUMERIC','']]
    
    #test.create_table('disk_table')
    #test.create_table('directory_table')
    #test.create_table('file_table')

    #test.fill_tables()


    #test.find_drives()
    test.get_all_dirs(path='/Volumes/samsung4')
    #test.add_columns(table_name='disk_table',columns=columns1)
    #test.delete_db(db_name = 'disk')
    test.close_system()

