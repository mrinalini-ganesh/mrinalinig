#!/usr/bin/python3
# This script reads in three arguments, all positive numbers, on the command line and finds their average to two decimal places
# Mrinalini-20230417: initial version

import sys

#Define a function to calculate the average of three numbers that are inputed
def avg3(num1, num2, num3):
     # Check if any of the numbers are negative
    if num1 < 0 or num2 < 0 or num3 < 0:
        print("Error: All input numbers must be positive")
        return
    
    #calculate the average and print it to two decimal places
    avg = (num1 + num2 + num3) /3
    print(f"The Average of {num1}, {num2}, and {num3} is {avg:.2f}")
  
    #Make sure that there are only three arguments
if len(sys.argv) != 4:
    print("To find the average as 3 values enter: python avg3.py num1 num2 num3")
else:
    # Convert all the arguments into floats, not using integers as we need decimal places. Print an error if it is not.
    try:
        num1 = float(sys.argv[1])
        num2 = float(sys.argv[2])
        num3 = float(sys.argv[3])
        # Call the avg3 function with the three numbers
        avg3(num1, num2, num3)
    except ValueError:
        print("Error: all arguments must be valid numbers")