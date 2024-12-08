from dataclasses import dataclass

# class to store resident data
@dataclass
class Resident:
  RK:int = 0
  lastName:str = ""
  firstName:str = ""
  dateOfBirth:str=""
  
  @property
  def fullName(self):
    return f"{self.firstName} {self.lastName}"

# class to store stay data  
@dataclass
class Stay:
  SK:int = 0
  RK:int = 0
  arrivalDate:str = ""
  departDate:str = ""
  activeStay:int = 1
  firstName:str = ""
  lastName:str = ""
  
  @property 
  def stayDetail(self):
    return f"{self.arrivalDate} {self.departDate}"

# class to create a list of residents  
class residentRoster:
  def __init__(self):
    self.__list = []

    
  @property
  def count(self):
    return len(self.__list)
  
  def add(self, resident):
    return self.__list.append(resident)
  
  def get(self, number):
    return self.__list[number-1]
  
  def __iter__(self):
    for resident in self.__list:
      yield resident
  def __len__(self):
    return len(self.__list)

# class to create a list of stays      
class stayList:
  def __init__(self):
    self.__list = []
    
  @property
  def count(self):
    return len(self.__list)
  
  def add(self, stay):
    return self.__list.append(stay)
  
  def get(self, number):
    return self.__list[number-1]
  
  def __iter__(self):
    for stay in self.__list:
      yield stay
  def __len__(self):
    return len(self.__list)