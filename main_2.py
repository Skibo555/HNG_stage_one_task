from fastapi import FastAPI, Query
import requests
import math
from typing import List, Union, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Number Analysis API",
              description="API that provides mathematical properties and fun facts about numbers")

# Define allowed origins
origins = [
    "*",  # Allows all domains
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# Separate models for success and error responses
class SuccessResponse(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: List[str]
    digit_sum: int
    fun_fact: str
    error: bool = False


class ErrorResponse(BaseModel):
    number: str
    error: bool = True


def is_armstrong(num: int) -> bool:
    """Check if a number is an Armstrong number."""
    if not isinstance(num, int):
        return False

    num_str = str(abs(num))
    power = len(num_str)
    sum_of_powers = sum(int(digit) ** power for digit in num_str)
    return sum_of_powers == abs(num)


def is_prime(num: int) -> bool:
    """Check if a number is prime."""
    if abs(num) < 2:
        return False
    for i in range(2, int(math.sqrt(abs(num))) + 1):
        if abs(num) % i == 0:
            return False
    return True


def is_perfect(num: int) -> bool:
    """Check if a number is perfect (sum of proper divisors equals the number)."""
    num = abs(num)
    if num <= 1:
        return False

    divisors_sum = 1
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            divisors_sum += i
            if i != num // i:  # Add the other divisor if it's different
                divisors_sum += num // i
    return divisors_sum == num


def get_digit_sum(num: int) -> int:
    """Calculate the sum of digits in a number."""
    return sum(int(digit) for digit in str(abs(num)))


def get_properties(num: int) -> List[str]:
    """Get list of properties (armstrong, odd/even) for a number."""
    properties = []

    # Check Armstrong
    if is_armstrong(num):
        properties.append("armstrong")

    # Check odd/even
    if num % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    return properties


@app.get("/api/classify-number", response_model=Union[SuccessResponse, ErrorResponse])
async def analyze_number(number: str = Query(..., description="The number to analyze")):
    """
    Analyze a number and return its mathematical properties.

    - Returns mathematical properties like prime, perfect, Armstrong
    - Includes sum of digits
    - Fetches a fun fact from the Numbers API
    - Handles both valid numbers (including negative) and invalid inputs
    """
    try:
        num = int(number)

        # Get fun fact from Numbers API
        try:
            fun_fact_response = requests.get(f'http://numbersapi.com/{num}/math')
            fun_fact = fun_fact_response.text if fun_fact_response.status_code == 200 else f"{num} is a boring number."
        except requests.RequestException:
            fun_fact = f"{num} is a boring number."

        return SuccessResponse(
            number=num,
            is_prime=is_prime(num),
            is_perfect=is_perfect(num),
            properties=get_properties(num),
            digit_sum=get_digit_sum(num),
            fun_fact=fun_fact
        )

    except ValueError:
        # Return only number and error flag for invalid inputs
        return ErrorResponse(number=number)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)