#!/usr/bin/python3
#This script prints out the date of when a person with the birthday will reach that number after the number of days entered.
#Mrinalini-20230428: second version

import datetime

# Get birthdate and number of days from user
birthdate = input("Enter birthdate (mm-dd-yyyy): ")
num_days = int(input("Enter number of days: "))

# Convert birthdate string to datetime object
birthdate_obj = datetime.datetime.strptime(birthdate, '%m-%d-%Y')

# Calculate date when person will reach num_days
future_date = birthdate_obj + datetime.timedelta(days=num_days)

# Convert future_date to formatted string
future_date_str = future_date.strftime('%m-%d-%Y')

# Print result
print("You will reach",num_days, "days old on ",future_date_str, ".")

