import uvicorn
from fastapi import FastAPI, Request, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware

from utils import(
    check_number,
    is_perfect_number,
    is_armstrong,
    is_prime,
    even,
    digit_sum,
    get_positive_integer
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
    print(user_input)
    armstrong = []
    if not user_input:
        response = {
            "number": user_input,
            "error": True
        }
        res.status_code = status.HTTP_400_BAD_REQUEST

        return response

    if get_positive_integer(int(user_input)):
        try:
            user_in = abs(int(user_input))
            result = check_number(int(user_in))
            ev_od = even(int(user_input))
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
    response = {
        "number": user_input,
        "error": True
    }
    res.status_code = status.HTTP_400_BAD_REQUEST

    return response


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, host="0.0.0.0")
