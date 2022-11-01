############################################
#          Author: Dale Campbell           #
#          DSSA 5102-001                   # 
#          Halloween Assignment            #
#          Week 8                          # 
############################################

# Let's import libaries we'll need
import pandas as pd
import numpy as np
#import matplotlib as plt


def printData(dfa, dfb, dfc):
    # Print an identifier to the file -- data -- new line (to seperate the data for easier reading)
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
    first = []
    last = []
    for name in dfc["Name"]:
        nameSplit = name.split()
        if len(nameSplit) == 1:
            first.append(name)
            last.append("")
        elif len(nameSplit) == 2:
            first.append(nameSplit[0])
            last.append(nameSplit[-1])
        elif len(nameSplit) == 3:
            if (nameSplit[2] == "Jr.") or (nameSplit[2] == "Sr.") or (nameSplit[2] == "III"):
                first.append(nameSplit[0])
                last.append(nameSplit[1])
            else:
                first.append(nameSplit[0])
                last.append(nameSplit[-1])
        elif len(nameSplit) == 4:
            first.append(nameSplit[0])
            last.append(nameSplit[2])
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
    newdf = pd.DataFrame()
    newdf["firstName"] = df.iloc[:,0]
    newdf["lastName"] = df.iloc[:,1]
    newdf["DOB"] = df.iloc[:,2]
    newdf["DOD"] = df.iloc[:,3]
    newdf["Sex"] = df.iloc[:,4]
    return newdf

def formatGender(df):
    gender = []
    for sex in df["Sex"]:
        if sex == "Male" or sex == "male" or sex == "m" or sex == "M" or sex == "Male " or sex == "m " or sex == "M " or sex == " Male" or sex == " m" or sex == " M":
            gender.append('M')
        elif sex == "Female" or sex == "female" or sex == "f" or sex == "F" or sex == "Female " or sex == "f " or sex == "F " or sex == " Female" or sex == " f" or sex == " F":
            gender.append('F')
        else:
            gender.append('')
            
    df["Sex"] = pd.DataFrame(gender)
    return df

def updateDates(df):
    newDOB = []
    newDOD = []
    
    for dateOfBirth in df["DOB"]:
        newDOB.append("")
        newDOD.append("")
    
    #df["DOB"] = pd.DataFrame(newDOB)
    #df["DOD"] = pd.DataFrame(newDOD)
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
    
    # Based off this, let's prepare a format that's consitent which disregards any middle names
    #                      firstName, lastName, DOB, DOD, Sex
    
    # Removing MiddleName from dataframe A
    dfa.pop("MiddleName")

    # Adding Empty column for "Sex" to dataframe A 
    dfa["Sex"] = ""
    #print(dfa.head().to_string()) 

    # Dataframe B is in the format we desire 
    # Dataframe C needs the names split up
    dfc = splitNamesColumn(dfc)
    
    # Let's pass each dataframe to ensure column names are in our desired format
    dfa = correctColNames(dfa)
    dfb = correctColNames(dfb)
    dfc = correctColNames(dfc)
    
    # Now that each of our dataframes is in the desired format -- let's merge them into one dataframe
    df = pd.concat([dfa, dfb, dfc], ignore_index=True)

    # OPTIONAL FOR FINAL CODE -- If you would ilke to see all of the data listed, uncomment the next line
    #print(df.to_string())
    
    # Some results have 'Male'/'Female' whereas some have 'm'/'M'/'f'/'F' 
    # For consistency, let's make these either 'M' or 'F'
    df = formatGender(df)
    
    # Our dates are very inconsistent, I've identified at least the following formats:
    #   NaN, 1930, jan 14 1947, 04-03-1921
    #   These seem to be a typo
    #       Feb 41993 (we'll assume this to be Feb 4 1993)
    #       02/14/000 (we'll assume this to 02/14/1900)
    # Let's make everything a standard format of mm/dd/yyyy
    #   If only a year is provided we will format it to 01/01/yyyy
    #   If only month and year are provided we will format it to mm/01/yyyy
    
    df = updateDates(df)
    
    print(df.to_string())

    
    


if __name__ == '__main__':
    main()