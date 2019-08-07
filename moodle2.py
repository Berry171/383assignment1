import os
import pymysql
import csv
# read the csv file


# find external ip
r = os.popen("curl ifconfig.me")
ip = r.read()
r.close()

conn = pymysql.connect(host='127.0.0.1',port=3306, user=TopUser,passwd=TopPwd)
cursor=conn.cursor()

list_of_students = [[1,'q','a','23'],[2,'w','e','321'],[3,'ttt','hhh','456']]


for i in list_of_students:
        SQLcmd1=cursor.execute("create database student%s default character set utf8 collate utf8_general_ci;",i[0])
        SQLcmd3=cursor.execute(" create user student%s@'%%' identified by %s;",(i[0],i[3]))
        SQLcmd4=cursor.execute("GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,CREATE TEMPORARY TABLES,DROP,INDEX,ALTER ON student%s.* TO student%s@'%%' IDENTIFIED BY %s;",(i[0],i[0],i[3]))
        SQLcmd6=cursor.execute("flush privileges;")
conn.commit()
cursor.close()
conn.close()

for i in list_of_students:
        os.system("sudo cp -R /opt/moodle /var/www/html/"+str(i[0]))
        os.chdir("/var/www/html/")
        os.chmod(str(i[0]),777)
        os.chdir(str(i[0]))
        if os.path.isfile("config.php"):
                os.system("rm -rf config.php")

        os.system("touch config.php ")
        data="<?php  // Moodle configuration file\n" \
                "unset($CFG);\n" \
                "global $CFG;\n" \
                "$CFG = new stdClass();\n" \
                "$CFG->dbtype    = 'mysqli';\n" \
                "$CFG->dblibrary = 'native';\n" \
                "$CFG->dbhost    = 'localhost';\n" \
                "$CFG->dbname    = 'student"+str(i[0])+"';\n" \
                "$CFG->dbuser    = 'student"+str(i[0])+"';\n" \
                "$CFG->dbpass    = '"+str(i[3])+"';\n" \
                "$CFG->prefix    = 'mdl_';\n" \
                "$CFG->dboptions = array (\n" \
                "  'dbpersist' => 0,\n" \
                "  'dbport' => '',\n" \
                "  'dbsocket' => '',\n" \
                "  'dbcollation' => 'utf8mb4_unicode_ci',\n" \
                ");\n" \
                "$CFG->wwwroot   = 'http://"+str(ip)+"/"+str(i[0])+"';\n" \
				"$CFG->dataroot  = '/var/moodledata';\n" \
				"$CFG->admin     = 'admin';\n" \
				"$CFG->directorypermissions = 0777;\n" \
				"require_once(__DIR__ . '/lib/setup.php');\n"
        content = data
        file = open('config.php', "w")
        file.write(content)
        file.close()
