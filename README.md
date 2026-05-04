# API Principal

## What is it?
This api work as a midfielder between 180's partners and 180 backend apis, allowing partners to register into 180 as 
partners and create insurance policies for their customers.

## Running automated tests
On command line run: 
>` pytest`

## Running locally

First install dependencies, on command line run:
> `pip install -r requirements.txt`
### Set secrets:
Before run the app you should set the 180's insurance api  secret api key,
following the `model.env` file on a new file called `.env`.

Then, with a running container of the 180's insurance API, on command line run:
> `python app.py`

And then it is ready for requests.
