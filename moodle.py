import os
import pymysql
import csv
# read the csv file
with open('C:\\Users\\adrienne\\Desktop\\csv_example.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    list_of_students = []
    for row in reader:
        list_of_students.append(row)
    list_of_students.pop(0)
csvFile.close()
# finish downing moodle
os.chdir("/opt")
os.system("sudo git clone https://github.com/moodle/moodle.git")
os.chdir("/opt/moodle")
os.system("sudo git branch -a")
os.system("sudo git branch -track MOODLE_36_STABLE origin/MOODLE_36_STABLE")
os.system("sudo git checkout MOODLE_36_STABLE ")
print("moodle download finished")

#find the top level passwd

os.chdir('/etc/mysql/')
os.system("sudo chmod o+w debian.cnf")
os.system("sudo chmod o+r debian.cnf")

data=""
pwdfile = open('/etc/mysql/debian.cnf',"r")
pwdcontent = pwdfile.read()

pos = pwdcontent.find("[mysql_upgrade]\nhost     = localhost")
lenth=len('[mysql_upgrade]\nhost     = localhost')
UAP=(pwdcontent[pos+lenth:])

pos_user=UAP.find('user     = ')
pos_pwd=UAP.find('password = ')
pos_socket=UAP.find('socket')

TopUser=UAP[pos_user+len('user     = '):pos_pwd]
TopPwd=UAP[pos_pwd+len('password = '):pos_socket]


os.system("sudo chmod o-w debian.cnf")
os.system("sudo chmod o-r debian.cnf")

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
os.system("sudo mkdir /var/moodledata")
os.system("sudo chown -R www-data /var/moodledata")
os.system("sudo chmod -R 777 /var/moodledata")


# find external ip
r = os.popen("curl ifconfig.me")
ip = r.read()
r.close()


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
