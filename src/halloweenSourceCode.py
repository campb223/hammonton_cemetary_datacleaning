############################################
#          Author: Dale Campbell           #
#          DSSA 5102-001                   # 
#          Halloween Assignment            # 
############################################

# Let's import libaries we'll need
from cmath import nan
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.parser import parse
#import matplotlib as plt

def printData(dfa, dfb, dfc):
    # Print an identifier to the file -- data -- new line (to seperate the data for easier reading)
    """To initally view the data from three provided dataframes the function accepts the dataframes, prints which
    file it is, the head of the data, then a new line, and repeats for the other two dataframes.

    Args:
        dfa (Pandas DataFrame): Data from halloween2019a.csv
        dfb (Pandas DataFrame): Data from halloween2019b.csv
        dfc (Pandas DataFrame): Data from halloween2019c.csv
    """
    
    print('2019a \n')
    print(dfa.head().to_string()) 
    print('\n')

    print('2019b \n')
    print(dfb.head().to_string()) 
    print('\n')

    print('2019c \n')
    print(dfc.head().to_string()) 
    print('\n')
    
def splitNamesColumn(dfc):
    """In the dataframe provived there is one column labeled "Name" -- this function grabs the first and last (if available) names,
    creates a new dataframe with two columns "firstName" and "lastName" and returns that dataframe.

    Args:
        dfc (Pandas DataFrame): Data from halloween2019c.csv

    Returns:
        newdf (Pandas DataFrame): Dataframe with two columns for firstName and lastName (as well as other columns)
    """
    
    first = []
    last = []
    
    # There are a few cases we'll run into with splitting up names into firstName / lastName
    for name in dfc["Name"]:
        # Initally we'll split the names
        nameSplit = name.split()
        
        # If there's only one name:
        #   1. The provided name will be the first name
        #   2. The last name will be null
        if len(nameSplit) == 1:
            first.append(name)
            last.append("")
        # If it's a perfect split with two names -- firstName=first split and lastName=last split
        elif len(nameSplit) == 2:
            first.append(nameSplit[0])
            last.append(nameSplit[-1]) 
        # If there's three provided names we need to analyze further
        elif len(nameSplit) == 3:
            # If the final name provided is Jr., Sr., or III -- disregard that part (Jr., Sr., or III)
            if (nameSplit[2] == "Jr.") or (nameSplit[2] == "Sr.") or (nameSplit[2] == "III"):
                first.append(nameSplit[0])
                last.append(nameSplit[1])
            # Otherwise we'll assume it's a middle name and firstName=first split then lastName=last split
            else:
                first.append(nameSplit[0])
                last.append(nameSplit[-1])
        # If there are 4 provided names, firstName=first split and lastName=third split
        elif len(nameSplit) == 4:
            first.append(nameSplit[0])
            last.append(nameSplit[2])
        # If none of the above cases split the names -- firstName=first split and lastName=last split
        else:
            first.append(nameSplit[0])
            last.append(nameSplit[-1])
    
    # Now let's create a new dataframe with the format of firstName, lastName, DOB, DOD, Sex
    newdf = pd.DataFrame()
    newdf["firstName"] = first
    newdf["lastName"] = last
    newdf["DOB"] = dfc["DOB"]
    newdf["DOD"] = dfc["DOD"]
    newdf["Sex"] = dfc["Sex"]
    
    # Finally return the dataframe
    return newdf

def correctColNames(df):
    """This function accepts a dataframe then renames the columns in case they are not already in this format then returns the dataframe:
        firstName
        lastName
        DOB
        DOD
        Sex

    Args:
        df (Pandas DataFrame): dataframe that could or could not have the correct column names

    Returns:
        newdf (Pandas DataFrame): dataframe with the proper column names 
    """
    
    # Here we'll init an empty dataframe and explicitly label the columns in our desired format
    newdf = pd.DataFrame()
    newdf["firstName"] = df.iloc[:,0]
    newdf["lastName"] = df.iloc[:,1]
    newdf["DOB"] = df.iloc[:,2]
    newdf["DOD"] = df.iloc[:,3]
    newdf["Sex"] = df.iloc[:,4]
    
    # Finally return the dataframe
    return newdf

def formatGender(df):
    """This function accepts a dataframe, then standardizes variations of m/M/Male or f/F/Female into:
        'M'
        'F'

    Args:
        df (Pandas DataFrame): dataframe which has a column labeled "Sex"

    Returns:
        df (Pandas DataFrame): dataframe with male = 'M' and female = 'F'
    """
    
    gender = []
    for sex in df["Sex"]:
        # Let's remove any leading spaces from the entry
        sex = str(sex).lstrip()
        # If the entry is anything related to 'male' it will become 'M'
        if sex == "Male" or sex == "male" or sex == "m" or sex == "M" or sex == "Male " or sex == "m " or sex == "M ":
            gender.append('M')
        # If the entry is anything related to 'female' it will become 'F'
        elif sex == "Female" or sex == "female" or sex == "f" or sex == "F" or sex == "Female " or sex == "f " or sex == "F ":
            gender.append('F')
        # Otherwise, it's a blank entry. 
        else:
            gender.append('')
            
    # Here we re-write to the column "Sex" with our consistently labaled gender format
    df["Sex"] = pd.DataFrame(gender)
    
    # Finally return the dataframe
    return df

def updateDates(df):
    """The function is intended to update the date for DOB and DOD on the provided dataframe. 
    
    I've identified at least the following formats to be present:
       NaN, 1930, jan 14 1947, 04-03-1921, Jan 1980
    
    These seem to be a typo
        Feb 41993 (we'll assume this to be Feb 4 1993)
        02/14/000 (we'll assume this to 02/14/1900)
    
    If only a year is provided we will format it to 01/01/yyyy
    If only month and year are provided we will format it to mm/01/yyyy

    Args:
        df (Pandas DataFrame): Accepts a dataframe with varying date formats for DOB and DOD

    Returns:
        df (Pandas DataFrame): Returns a dataframe with the DOB and DOD consistently updated to mm/dd/yyyy
    """
    
    newDOB = []
    newDOD = []
    
    # Loop through each DOB
    for dateOfBirth in df["DOB"]:
        # Make each DOB a string
        dateOfBirth = str(dateOfBirth)
        # If the DOB appears to be a typo, we'll correct it first then continue to loop. 
        if dateOfBirth == "02/14/000":
            newDOB.append(datetime.strptime("02/14/1900", '%m/%d/%Y'))
            continue
        elif dateOfBirth == " Feb 41993":
            newDOB.append(datetime.strptime("04/04/1993", '%m/%d/%Y'))
            continue
        elif dateOfBirth == "04-03-1921":
            newDOB.append(datetime.strptime("04/03/1921", '%m/%d/%Y'))
            continue
            
        # Here we'll remove any leading white spaces on the DOB
        dateOfBirth = str(dateOfBirth).lstrip()

        # If the DOB is null -- add an empty entry
        if pd.isna(str(dateOfBirth)) or dateOfBirth == "nan":
            newDOB.append("")
        # If the length of the string = 4, we'll assume only a year is provided and return 01/01/yyyy
        elif len(str(dateOfBirth)) == 4:
            dateOfBirth = "01/01/" + dateOfBirth
            newDOB.append(datetime.strptime(str(dateOfBirth), '%m/%d/%Y'))
        # Otherwise we'll need to do some additional formatting to get mm/dd/yyyy
        else:
            # Attempting to just convert to mm/dd/yyyy
            try:
                newDOB.append(datetime.strptime(str(dateOfBirth), '%m/%d/%Y'))
            except:
                try:
                    newDOB.append(datetime.strptime(str(dateOfBirth), '%b/%d/%Y'))
                except:
                    # If that failed, try to capitalize the first letter and see how many times it split
                    tempDateOfBirth = str(dateOfBirth).capitalize()
                    strSplit = tempDateOfBirth.split()
                    # If split = 2 then it's like Sept 1900
                    if len(strSplit) == 2:
                        if(strSplit[0] == "Sept"):
                            tempDateOfBirth = "Sep"
                            newTempStr = tempDateOfBirth + "/01/" + strSplit[1]
                        else:
                            newTempStr = strSplit[0] + "/01/" + strSplit[1]
                        try:
                            newDOB.append(datetime.strptime(newTempStr, '%b/%d/%Y'))
                        except:
                            newDOB.append(datetime.strptime(newTempStr, '%B/%d/%Y'))
                            continue
                    elif len(strSplit) == 3:
                        try:
                            if len(strSplit[1]) == 2:
                                newTempStr = strSplit[0] + "/" + strSplit[1][0] + strSplit[1][1]  + "/" + strSplit[2]
                            else:
                                newTempStr = strSplit[0] + "/0" + strSplit[1][0] + "/" + strSplit[2]
                            newDOB.append(datetime.strptime(str(newTempStr), '%b/%d/%Y'))
                        except:
                            newDOB.append(datetime.strptime(str(newTempStr), '%B/%d/%Y'))
                                            
    for dateOfDeath in df["DOD"]:
        
        # If the DOB appears to be a typo, we'll correct it first then continue to loop. 
        if dateOfDeath == "11/00/0000":
            newDOD.append("")
            continue
        
        dateOfDeath = str(dateOfDeath).lstrip()
        
        if pd.isna(dateOfDeath) or dateOfDeath == "nan":
            newDOD.append("")
        elif len(dateOfDeath) == 4:
            dateOfDeath = "01/01/" + dateOfDeath
            newDOD.append(datetime.strptime(str(dateOfDeath), '%m/%d/%Y'))
        else:
            # Attempting to just convert to mm/dd/yyyy
            try:
                newDOD.append(datetime.strptime(str(dateOfDeath), '%m/%d/%Y'))
            except:
                try:
                    newDOD.append(datetime.strptime(str(dateOfDeath), '%b/%d/%Y'))
                except:
                    # If that failed, try to capitalize the first letter and see how many times it split
                    tempDateOfDeath = str(dateOfDeath).capitalize()
                    strSplit = tempDateOfDeath.split()
                    # If split = 2 then it's like Sept 1900
                    if len(strSplit) == 2:
                        if(strSplit[0] == "Sept"):
                            tempDateOfDeath = "Sep"
                            newTempStr = tempDateOfDeath + "/01/" + strSplit[1]
                        else:
                            newTempStr = strSplit[0] + "/01/" + strSplit[1]
                        try:
                            newDOD.append(datetime.strptime(newTempStr, '%b/%d/%Y'))
                        except:
                            newDOD.append(datetime.strptime(newTempStr, '%B/%d/%Y'))
                            continue
                    elif len(strSplit) == 3:
                        try:
                            if len(strSplit[1]) == 2:
                                newTempStr = strSplit[0] + "/" + strSplit[1][0] + strSplit[1][1]  + "/" + strSplit[2]
                            else:
                                newTempStr = strSplit[0] + "/0" + strSplit[1][0] + "/" + strSplit[2]
                            newDOD.append(datetime.strptime(str(newTempStr), '%b/%d/%Y'))
                        except:
                            newDOD.append(datetime.strptime(str(newTempStr), '%B/%d/%Y'))
    
    # Now we can update our DOB and DOD with our formatted datetime objects. 
    df["DOB"] = pd.DataFrame(newDOB)
    df["DOD"] = pd.DataFrame(newDOD)
    
    # Finally return the dataframe
    return df
        

def addLifespan(df):
    """This function takes in a dataframe, adds a column calcuating the death-birth to generate a lifespan. Then returns the new dataframe

    Args:
        df (Pandas DataFrame): A dataframe with birth year & death year

    Returns:
        df (Pandas DataFrame): The same dataframe with one extra column for "lifespan"
    """
    
    lifespan = []
    birth = []
    death = []
    
    for dateOfBirth in df["DOB"]:
        birth.append(dateOfBirth)
    for dateOfDeath in df["DOD"]:
        death.append(dateOfDeath)
    #lifespan.append(dateOfDeath - dateOfBirth)
    #df["Lifespan"] = pd.DataFrame(lifespan)
    return df


def main():
    # Let's read in each of the CSV files to their own dataframes
    dfa = pd.read_csv('data\halloween2019a.csv')
    dfb = pd.read_csv('data\halloween2019b.csv')
    dfc = pd.read_csv('data\halloween2019c.csv')
    
    # OPTIONAL FOR FINAL CODE -- If you would like to see the head of each dataframe -- uncomment the next line
    #printData(dfa, dfb, dfc)
    
    # Our data is in the following formats:
    #             halloween2019a.csv            #           halloween2019b.csv           #   halloween2019c.csv 
    #   FirstName,MiddleName,LastName,DOB,DOD   #   FirstName, LastName, DOB, DOD, Sex   #    Name,DOB,DOD,Sex
    
    # Let's prepare a format that's consitent which disregards any middle names (firstName, lastName, DOB, DOD, Sex)
    
    # Removing MiddleName from dataframe A
    dfa.pop("MiddleName")

    # Adding Empty column for "Sex" to dataframe A 
    dfa["Sex"] = ""

    # Dataframe B is in the format we desire 
    # Dataframe C needs the names split up
    dfc = splitNamesColumn(dfc)
    
    # Let's pass each dataframe to ensure column names are in our desired format
    dfa = correctColNames(dfa)
    dfb = correctColNames(dfb)
    dfc = correctColNames(dfc)
    
    # Now that each of our dataframes are in the desired format -- let's merge them into one dataframe
    df = pd.concat([dfa, dfb, dfc], ignore_index=True)

    # OPTIONAL FOR FINAL CODE -- If you would ilke to see all of the data listed, uncomment the next line
    #print(df.to_string())
    
    # Some results have 'Male'/'Female' whereas some have 'm'/'M'/'f'/'F' 
    # For consistency, let's make these either 'M' or 'F'
    df = formatGender(df)
    
    # Our dates are very inconsistent, let's make everything a standard format of mm/dd/yyyy
    df = updateDates(df)
    
    # Now let's create a new column that calculates the individuals lifespan
    #df = addLifespan(df)
    
    print(df.to_string())

    
    


if __name__ == '__main__':
    main()