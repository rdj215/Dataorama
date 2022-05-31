import os
from dotenv import load_dotenv
import requests
import pathlib
import json
import psycopg2

load_dotenv('.env')


# url_birth = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Vital_Natality_Cty/FeatureServer/0/query?where=1%3D1"

# endpoint for pollling data in philadelphia
url_polling = "https://phl.carto.com/api/v2/sql?q=SELECT * FROM polling_places"
# url_turnout2018 = "https://phl.carto.com/api/v2/sql?q=SELECT * FROM voter_turnout_primary_election_2018"
res = requests.get(url_polling) # make get request
res_json = json.dumps(res.json(), indent=4) # wrap json object in srtings
res_json = json.loads(res_json) # convert json object to dict
arr = []
row_keys = res_json['fields'].keys() # get keys from returned response

## get keys from response 
res_json_keys = res_json.keys() 
total = res_json['total_rows']



print(res_json.keys()) 
print(res_json['time'])
print(res_json['fields'].keys())
print(res_json['rows'][0])
print(f" total rows: {total}  type: {type(total)}")
print(f"DB: {os.environ.get('DBNAME')}")
print(f"USER: {os.environ.get('USER')}")


# create connection object
conn = psycopg2.connect(f"dbname={os.environ.get('DBNAME')} user={os.environ.get('USER')} password={os.environ.get('PASSWORD')}")
# open cursor
cur = conn.cursor()

#####  TABLE CREATION STATEMENTS ########

cur.execute("DROP TABLE IF EXISTS test.polling_places")
cur.execute("""CREATE TABLE test.polling_places 
(              objectid varchar(600),
               ward integer, 
               division integer, 
               precinct integer,
               placename varchar(150),
               street_address varchar(150),
               zipcode integer,
               accessibility_code varchar(5),
               parking_code varchar(5)
               
) 
""")


# loop over results and insert into database
count = 0 
for i in range(total):
    
    # print(res_json['rows'][i])
    row = res_json['rows'][i].values()
    row = [x for x in row]
    row_test = len(row)
    row.pop(0)
    row.pop(1)
    row.pop(2)
    # print(row)
    row = tuple(row)

    try:
        cur.execute("""INSERT INTO test.polling_places (
               objectid,
               ward , 
               division, 
               precinct,
               placename, 
               street_address,
               zipcode,
               accessibility_code ,
               parking_code
               )
               

               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               """,
               row
    )

        count+=1
        print(f'Inserted {count} record(s) Remaining: {total-count}')


    except Exception as e:
        print(f"ERROR : {e}")
        print(len(row))
        print(row_test)
        

print("the program is still executing")   


    
  

conn.commit()
cur.close()
conn.close()






