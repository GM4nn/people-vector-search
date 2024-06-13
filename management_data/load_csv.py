import pandas as pd

people_data = pd.read_csv('data\people.csv')
people_data['combined_text'] = (
    people_data['First Name'] + ' ' 
    + people_data['Last Name'] + ' ' 
    + people_data['Sex'] + ' '
    + people_data['Email'] + ' '
    + people_data['Phone'] + ' '
    + people_data['Date of birth'] + ' '
    + people_data['Job Title'] + ' '
)
