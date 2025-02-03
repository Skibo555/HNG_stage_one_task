import uvicorn
from fastapi import FastAPI, Request, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware

from utils import(
    check_number,
    check_input_type,
    is_perfect_number,
    is_armstrong,
    is_prime,
    even,
    digit_sum
)

app = FastAPI(tag=["Number API"])

# Define allowed origins
origins = [
    "*",  # Allows all domains
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/classify-number", status_code=status.HTTP_200_OK)
async def get_number(request: Request, res: Response):
    parameter = request.query_params
    user_input = parameter.get("number")
    armstrong = []
    try:
        if user_input.isnumeric():
            result = await check_number(int(user_input))
            ev_od = await even(int(user_input))
            is_perfect = await is_perfect_number(int(user_input))
            prime = await is_prime(int(user_input))
            dig_sum = await digit_sum(int(user_input))
            if is_armstrong(int(user_input)) and ev_od:
                armstrong.append("armstrong")
                armstrong.append("even")
            elif is_armstrong(int(user_input)) and not ev_od:
                armstrong.append("armstrong")
                armstrong.append("odd")
            else:
                if ev_od:
                    armstrong.append("even")
                if not ev_od:
                    armstrong.append("odd")

            success = {
                "number": user_input,
                "is_prime": prime,
                "is_perfect": is_perfect,
                "properties": armstrong,
                "digit_sum": dig_sum,
                "fun_fact": result
            }

            return success
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

    invalid_input = await check_input_type(user_input)

    response = {
        "number": invalid_input,
        "error": True
    }
    res.status_code = status.HTTP_400_BAD_REQUEST

    return response


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
