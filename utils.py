import requests


NUMBER_URL_BASE = "http://numbersapi.com/"


def check_number(number: int):
    response = requests.get(f"{NUMBER_URL_BASE}{number}/math")
    if response.status_code == 200:
        return response.text


def is_prime(num: int):
    # Negative numbers, 0 and 1 are not primes
    if num > 1:

        # Iterate from 2 to n // 2
        for i in range(2, (num // 2) + 1):

            # If num is divisible by any number between
            # 2 and n / 2, it is not prime
            if (num % i) == 0:
                return False
        else:
            return True
    else:
        return False


def even(number: int):
    if number != 1 and number % 2 == 0:
        return True
    return False


def is_perfect_number(number: int):
    divisors = sum([i for i in range(1, number) if number % i == 0])
    if number == divisors:
        return True
    return False


# Python program to determine whether
# the number is Armstrong number or not

# Function to calculate x raised to
# the power y
def power(x, y):
    if y == 0:
        return 1
    if y % 2 == 0:
        return power(x, y // 2) * power(x, y // 2)

    return x * power(x, y // 2) * power(x, y // 2)


# Function to calculate order of the number
def order(x):
    # Variable to store of the number
    n = 0
    while x != 0:
        n = n + 1
        x = x // 10

    return n


# Function to check whether the given
# number is Armstrong number or not
def is_armstrong(x):
    n = order(x)
    temp = x
    sum1 = 0

    while temp != 0:
        r = temp % 10
        sum1 = sum1 + power(r, n)
        temp = temp // 10

    # If condition satisfies
    return sum1 == x


# Function to get sum of digits
def digit_sum(n: int):
    summation = 0
    for digit in str(n):
        summation += int(digit)
    return summation


def get_positive_integer(user_input):
    if user_input:
        try:
            # Convert input to an integer
            number = int(user_input)

            # Ensure it's positive
            return abs(number)

        except ValueError:
            return None
    else:
        return None



