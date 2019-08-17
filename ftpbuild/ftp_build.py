import os
import csv
import random
password=[]
for i in range(100000,999999):
    password.append(i)
password=random.sample(password,200)

os.system("sudo -s")
os.system("apt-get install vsftpd")
r = os.popen("curl ifconfig.me")
ip = r.read()
r.close()

ftp_conf = open('ftp_conf.txt',"r")
new_content = ftp_conf.read()
ftp_conf.close()
position=new_content.find("/etc/pam.d/vsftpd")
modified= open('/etc/vsftpd.conf',"w")
modified.write(new_content[0:position]+"\n"+"pasv_address="+ip)
modified.close()
os.system("chmod a-w /var/www/html")

pam = open('/etc/pam.d/vsftpd',"w")
pam.write(new_content[position+18:len(new_content)])
pam.close()

os.mkdir("/etc/userconfig")

with open('test_examples.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    # create empty list
    list_of_students = []
    # for each student, append as list to list (list of lists)
    for row in reader:
        list_of_students.append(row)
        # Remove metadata from top row
    list_of_students.pop(0)

i=0
for student in list_of_students:

    os.system("useradd -m"+student[0])
    os.system("echo "+student[0]+":"+password[i]+"| chpasswd")
    os.system("chown -R " + student[0] + ":" + student[0] + "/var/www/html/" + student[5])
    os.system("chmod -R 777 /home/"+student[0])
    os.system("touch /etc/userconfig/"+student[0])
    user = open("/etc/userconfig/"+student[0], "w")
    user.write("local_root=/var/www/html/"+student[5])
    user.close()
    i=i+1


os.system("useradd -m teacher")
os.system("echo teacher:teacher| chpasswd")
os.system("chown -R teacher /var/www/html")
os.system("chmod -R 777 /home/teacher")
os.system("touch /etc/userconfig/teacher")
user = open("/etc/userconfig/teacher", "w")
user.write("local_root=/var/www/html/")
user.close()

os.system("sudo service vsftpd restart")


