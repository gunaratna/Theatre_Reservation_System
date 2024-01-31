import math
import datetime
import ast


movieShowTime = {'1': '09:00 - 12:00','2': '13:00 - 16:00','3': '17:00 - 20:00'}
hallType = ['S','M','L']


#********************************************************''
# this function read the users data from a file 'userList'
def readUserData():
    
    with open('C:/MOOC/Theatre Management System/userList.txt', 'r') as file:
        file_content = file.read()
        dict_str = file_content.split('=', 1)[1].strip() 
        uData = ast.literal_eval(dict_str)
  
    return uData
    
#********************************************************************
# Present a list of movies

def movieList(fname):
    # read and send movie list
    with open(fname, 'r') as file:
        file_content = file.read()
        parts = file_content.split('\n\n')
        movieSelect = ast.literal_eval(parts[0].split('=', 1)[1].strip())
        hallReservations = ast.literal_eval(parts[1].split('=', 1)[1].strip())
    
        file.close()
    
    return movieSelect, hallReservations
    
#*******************************************************************************
# Login     

def login():
    
    # Function to read the key-value pairs from the file

    uData = readUserData()

    while(True):
        uname = input("Username:")
                
        if uname in uData:
            pwd = input("Password:")
            while(uData[uname]!=pwd):
                print(f"Incorrect Password. Please, enter correct passwoord for {uname}")
                pwd = input("Password:")
            print("Login Successful")
            return True, uname
            break       
        else:
            print("User is not found")
            print("Register as new User")
            registerCustomer(uData)
 
#*********************************************************************'
# Date selection
               
def dateSelect():
    while True:  
        dateInput = input('Enter a date formatted as YYYY/MM/DD: ')
  
        
        dt = datetime.datetime.strptime(dateInput, "%Y/%m/%d")
        
    
        minDate = datetime.date.today() + datetime.timedelta(days=3)
        if dt.date() >= datetime.date.today() and dt.date() <= minDate:
            break
        
        else:
            print("Enter todays date or maximum 3 days ahead from today")
        
  
    return dt.date()
#********************************************************************
# Customer registration

def registerCustomer(uData):
    # Customer registration in the reservation system  
    while True:
        uname = input("Enter Username: ")
        if uname not in uData:
            pwd = input("Enter Password: ")
            uData[uname] = pwd
            print("User creation successful!")
            break
        else:
            print("This username already exists. Please, enter another username")
     
    with open('C:/MOOC/Theatre Management System/userList.txt', 'w') as file:
        file.write("userList = ")
        file.write(str(uData))
          

#************************************************************************
# Admin adds a movie to the screeting time and hall

def addMovie():
   
    print("select the effective date")
    hallTypeLst = ['S','M','L']
    while True:  
        dateInput = input('Enter a date formatted as YYYY/MM/DD: ')
  
        try:
            dt = datetime.datetime.strptime(dateInput, "%Y/%m/%d")
      
            minDate = datetime.datetime.today() + datetime.timedelta(days=3)
            
            if dt.date() > minDate.date():
                break
            else:
                print("Enter a date greater than 3 days from today")
      
        except:
            print("Error, try again")
        
    print("select the type of Hall")
    while True:
        hallInput = input("Enter S for Small, M for Medium, L for Large hall: ")
        try:
            if hallInput in hallTypeLst:
                break
        except:
            print("Enter correct input for hall type")
    
    for key, values in movieShowTime.items():
        print(f"Show Time Code: {key}. Show Time: {values}" )
            
    while True:
        selectedShowTime = int(input("Select showTime out of code 1 or 2 or 3: "))
        if selectedShowTime in [1,2,3]:
            selectedShowTime = str(selectedShowTime)
            break
       
    mName = input("Enter the movie name: ")
    
    selectedDate = dt.date()
    filename = 'C:/MOOC/Theatre Management System/' + str(selectedDate.day) + str(selectedDate.strftime("%b")) + '.txt'
    
    mDict, hallReservations = movieList(filename)
 
    for screenTime, hallTypes in mDict.items():
        for hallType, movie in hallTypes.items():
            if hallType == hallInput and screenTime == selectedShowTime:
                mDict[screenTime][hallType] = mName
    
    with open(filename, 'w') as file:
        file.write("movieSelect = ")
        file.write(str(mDict))
        file.write("\n\nhallReservations = ")
        file.write(str(hallReservations))
        
  
    return True     
      
#************************************************************************
# Admin add an extra screening time

def addScreeningTime():
    print("select the effective date")
    hallTypeLst = ['S','M','L']
    while True:  
        dateInput = input('Enter a date formatted as YYYY/MM/DD: ')
  
        try:
            dt = datetime.datetime.strptime(dateInput, "%Y/%m/%d")
      
            minDate = datetime.datetime.today() + datetime.timedelta(days=3)
            
            if dt.date() > minDate.date():
                break
            else:
                print("Enter a date greater than 3 days from today")
      
        except:
            print("Error, try again")
        
    print("select the type of Hall")
    while True:
        hallInput = input("Enter S for Small, M for Medium, L for Large hall: ")
        try:
            if hallInput in hallTypeLst:
                break
        except:
            print("Enter correct input for hall type")
    
    for key, values in movieShowTime.items():
        print(f"Show Time Code: {key}. Show Time: {values}" )
    
    filename = 'C:/MOOC/Theatre Management System/' + str(dt.date().day) + str(dt.date().strftime("%b")) + '.txt'
    
    with open(filename, 'r') as file:
        file_content = file.read()
        parts = file_content.split('\n\n')
        movieSelect = ast.literal_eval(parts[0].split('=', 1)[1].strip())
        hallReservations = ast.literal_eval(parts[1].split('=', 1)[1].strip())
        
        movieSelect['4'] = {hallInput: 'mm'}
        hallReservations['4'] = {hallInput : []}
              
        with open(filename, 'w') as file:
            file.write("movieSelect = ")
            file.write(str(movieSelect))
            file.write("\n\nhallReservations = ")
            file.write(str(hallReservations))
        
        file.close()
    
    print (f"Adding extra screening time over stanadrd times for {hallInput}")
    
#***********************************************************
# Admin browse reservations

def browseReservation():
    print("Please, Select the date of reservation in format YYYY/MM/DD: ")
    # open file with the given date

    selectedDate = dateSelect()
    filename = 'C:/MOOC/Theatre Management System/' + str(selectedDate.day) + str(selectedDate.strftime("%b")) + '.txt'
    
    mDict, hallReservations = movieList(filename)
    
    print("*******************************************")
    print("Screening time and movie list")  
    for showTime, hallTypes in mDict.items():
        for hallType, movieName in hallTypes.items():
            print(f"Screen Time: {showTime}. Hall Type: {hallType}. Movie Name: {movieName}")
    
    print("*******************************************")
    print("Reservation Status")    
    for showTime, hallTypes in hallReservations.items():
        for hallType, totalReservation in hallTypes.items():
            print(f"Screen Time: {showTime}. Hall Type: {hallType}. Total Reservations: {len(totalReservation)}")
    print("*******************************************")

#*************************************************************************
# Customer reserve a seat in the movie theatre

def reserveSeat(uname):
    # Customer choose date which is maximum 3 days ahead from todays date
    print("Screening time codes are as below")
    print("1: 09:00 - 12:00, 2: 13:00 - 16:00, 3: 17:00 - 20:00, 4: 20:30 - 23:00")
    print("Hall types are S: Small, M: Medium , L: Large")
    
    selectedDate = dateSelect()
       
    filename = 'C:/MOOC/Theatre Management System/' + str(selectedDate.day) + str(selectedDate.strftime("%b")) + '.txt'
   
    movieSelect, hallReservations = movieList(filename)
    movieNames = set()

    for inner_dict in movieSelect.values():
        for value in inner_dict.values():
            movieNames.add(value)
            
 
    movieNamesList = list(movieNames)
    while True:
        print(f"Movie List: {movieNames}")
        selectedMovie = input("Please, Select the movie.Enter the name: ")
        if selectedMovie in movieNamesList:
            break
        else:
            print("print select the correct movie name")
    
    # present the available halltypes and time slotts
    cnt=0
    
    seatAvailabilityDict = {}
    for screeningTime, hallTypes in movieSelect.items():
        for hallType, value in hallTypes.items():
            if value == selectedMovie:
                cnt = cnt + 1
                print(f"Option {cnt} => Screening Time: {screeningTime}, Hall Type: {hallType}")
                seatAvailability = []
                seatAvailability.append(screeningTime)
                seatAvailability.append(hallType)
                seatAvailabilityDict[cnt] = seatAvailability
          
         
    selectedOption = int(input("Please, select option: "))
    
    lst = seatAvailabilityDict[selectedOption]
    
    selectedScreeningTime = lst[0]
    selectedHallType = lst[1]

    # Customer select the halltype and time slotts
   
        
    for outer_key, inner_dict in hallReservations.items():
        for inner_key, value in inner_dict.items():
            if outer_key==selectedScreeningTime and inner_key == selectedHallType:
                if inner_key == 'S' and len(value)<10:
                    value.append(uname)
                    print(f"Screening Time: {outer_key}, Hall Type: {inner_key}")
                    print("Seat is reserved")
                    break
                elif inner_key == 'M' and len(value)<15:
                    value.append(uname)
                    print(f"Screening Time: {outer_key}, Hall Type: {inner_key}")
                    print("Seat is reserved")
                    break
                elif inner_key == 'L' and len(value)<20:
                    value.append(uname)
                    print(f"Screening Time: {outer_key}, Hall Type: {inner_key}")
                    print("Seat is reserved")
                    break
                else:
                    print("This hallType is full for selected screening time and movie!")
    
    with open(filename, 'w') as file:
        file.write("movieSelect = ")
        file.write(str(movieSelect))
        file.write("\n\nhallReservations = ")
        file.write(str(hallReservations))
 
#********************************************************************************
# Create a file having reservation details
   
def createReservationFile():
    movieSelect = {
    '1': {'S': 'm1', 'M': 'm2', 'L': 'm3'},
    '2': {'S': 'm2', 'M': 'm1', 'L': 'm4'},
    '3': {'S': 'm1', 'M': 'm4', 'L': 'm3'}
    }

    hallReservations = {
    '1': {'S': [], 'M': [], 'L': []},
    '2': {'S': [], 'M': [], 'L': []},
    '3': {'S': [], 'M': [], 'L': []}
    }


    
    while True:  
        dateInput = input('Enter a date formatted as YYYY/MM/DD: ')

        try:
            dt = datetime.datetime.strptime(dateInput, "%Y/%m/%d")
        
            minDate = datetime.datetime.today() + datetime.timedelta(days=3)
            
            if dt.date() > minDate.date():
                break
            else:
                print("Enter a date greater than 3 days from today")
        
        except:
            print("Error, try again")
    
    selectedDate = dt.date()
            
    filename = 'C:/MOOC/Theatre Management System/' + str(selectedDate.day) + str(selectedDate.strftime("%b")) + '.txt'
    fileContent = f"movieSelect = {movieSelect}\n\nhallReservations = {hallReservations}"
    with open(filename, 'w') as file:
        file.write(fileContent)
    print(f"A new reservation file is created for date {dt.date()}")
    
#***********************************************************************

def main():
   
    LoginStatus, uname = login()
    if LoginStatus == True and uname!="Admin":
        print("***Welcome to Royal Multiplex Reservation System!***")
        print("Select the date of the show. It should be within next 3 days")
        reserveSeat(uname)
        
        
    elif LoginStatus == True and uname == 'Admin':
        print("Hi Admin")
        ans = int(input("Enter 1 for Browse Reservations or Enter 2 for Adding a new movie or 3 for adding new screeing time or 4 for adding a new reservation file: "))
        if ans==1:
            print("Browse reservation")
            browseReservation()
        elif ans==2:
            print("Add movie")
            reply_movie_addition = addMovie()
            if reply_movie_addition == True:
                print("Movie added successfully!")
            else:
                print("There was an error while adding a new movie")
        elif ans==3:
            print("Add a new screeing time")
            print(addScreeningTime())
            
        elif ans==4:
            print("Create a new reservation file")
            createReservationFile()
            
  
if __name__ == "__main__":
    main()   

