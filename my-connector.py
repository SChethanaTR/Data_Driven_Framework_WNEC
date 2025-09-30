import mysql.connector


mydb = mysql.connector.connect(
    host='10.99.13.117',
    user='wnec',
    password='reut3r5',
    port='3306',
    database='wne'
)

mycursor = mydb.cursor()

mycursor.execute('Select * from distribution_configuration_ftp')

rlob = mycursor.fetchall()

for rlo in rlob:
    print(rlo)
