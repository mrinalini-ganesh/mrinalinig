#!/usr/bin/python3
# This script reads in any number of positive numbers, on the command line and finds their average to two decimal places
# Mrinalini-20230417: initial version

import sys

#!/usr/bin/python3
import sys

def calculate_average(numbers):
# This calculates the numbers inputed and prints the average of a list of numbers.
    total = sum(numbers)
    average = total / len(numbers)
    print("The average of the given numbers is: {:.2f}".format(average))

def main():
#The main function calls the calculate_average function.
    if len(sys.argv) < 2:
        print("To find the average of your values enter: avgn.py <num1> <num2> ... <numN>")
        return
   
    numbers = []
    for arg in sys.argv[1:]:
        try:
            num = float(arg)
            if num < 0:
                print("Error: all arguments must be positive")
                return
            numbers.append(num)
        except ValueError:
            print("Error: all arguments must be valid numbers")
            return
    
    calculate_average(numbers)

if __name__ == '__main__':
    main()

