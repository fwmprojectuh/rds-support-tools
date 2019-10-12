
#!/usr/bin/env python

import pymysql
import logging
import traceback
from os import environ

address=environ.get('ENDPOINT')
port=environ.get('PORT')
user=environ.get('DBUSER')
pw=environ.get('DBPASSWORD')
database=environ.get('DATABASE')

insert="INSERT INTO fwmprojectuh.floodwaterdata (Reading) VALUES (210)"

logger=logging.getLogger()
logger.setLevel(logging.INFO)

def make_connection():
    return pymysql.connect(host=address, user=user, passwd=pw,
        port=int(port), db=database, autocommit=True)

def log_err(errmsg):
    logger.error(errmsg)
    return {"body": errmsg , "headers": {}, "statusCode": 400,
        "isBase64Encoded":"false"}

logger.info("Cold start complete.") 

def handler(event,context):

    try:
        cnx = make_connection()
        cursor=cnx.cursor()
        
        try:
            cursor.execute(insert)
        except:
            return log_err ("ERROR: Cannot execute cursor.\n{}".format(
                traceback.format_exc()) )

        try:
            results_list=[]
            for result in cursor: results_list.append(result)
            print(results_list)
            cursor.close()

        except:
            return log_err ("ERROR: Cannot insert data.\n{}".format(
                traceback.format_exc()))


        return {"body": str(results_list), "headers": {}, "statusCode": 200,
        "isBase64Encoded":"false"}

    
    except:
        return log_err("ERROR: Cannot connect to database from handler.\n{}".format(
            traceback.format_exc()))


    finally:
        try:
            cnx.close()
        except: 
            pass 

if __name__== "__main__":
    handler(None,None)
