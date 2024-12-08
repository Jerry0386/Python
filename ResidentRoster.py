import db
from business import Resident, Stay, residentRoster
from datetime import datetime


# adds resident to database
def addResident(residents):
  RK = 0
  lastName = input("Last Name: ").title()
  firstName = input("First Name: ").title()
  dateOfBirth = input("Date of Birth (mm/dd/yyyy): ")
  formattedDOB = formatDate(dateOfBirth)
  if not formattedDOB:
    print("Cannot add resident due to invalid date of birth format.")
    return
  
  resident = Resident(RK, lastName, firstName, formattedDOB)
  residents.add(resident)
  db.addResident(resident)
  

# adds stay to database  
def addStay(stays):
  SK = 0
  RK = int(input("Enter RK: "))
  arrivalDate = input("Arrival Date (mm/dd/yyyy): ")
  
  #Validate and format date
  formattedArrivalDate = formatDate(arrivalDate)
  if not formattedArrivalDate:
    print("Cannot add stay due to invalid date.")
    return
  
  departDate = ""
  stay = Stay(SK, RK, formattedArrivalDate, departDate)
  stays.add(stay)
  db.addStay(stay)
  

# adds departure  
def addDepart(stays):
  SK = int(input("Enter SK: "))
  RK = 0
  arrivalDate = 0
  departDate = input("Departure Date (mm/dd/yyyy): ")
  
  #Validate and format date
  formattedDepartDate = formatDate(departDate)
  if not formattedDepartDate:
    print("Cannot add departure due to invalid date.")
    return
  
  activeStay = 0
  
  stay = Stay(SK, RK, arrivalDate, formattedDepartDate, activeStay)
  stays.add(stay)
  db.addDepart(stay)
  print(f"Departure added.")

# date formatting
def formatDate(dateStr):
  try:
    return datetime.strptime(dateStr, "%m/%d/%Y").strftime("%Y-%m-%d")
  except ValueError:
    print("Invalid date format. Please use mm/dd/yyyy.")
    return None
  
def displaySeparator():
  print('{:=^65}'.format(''))

# displays active stays with resident name  
def displayActiveStays(activeStays):
    if len(activeStays) == 0:
        print("There are no active stays.\n")
    else:
        print("\nStays:")
        print(f"{'SK ':<5}{'RK ':<5}{'First Name ':<25}{'Last Name ':<25}{'Arrival Date ':<15}{'Departure Date ':<15}")
        
        for activeStay in activeStays:
            # Access attributes of the Stay object directly
            firstName = activeStay.firstName if activeStay.firstName is not None else ""
            lastName = activeStay.lastName if activeStay.lastName is not None else ""
            arrivalDate = activeStay.arrivalDate if activeStay.arrivalDate is not None else ""
            departDate = activeStay.departDate if activeStay.departDate is not None else ""

            # Print the values with proper formatting
            print(f"{activeStay.SK:<5}{activeStay.RK:<5}{firstName:<25}{lastName:<25}{arrivalDate:<15}{departDate:<15}")
            print()
            
# displays all stays and whether they are active            
def displayAllStays(stays):
  if len(stays) == 0:
    print("There have been no stays.\n")
  else:
    print("\nStays:")
    print(f"{'SK ':<5}{'RK ':<5}{'First Name ':<25}{'Last Name ':<25}{'Arrival Date ':<15}{'Departure Date ':<15}{'Active ':<10}")
    for stay in stays:
      firstName = stay.firstName if stay.firstName is not None else ""
      lastName = stay.lastName if stay.lastName is not None else ""
      arrivalDate = stay.arrivalDate if stay.arrivalDate is not None else ""
      departDate = stay.departDate if stay.departDate is not None else ""
      
      if stay.activeStay == 1:
        active = 'Yes'
      else:
        active = 'No'
    
      print(f"{stay.SK:<5}{stay.RK:<5}{firstName:<25}{lastName:<25}{arrivalDate:<15}{departDate:<15}{active:<10}")
      print()    

# displays all existing residents in database
def displayAllResidents(residents):
  if len(residents) == 0:
    print("There are no residents.\n")
  else:
    print("\nResidents:")
    print(f"{'RK ':<5}{'First Name ':<25}{'Last Name ':<25}{'DOB ':<15}")
    for resident in residents:
      print(f"{resident.RK:<5}{resident.firstName:<25}{resident.lastName:<25}{resident.dateOfBirth:<15}")
      print()

# displays all residents currently staying
def displayActiveResidents(activeResidents):
  if len(activeResidents) == 0:
    print("There are no residents.\n")
  else:
    print("\nResidents:")
    print(f"{'RK ':<5}{'First Name ':<25}{'Last Name ':<25}{'DOB ':<15}")
    for resident in activeResidents:
      print(f"{resident.RK:<5}{resident.firstName:<25}{resident.lastName:<25}{resident.dateOfBirth:<15}")
      print()

def displayTitle():
  displaySeparator()  
  print('{:^65}'.format("Resident and Stay Management System"))
  displaySeparator()
  

def displayMenu():
  print("MENU")
  print("1  Add Resident")
  print("2  Add Stay")
  print("3  Add Departure")
  print("4  View Current Residents")
  print("5  View All Residents")
  print("6  View Active Stays")
  print("7  View Stay History")
  print("8  EXIT")

def main():

# Run connection in db.py and add get values for lists
  db.connect()
  activeStays = db.getActiveStays()
  stays = db.getStays()
  residents = db.getResidents()
  activeResidents = db.activeResidents()

  displayTitle()
  displayMenu()

  while True:
    try:
      option = int(input("Menu Option: "))
    except ValueError:
      option = -1
      
    if option == 1:
      addResident(residents)
      activeResidents = db.activeResidents()
      residents = db.getResidents()
    elif option == 2:
      addStay(stays)
      activeStays = db.getActiveStays()
      stays = db.getStays()
    elif option == 3:
      addDepart(stays)
      activeStays = db.getActiveStays()
      stays = db.getStays()
    elif option == 4:
      displayActiveResidents(activeResidents)
    elif option == 5:
      displayAllResidents(residents)
    elif option == 6:
      displayActiveStays(activeStays)
    elif option == 7:
      displayAllStays(stays)
    elif option == 8:
      db.close()
      print("Goodbye!")
      break
    else:
      print("Not a valid option. Try again.")
      displayMenu()
    
if __name__ == "__main__":
  main()

