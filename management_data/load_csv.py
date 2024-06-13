import pandas as pd

people_data = pd.read_csv('data\people.csv')
people_data['people_jobs'] = (
    people_data['First Name'] + ' ' 
    + people_data['Last Name'] + ' '
    + people_data['Job Title'] + ' '
)

people_data['people_births_date'] = (
    people_data['First Name'] + ' ' 
    + people_data['Last Name'] + ' '
    + people_data['Date of birth'] + ' '
)

people_data['people_genders'] = (
    people_data['First Name'] + ' ' 
    + people_data['Last Name'] + ' '
    + people_data['Date of birth'] + ' '
)

people_data['people_phone'] = (
    people_data['First Name'] + ' ' 
    + people_data['Last Name'] + ' '
    + people_data['Phone'] + ' '
)

people_data['people_email'] = (
    people_data['First Name'] + ' ' 
    + people_data['Last Name'] + ' '
    + people_data['Email'] + ' '
)