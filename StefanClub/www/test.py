import cx_Oracle


connstr = 'ifsapp/ifsapp@DEV'
conn = cx_Oracle.connect(connstr)
curs = conn.cursor()

curs.execute('select * from site_tab')
print(curs.description)
for row in curs:
    print(row[0])
conn.close()