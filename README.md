# Weather Info 


## Usage

first of all create an environment (I used pipenv for that) and install requerements

    pip install pipenv
    pipenv install Pipfile


then to create a database and see cities data run command

    python dbconnect.py

then to add weather info to the **database** via `city_id`  from  http://api.darksky.net run command

    python project.py 2
    python project.py 3

here 2 and 3 are arguments (`city_id`)

then to get *csv* file run command with `fname`

    python run.py myfile
    python run.py secondfile

#   

## How it Works

first it creates database with two tables *cities* and *weather* 

then it inserts data to *cities* table

then it fetches data from the url by `city_id` and checks time of last insert in *weather* table, whether it is more than 1 minute earlier, if so inserts them to *weather* table 

then it saves all data in *weather* table into `fname`.csv file


#
