############################################
#          Author: Dale Campbell           #
#          DSSA 5102-001                   # 
#          Halloween Assignment            # 
############################################

# Let's import libaries we'll need
import pandas as pd
import numpy as np
from datetime import datetime
#import matplotlib as plt

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
    newdf["DOBYear"] = df.iloc[:,2]
    newdf["DODYear"] = df.iloc[:,3]
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

def addLifespan(df):
    """This function takes in a dataframe, adds a column calcuating the death-birth to generate a lifespan. Then returns the new dataframe

    Args:
        df (Pandas DataFrame): A dataframe with birth year & death year

    Returns:
        df (Pandas DataFrame): The same dataframe with one extra column for "lifespan"
    """
    lifespan = []
    counter = 0
    
    for dateOfBirth in df["DOBYear"]:
        # Grab the DOB and DOD as variables
        birth = df["DOBYear"][counter]
        death = df["DODYear"][counter]
        # Find the difference in death - birth
        diff = int(death) - int(birth)
        lifespan.append(diff)
        counter += 1
    
    # Finally we can add the lifespan as a new column and return the dataframe
    df["Lifespan"] = pd.DataFrame(lifespan)
    return df

def cleanDataA(dfa):
    """ Takes in a dataframe, removes empty data, adds an empty column for "Sex", then changes the DOB and DOD into just a year format

    Args:
        dfa (Pandas DataFrame): Dataframe with --> FirstName,MiddleName,LastName,DOB,DOD

    Returns:
        dfa (Pandas DataFrame): Dataframe with --> FirstName,LastName,DOB,DOD,Sex
    """
    # Removing MiddleName from dataframe A then 
    dfa.pop("MiddleName")
    
    # Dropping NA values
    dfa.dropna(inplace = True) 
    dfa.reset_index(drop=True, inplace=True)
    
    # Adding Empty column for "Sex" 
    dfa["Sex"] = ""
    
    # Now let's clean the messed up datetime values in DOB
    newDOB = []
    for dateOfBirth in dfa['DOB']:
        # There are a few weird dates we need to clean:
        #   02/14/000  --> 02/14/1900
        #   Feb 41993  --> 04/04/1993
        #   04-03-1921 --> 04/03/1921
        if dateOfBirth == "02/14/000":
            newDOB.append(datetime.strptime("02/14/1900", '%m/%d/%Y'))
        elif dateOfBirth == " Feb 41993":
            newDOB.append(datetime.strptime("04/04/1993", '%m/%d/%Y'))
        elif dateOfBirth == "04-03-1921":
            newDOB.append(datetime.strptime("04/03/1921", '%m/%d/%Y'))
        else:
            newDOB.append(dateOfBirth)
    
    # Now let's clean the messed up datetime values in DOD
    newDOD = []
    for dateOfDeath in dfa['DOD']:
        # 11/00/0000 --> 11/01/2000"
        if dateOfDeath == "11/00/0000":
            newDOD.append(datetime.strptime("11/01/2000", '%m/%d/%Y'))
        else:
            newDOD.append(dateOfDeath)
    
    # Combining newDOB and newDOD into DataFrames        
    dfa['DOB'] = pd.DataFrame(newDOB)
    dfa['DOD'] = pd.DataFrame(newDOD)
    
    # Adding the datetime formate to these columns
    dfa['DOB'] = pd.to_datetime(dfa['DOB'])
    dfa['DOD'] = pd.to_datetime(dfa['DOD'])
    
    # Now loop through to get just the years from DOB and DOD
    counter = 0
    birth = []
    death = []
    for dateOfBirth in dfa['DOB']:
        birth.append(dfa["DOB"][counter].year)
        death.append(dfa["DOD"][counter].year)
        counter += 1
    dfa['DOB'] = pd.DataFrame(birth)
    dfa['DOD'] = pd.DataFrame(death)
    return dfa

def cleanDataB(dfb):
    """ Takes in a dataframe, removes empty data, then changes the DOB and DOD into just a year format

    Args:
        dfb (Pandas DataFrame): Dataframe with --> FirstName, LastName, DOB, DOD, Sex

    Returns:
        dfb (Pandas DataFrame): Dataframe with --> firstName,lastName,DOB,DOD,Sex
    """
    # Dropping NA values
    dfb.dropna(inplace = True) 
    dfb.reset_index(drop=True, inplace=True)
    
    # Now let's clean the messed up datetime values in DOB
    newDOB = []
    for dateOfBirth in dfb[' DOB']:
        # If there are only 4 numbers, then only year is provided. Add a temp 01/01 placeholder
        if len(str(dateOfBirth)) == 4:
            dateOfBirth = "01/01/" + dateOfBirth
            newDOB.append(datetime.strptime(str(dateOfBirth), '%m/%d/%Y'))
        else:
            newDOB.append(dateOfBirth)
            
    # Now let's clean the messed up datetime values in DOD
    newDOD = []
    for dateOfDeath in dfb[' DOD']:
         # If there are only 4 numbers, then only year is provided. Add a temp 01/01 placeholder
        if len(str(dateOfDeath)) == 4:
            dateOfDeath = "01/01/" + dateOfDeath
            newDOD.append(datetime.strptime(str(dateOfDeath), '%m/%d/%Y'))
        else:
            newDOD.append(dateOfDeath)
            
    # Combining newDOB and newDOD into DataFrames 
    dfb[' DOB'] = pd.DataFrame(newDOB)
    dfb[' DOD'] = pd.DataFrame(newDOD)
    
    # Adding the datetime formate to these columns
    dfb['DOB'] = pd.to_datetime(dfb[' DOB'])
    dfb['DOD'] = pd.to_datetime(dfb[' DOD'])
    
    # Now loop through to get just the years from DOB and DOD
    counter = 0
    birth = []
    death = []
    for dateOfBirth in dfb['DOB']:
        birth.append(dfb["DOB"][counter].year)
        death.append(dfb["DOD"][counter].year)
        counter += 1
    dfb['DOB'] = pd.DataFrame(birth)
    dfb['DOD'] = pd.DataFrame(death)
    
    # Remove the two columns that are ' DOB' and ' DOD'
    dfb.pop(" DOB")
    dfb.pop(" DOD")
    
    # To keep a consistent format we'll return a new dataframe
    newdf = pd.DataFrame()
    newdf["firstName"] = dfb["FirstName"]
    newdf["lastName"] = dfb[" LastName"]
    newdf["DOB"] = dfb["DOB"]
    newdf["DOD"] = dfb["DOD"]
    newdf["Sex"] = dfb[" Sex"]
    
    # Finally return the dataframe
    return newdf
    
def cleanDataC(dfc):
    """ Takes in a dataframe, removes empty data, turns 'Names' into firstName & lastName, then changes the DOB and DOD into just a year format

    Args:
        dfc (Pandas DataFrame): Dataframe with --> Name,DOB,DOD,Sex

    Returns:
        dfc (Pandas DataFrame): Dataframe with --> firstName,lastName,DOB,DOD,Sex
    """
    # Dropping NA values
    dfc.dropna(inplace = True) 
    dfc.reset_index(drop=True, inplace=True)
    
    # Dataframe C needs the names split up
    dfc = splitNamesColumn(dfc)
    
    # Now let's clean the messed up datetime values in DOB
    newDOB = []
    for dateOfBirth in dfc['DOB']:
        # If there are only 4 numbers, then only year is provided. Add a temp 01/01 placeholder
        if len(str(dateOfBirth)) == 4:
            dateOfBirth = "01/01/" + dateOfBirth
            newDOB.append(dateOfBirth)
            #newDOB.append(datetime.strptime(str(dateOfBirth), '%m/%d/%Y'))
        else:
            newDOB.append(dateOfBirth)
            
    # Now let's clean the messed up datetime values in DOD
    newDOD = []
    for dateOfDeath in dfc['DOD']:
         # If there are only 4 numbers, then only year is provided. Add a temp 01/01 placeholder
        if len(str(dateOfDeath)) == 4:
            dateOfDeath = "01/01/" + dateOfDeath
            newDOD.append(dateOfDeath)
            #newDOD.append(datetime.strptime(str(dateOfDeath), '%m/%d/%Y'))
        else:
            newDOD.append(dateOfDeath)
            
    # Combining newDOB and newDOD into DataFrames 
    dfc['DOB'] = pd.DataFrame(newDOB)
    dfc['DOD'] = pd.DataFrame(newDOD)
    
    # Adding the datetime formate to these columns
    dfc['DOB'] = pd.to_datetime(dfc['DOB'])
    dfc['DOD'] = pd.to_datetime(dfc['DOD'])
    
    # Now loop through to get just the years from DOB and DOD
    counter = 0
    birth = []
    death = []
    for dateOfBirth in dfc['DOB']:
        birth.append(dfc["DOB"][counter].year)
        death.append(dfc["DOD"][counter].year)
        counter += 1
    dfc['DOB'] = pd.DataFrame(birth)
    dfc['DOD'] = pd.DataFrame(death)
    
    return dfc

def find_Z_Score(df):
    """ Credit to the website below for showing how to use the .quantile() function to calculate some outliers
    https://careerfoundry.com/en/blog/data-analytics/how-to-find-outliers/#:~:text=Finding%20outliers%20using%20statistical%20methods,-Since%20the%20data&text=Using%20the%20IQR%2C%20the%20outlier,Q1%20(Q3%E2%80%93Q1).

    Args:
        df (Dataframe): 

    Returns:
       [outliers, not_outliers, outliers_dropped]: Returns which values are outliers, not outliers, and which ones were dropped
    """
    q1 = df['Lifespan'].quantile(0.25)
    q3 = df['Lifespan'].quantile(0.75)
    IQR = q3-q1
    
    outliers = df['Lifespan'][((df['Lifespan']<(q1-1.5*IQR)) | (df['Lifespan']>(q3+1.5*IQR)))]
    not_outliers = df['Lifespan'][~((df['Lifespan']<(q1-1.5*IQR)) | (df['Lifespan']>(q3+1.5*IQR)))]
    outliers_dropped = outliers.dropna().reset_index()
    
    return [outliers, not_outliers, outliers_dropped]

def main():
    # First we'll clean our data so we can begin to visualize the average lifespan over time. 
    
    # Cleaning dataset A
    dfa = pd.read_csv('data\halloween2019a.csv')
    dfa = cleanDataA(dfa)
   
    # Cleaning dataset B
    dfb = pd.read_csv('data\halloween2019b.csv')
    dfb = cleanDataB(dfb)
    
    # Cleaning dataset C
    dfc = pd.read_csv('data\halloween2019c.csv')
    dfc = cleanDataC(dfc)
    
    # Let's pass each dataframe to ensure column names are in our desired format
    dfa = correctColNames(dfa)
    dfb = correctColNames(dfb)
    dfc = correctColNames(dfc)
    
    # Now that each of our dataframes are in the desired format -- let's merge them into one dataframe
    df = pd.concat([dfa, dfb, dfc], ignore_index=True)
    
    # For consistency, let's make the gender consistently either 'M' or 'F'
    df = formatGender(df)
    
    # Now let's create a new column that calculates the individuals lifespan
    df = addLifespan(df)
    #print(df.to_string())
    
    # Calling a function to find outliers. 
    outliersArr = find_Z_Score(df)
    outliers = outliersArr[0]
    not_outliers = outliersArr[1]
    outliers_to_drop = outliersArr[2]

    print("Number of Outliers: "+ str(len(outliers)))
    print("Max Outlier Value: "+ str(outliers.max()))
    print("Min Outlier Value: "+ str(outliers.min()))
    #print(outliers_to_drop)
    
    # Now to remove the specific indexes from df that were provided in outliers_to_drop
    count = 0
    for num in outliers_to_drop["index"]:
        df = df.drop(df.index[num-count])
        count += 1
    df.reset_index(inplace=True)
    #print(df.to_string())

    # Grouping by year of birth
    tempVar1 = df.groupby(by=['DOBYear'], sort=True).sum()
    print(tempVar1)
    
    #tempVar2 = df.groupby(by=['DOBYear'], sort=True).aggregate(['min', 'max'])
    #print(tempVar2)
    
    # Now let's calcuate the averages
    totalPerGroup = set()
    for dob in tempVar1['DOBYear']:
        totalPerGroup.add({dob, 0})
    
    
    
    
if __name__ == '__main__':
    main()