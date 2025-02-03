Welcome my Stage 1 task for HNG
This project when given a valid integer, it returns if the number is prime number, perfect number, returns a fun fact about the number and also checks if the number is an even or odd number and also if the number is armstrong or not, below is an example of a successful response:
with a status code 200 Ok.
```commandline
{
  "number": "153",
  "is_prime": false,
  "is_perfect": false,
  "properties": [
    "armstrong",
    "odd"
  ],
  "digit_sum": 9,
  "fun_fact": "153 is a narcissistic number."
}
```
an invalid input such as an alphanumeric or an alphabet.

```commandline
{
  "number": "alphabet",
  "error": true
}
```

Get Started

clone the repo using this url: 

Initiate Virtual Environment with command:

python3 -m venv venv
Start Envirnoment with command:

from the root directory
`cd stage_1_task`

Activate the virtual environment
`source venv/bin/activate`
Deactivate Environment with command:

Install packages in requirements.txt with command:

`pip3 install -r requirements.txt`

run the app with:
`python3 main.py`

You can visit the live project here:
https://hng-stage-one-task-m9j7.onrender.com/



HNG backlink:

https://hng.tech/hire/python-developers
