import uvicorn
from fastapi import FastAPI, Request, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
import requests


app = FastAPI(tag=["Number API"])

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
    return {"message": "Welcome"}


def check_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

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

NUMBER_URL_BASE = "http://numbersapi.com/"


def check_number(number: int):
    response = requests.get(f"{NUMBER_URL_BASE}{number}/math")
    if response.status_code == 200:
        return response.text
def even(value):
    return value % 2 == 0

def is_perfect_number(value):
    # Placeholder logic for perfect number check
    return sum(i for i in range(1, value) if value % i == 0) == value

def is_prime(value):
    # Placeholder logic for prime number check
    if value < 2:
        return False
    for i in range(2, int(value**0.5) + 1):
        if value % i == 0:
            return False
    return True

def digit_sum(value):
    return sum(int(digit) for digit in str(value))

def is_armstrong(value):
    # Placeholder logic for Armstrong number check
    digits = [int(d) for d in str(value)]
    num_digits = len(digits)
    return sum(d ** num_digits for d in digits) == value

@app.get("/api/classify-number", status_code=status.HTTP_200_OK)
async def get_number(request: Request, res: Response):
    parameter = request.query_params
    user_input = parameter.get("number")
    armstrong = []

    # Input validation
    if not user_input or not check_int(user_input):
        response = {
            "number": user_input,
            "error": True
        }
        res.status_code = status.HTTP_400_BAD_REQUEST
        return response

    # Ensure the input is a positive integer
    if not get_positive_integer(user_input):
        response = {
            "number": user_input,
            "error": True
        }
        res.status_code = status.HTTP_400_BAD_REQUEST
        return response

    # Process the valid input
    try:
        user_in = abs(int(user_input))
        result = check_number(int(user_in))
        ev_od = even(int(user_in))
        is_perfect = is_perfect_number(int(user_in))
        prime = is_prime(int(user_in))
        dig_sum = digit_sum(int(user_in))

        if is_armstrong(int(user_in)) and ev_od:
            armstrong.append("armstrong")
            armstrong.append("even")
        elif is_armstrong(int(user_in)) and not ev_od:
            armstrong.append("armstrong")
            armstrong.append("odd")
        else:
            if ev_od:
                armstrong.append("even")
            if not ev_od:
                armstrong.append("odd")

        success = {
            "number": int(user_input),
            "is_prime": prime,
            "is_perfect": is_perfect,
            "properties": armstrong,
            "digit_sum": dig_sum,
            "fun_fact": result
        }

        return success
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, host="0.0.0.0")