#!/usr/bin/python3
#This script prints out the date of when a person with the birthday will reach that number after the number of days entered.
#Mrinalini-20230426:initial version

# Prompt the user for a birthdate and a number of days
birthdate = input("Enter birthdate (mm-dd-yyyy): ")
days = int(input("Enter number of days: "))

# Calculate the date that the person will reach the given number of days
birthdate_list = birthdate.split("-")
birthdate_month = int(birthdate_list[0])
birthdate_day = int(birthdate_list[1])
birthdate_year = int(birthdate_list[2])

target_year = birthdate_year + (days // 365)
target_month = birthdate_month
target_day = birthdate_day + (days % 365)

while True:
    days_in_month = 31
    if target_month in [4, 6, 9, 11]:
        days_in_month = 30
    elif target_month == 2:
        if (target_year % 4 == 0 and target_year % 100 != 0) or target_year % 400 == 0:
            days_in_month = 29
        else:
            days_in_month = 28

    if target_day <= days_in_month:
        break

    target_day -= days_in_month
    target_month += 1
    if target_month > 12:
        target_month = 1
        target_year += 1

# Print the result in the format mm-dd-yyyy
print("{:02d}-{:02d}-{}".format(target_month, target_day, target_year))

