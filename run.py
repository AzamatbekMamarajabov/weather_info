import sys
import os
import csv
basedir = os.path.abspath(os.path.dirname(__file__))

from dbconnect import select_weather_all, insert_weather, select_weather_by_city, create_connection

first_arg = sys.argv[1]


def csv_download(fname, result):
    """This funtion is used for downloading result as a csv file """
   
    with open('{bd}/{fn}.csv'.format(bd=basedir,fn=fname), 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for sub_list in result:
            rows = sub_list
            writer.writerow(rows)


if __name__ == '__main__':
    database = os.path.join(basedir, 'data.db')

    # create a database connection
    conn = create_connection(database)

    
    with conn:

        print("Query all weather")
        result = select_weather_all(conn)
       
        csv_download(first_arg, result)

