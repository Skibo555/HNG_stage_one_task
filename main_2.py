import uvicorn
from fastapi import FastAPI, Request, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(tags=["Number API"])

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

@app.get('/')
def get_home():
    return {"message": "Welcome to the Number API!"}

def check_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def get_positive_integer(user_input):
    try:
        # Convert input to an integer
        number = int(user_input)

        # Ensure it's positive
        return abs(number)

    except ValueError:
        return None

NUMBER_URL_BASE = "http://numbersapi.com/"

def check_number(number: int):
    try:
        response = requests.get(f"{NUMBER_URL_BASE}{number}/math")
        if response.status_code == 200:
            return response.text
        return "No fun fact available."
    except requests.RequestException:
        return "Failed to fetch fun fact."

def even(value):
    return value % 2 == 0

def is_perfect_number(value):
    return sum(i for i in range(1, value) if value % i == 0) == value

def is_prime(value):
    if value < 2:
        return False
    for i in range(2, int(value**0.5) + 1):
        if value % i == 0:
            return False
    return True

def digit_sum(value):
    return sum(int(digit) for digit in str(value))

def is_armstrong(value):
    digits = [int(d) for d in str(value)]
    num_digits = len(digits)
    return sum(d ** num_digits for d in digits) == value

@app.get("/api/classify-number", status_code=status.HTTP_200_OK)
async def get_number(request: Request, res: Response):
    parameter = request.query_params
    user_input = parameter.get("number")
    properties = []

    # Input validation
    if not user_input or not check_int(user_input):
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "number": user_input,
            "error": True,
            "message": "Invalid input. Please provide a valid integer."
        }

    # Ensure the input is a positive integer
    user_in = get_positive_integer(user_input)
    if user_in is None:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "number": user_input,
            "error": True,
            "message": "Invalid input. Could not parse a positive integer."
        }

    # Process the valid input
    try:
        result = check_number(user_in)
        is_even = even(user_in)
        is_perfect = is_perfect_number(user_in)
        is_prime_result = is_prime(user_in)
        digit_sum_result = digit_sum(user_in)
        is_armstrong_result = is_armstrong(user_in)

        if is_armstrong_result:
            properties.append("armstrong")
        if is_even:
            properties.append("even")
        else:
            properties.append("odd")

        success = {
            "number": user_in,
            "is_prime": is_prime_result,
            "is_perfect": is_perfect,
            "properties": properties,
            "digit_sum": digit_sum_result,
            "fun_fact": result
        }

        return success
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, host="0.0.0.0", port=8000)
