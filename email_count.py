import sqlite3 as sql

conx = sql.connect('emaildb.sqlite')
curs = conx.cursor()

curs.execute('DROP TABLE IF EXISTS Counts')

curs.execute('CREATE TABLE Counts (email TEXT, count INTEGER)')

file = input('Enter file name:')
# if len(file) < 1: print('ERROR, FILE NOT FOUND')
fh = open(file).read().split('\n')

for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    curs.execute('SELECT count FROM Counts WHERE email = ?', (email,))
    row = curs.fetchone()

    if row is None:
        curs.execute(''' INSERT INTO Counts (email, count) VALUES (?, 1)''', (email,))
    else:
        curs.execute('UPDATE Counts SET count = count + 1 WHERE email = ?', (email,))
    
    conx.commit()
sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in curs.execute(sqlstr):
    print(row[0], row[1])

curs.close()