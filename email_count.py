import sqlite3 as sql

conx = sql.connect('emaildb.sqlite')
curs = conx.cursor()

curs.execute('DROP TABLE IF EXISTS Counts')

curs.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

file = input('Enter file name:')
# if len(file) < 1: print('ERROR, FILE NOT FOUND')
fh = open(file).readlines()

for line in fh:
    if not line.startswith('From: '): continue
    org = line.split('@')[1].strip()


    curs.execute('SELECT count FROM Counts WHERE org = ?', (org,))
    row = curs.fetchone()

    if row is None:
        curs.execute(''' INSERT INTO Counts (org, count) VALUES (?, 1)''', (org,))
    else:
        curs.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))
    
    conx.commit()
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in curs.execute(sqlstr):
    print(row[0], row[1])

curs.close()