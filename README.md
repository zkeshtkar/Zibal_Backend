# Sample Zibal Backend

Many transactions occur daily. We intend to store and use them .
This api supports daily, weekly and monthly modes for classifying transactions and number and amount modes for the final output amount per customer.



## Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/zkeshtkar/Zibal_Backend.git
    $ cd Zibal_Backend
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt


## Get list of Transactions

### Request

`GET /transactionApi/trnsaction`

    curl --location --request GET 'http://127.0.0.1:8000/transactionApi/trnsaction' --header 'Content-Type: application/json' --data-raw '{"mode":"weekly","type":"amount","merchantId":"5b086ecdf92ea126d079275d"}'


### Sample Response Body


    [
        {
            "key": "هفته ی 22 سال 2020",
            "value": 118160544
        }
    ]


## Get list of Transactions from cache

### Request

`GET /transactionApi/cachedTrnsaction`

    curl --location --request GET 'http://127.0.0.1:8000/transactionApi/cachedTrnsaction' --header 'Content-Type: application/json' --data-raw '{
    "mode":"weekly",
    "type":"amount",
    "merchantId":"5b086ecdf92ea126d079275d"
    }'

### Sample Response Body
    [
        {
            "key": "هفته ی 22 سال 2020",
            "value": 118160544
        }
    ]
## Command
You can also use this command to get the right result from `/transactionApi/cachedTrnsaction` and increase the speed.
 
    python3 manage.py save_data  --mode weekly --type amount --merchantId 5b086ecdf92ea126d079275r  
        


