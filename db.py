import sqlite3

from contextlib import closing
from business import Resident, residentRoster, Stay, stayList

conn = None

def connect():
  global conn
  if not conn:
    DB_FILE = "resident_db.sqlite"
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    
def close():
  if conn:
    conn.close()

# Creates Resident object from database row    
def makeResident(row):
  return Resident(row["RK"], row["lastName"],
                  row["firstName"], row["dateOfBirth"])
  
# Creates Stay object from database row
def makeStay(row):
    return Stay(
        SK=row["SK"],
        RK=row["RK"],
        arrivalDate=row["arrivalDate"] if row["arrivalDate"] is not None else "",
        departDate=row["departDate"] if row["departDate"] is not None else "",
        activeStay=row["activeStay"],
        firstName=row["firstName"] if row["firstName"] is not None else "",
        lastName=row["lastName"] if row["lastName"] is not None else ""
    )

# Queries database for all residents and adds them to residentRoster()    
def getResidents():
  query = '''SELECT RK, lastName, firstName, dateOfBirth
             FROM residentTable
             ORDER BY lastName, firstName ASC'''
  with closing(conn.cursor()) as c:
    c.execute(query)
    results = c.fetchall()
    
  residents = residentRoster()
  for row in results:
    resident = makeResident(row)
    residents.add(resident)
  return residents

# Queries database for active residents and adds them to residentRoster()
def activeResidents():
  query = '''SELECT r.RK, r.lastName, r.firstName, r.dateOfBirth
             FROM residentTable as r LEFT JOIN stayTable as s
             ON r.RK = s.RK
             WHERE s.activeStay = 1
             ORDER BY r.lastName, r.firstName'''
  with closing(conn.cursor()) as c:
    c.execute(query)
    results = c.fetchall()
    
    residents = residentRoster()
    for row in results:
      resident = makeResident(row)
      residents.add(resident)
    return residents

# Queries database for inactive residents and adds them to residentRoster()
def inactiveResidents():
  query = '''SELECT r.RK, r.lastName, r.firstName, r.dateOfBirth
             FROM residentTable as r LEFT JOIN stayTable as s
             ON r.RK = s.RK
             WHERE s.activeStay = 0'''
  with closing(conn.cursor()) as c:
    c.execute(query)
    results = c.fetchall()
    
    residents = residentRoster()
    for row in results:
      resident = makeResident(row)
      residents.add(resident)
    return residents

# checks to see if resident already exists and if they don't, inserts the resident to residentTable  
def addResident(resident):
  
  sqlCheck = '''SELECT COUNT(*)
                FROM residentTable
                WHERE lastName = ? AND firstName = ? AND dateOfBirth = ?'''
  with closing(conn.cursor()) as c:
        c.execute(sqlCheck, (resident.lastName, resident.firstName, resident.dateOfBirth))
        result = c.fetchone()
        if result[0] > 0:
            print(f"Resident {resident.fullName} already exists in the database.")
            return

  sql = '''INSERT INTO residentTable
            (lastName, firstName, dateOfBirth)
           VALUES
            (?,?,?)'''
  with closing(conn.cursor()) as c:
    c.execute(sql, (resident.lastName, resident.firstName, resident.dateOfBirth))
    conn.commit()
    print(f"{resident.fullName} was added.\n")

# Queries database for resident and stay information on all stays      
def getStays():
  query = '''SELECT s.SK, s.RK, r.lastName, r.firstName, s.arrivalDate, s.departDate, s.activeStay
             FROM stayTable as s LEFT JOIN residentTable as r
             ON s.RK = r.RK
             ORDER BY s.SK ASC'''
  with closing(conn.cursor()) as c:
    c.execute(query)
    results = c.fetchall()
    
  stays = stayList()
  for row in results:
    stay = makeStay(row)
    stays.add(stay)
  return stays

#Queries database for resident and stay information for active stays
def getActiveStays():
  query = '''SELECT s.SK, s.RK, s.arrivalDate, s.departDate, s.activeStay, r.lastName, r.firstName
             FROM stayTable as s LEFT JOIN residentTable as r
             ON s.RK = r.RK
             WHERE s.activeStay = 1
             ORDER BY s.SK ASC;'''
  with closing(conn.cursor()) as c:
    c.execute(query)
    results = c.fetchall()
    
  stays = stayList()
  for row in results:
      stay = makeStay(row)
      stays.add(stay)
  return stays

# adds a stay to the database      
def addStay(stay):
  
  sqlCheck = '''SELECT COUNT(*)
                FROM stayTable
                WHERE activeStay = 1 AND RK = ?'''
  
  with closing(conn.cursor()) as c:
    c.execute(sqlCheck, (stay.RK,))
    result = c.fetchone()
    if result[0] > 0:    
      print(f"Resident already has an active stay.")
      return
  sql = '''INSERT INTO stayTable
            (RK, arrivalDate)
           VALUES
            (?,?)'''
  with closing(conn.cursor()) as c:
    c.execute(sql, (stay.RK, stay.arrivalDate))
    conn.commit()
    print(f"Stay added.")

# adds departure date to the database    
def addDepart(stay):
  sql = '''UPDATE stayTable
           SET departDate = ?, activeStay = ?
           WHERE SK = ?'''
  with closing(conn.cursor()) as c:
    c.execute(sql, (stay.departDate, stay.activeStay, stay.SK))
    conn.commit()
    print(f"Rows updated: {c.rowcount}")
    
