#!/usr/bin/python3
# Description: This script prompts the user for their name and favorite color, and prints out a message with the inputed values.
# Versioning:
# Mrinalini-20230417: initial version

# Set up initial variables and imports
import sys

# Main routine that is called when script is run, Define a function to run the program.
def main():
    # Prompt the user for their name and favorite color
    name = input("Hello! What is your name? ")
    color = input("What is your favorite color? ")

    # Print out the result
    print("The favorite color for " + name + " is " + color + ".")

# Run main() if script called directly, else use as a library to be imported
if __name__ == "__main__":
    main()

