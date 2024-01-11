#!/usr/bin/env python
"""
    18/11/2023
    Programming Fundamentals - Assessment 1

    General Styling: https://peps.python.org/pep-0008/
    Docstring format: https://peps.python.org/pep-0257/
"""

__author__ = "Emmet Noman"
__email__ = "27587991@students.lincoln.ac.uk"

from typing import List, Tuple # Type annotations for easier readability.
# The criteria said builtin imports that aren't used to perform calculations are permitted.
# These can be removed without affecting any of the logic

class UnexpctedInputException(Exception):
    """Raised when input sanitization fails"""
    def __init__(self, invalid_input):
        super().__init__(f"\"{invalid_input}\" is not a valid input!")

def is_int(number):
    """Checks if the provided input is an integer"""
    if number[0] in ('-', '+'): # check if it has unary operators
        return number[1:].isdigit() # if so, only check if the text after it is numerical.
    return number.isdigit()

def is_prime(number):
    """Does a primality test on the provided input."""
    if number <= 1: 
        return False # only natural numbers can be prime.
    if number % 2 == 0:
        return number == 2 # 2 is a prime, any other number divisible by 2 is not.
    for i in range(3, 1 + int(number**(1/2)), 2): # Loop over every possible divident for the given number in steps of 2
        if number % i == 0: # if the number divides cleanly for a single number, it is not a prime!
            return False
    return True # if the program didn't return during the for loop, it must be a prime.

def calculate_statistics(numbers: List[int]) -> Tuple[int, float, int, int]:
    """Determines and returns the sum, mean and minimum and maximum of a provided list.
    
    Arguments:
    numbers -- List of integers

    returns:
    A tuple containing the sum, mean, minimum & maximum respectively
    """
    sum_of_numbers, min_of_numbers, max_of_numbers = 0, None, None # declare variables to store changing values
    for number in numbers:
        if min_of_numbers == None or number < min_of_numbers:
            min_of_numbers = number # update minimum variable
        if max_of_numbers == None or number > max_of_numbers:
            max_of_numbers = number # update maximum variable

        sum_of_numbers += number # add the current iteration's value to the sum variable
    
    mean_of_numbers = sum_of_numbers / len(numbers) # calculate the mean from the sum we computed earlier

    return sum_of_numbers, mean_of_numbers, min_of_numbers, max_of_numbers # return a tuple of 3 ints and 1 float


def find_prime_numbers(list_of_numbers):
    """A function to find the prime numbers in a list

    Arguments:
    list_of_numbers -- A list of validated integers provided by the user

    Returns:
    A list containing the prime numbers which were in the input.
    """
    return sorted(list(filter(lambda number: is_prime(number), list_of_numbers)))

def validate_user_number_input(user_input) -> List[int] | str:
    """Validates and parses the text input given by the user.

    Arguments:
    user_input -- An input from the user.
    
    Returns:
    A list of integers or a string describing an unexpected input

    Raises:
    UnexpctedInputException -- If the given list of inputs are invalid.
    """

    number_list = user_input.replace(',', '').split(" ") # seperate user input into an array and remove any commas
    for number_candidate in number_list:    
        if not is_int(number_candidate): # Check if the number is an integer, e.g. 1, 2, 3 and does not contain anything but digits / minus.
            raise UnexpctedInputException(number_candidate) # oops, the user has input an invalid number, we should raise an error!
    else:
        return [int(number) for number in number_list] # if we passed all checks, cast every element of the array into an integer and return the newly generated array

def main():
    number_list = []
    print("Enter whole numbers seperated by spaces below, e.g. (42 +1 -10 292 0)") # print the instructions for the input
    while True: # keep going until broken out of after getting a valid input
        try:
            number_list = validate_user_number_input(input(": ")) # validate user input and store it in the function's scope
            break # if the validation succeeds, break out of the loop
        except UnexpctedInputException as e: # catch only the custom error defintion
            print(e) # tell the user the error

    print(f"You inputted {len(number_list)} whole number(s)") # count the number of inputs
    # we know for a fact that they are all integers, since we did the input sanitization.

    number_stats = calculate_statistics(number_list) # get the statistics of the number list
    prime_numbers = sorted(set(find_prime_numbers(number_list)))

    primes = ", ".join([str(number) for number in prime_numbers]) # filter the list

    print(f"""Statistics of the given whole number(s):
          
          Sum: {number_stats[0]}
          Mean: {number_stats[1]:.2f}
          Min: {number_stats[2]}
          Max: {number_stats[3]}
          Primes: [{primes}]
          """) # multi-line text to display the result in a clean manner.


if __name__ == "__main__": # make sure file is not being ran as a module
    main()