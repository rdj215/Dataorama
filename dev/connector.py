import os
from queue import Queue
from webbrowser import get
from dotenv import load_dotenv
import requests
import pathlib
import json
import psycopg2
from multiprocessing import Process, Queue
import get_url2


load_dotenv('.env')

if __name__ == '__main__':
    # url_birth = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Vital_Natality_Cty/FeatureServer/0/query?where=1%3D1"

    # endpoint for pollling data in philadelphia
    url_polling = "https://phl.carto.com/api/v2/sql?q=SELECT * FROM polling_places"
    url_turnout2018 = "https://phl.carto.com/api/v2/sql?q=SELECT * FROM voter_turnout_primary_election_2018"

    urls = [url_polling, url_turnout2018]

    q = Queue()

    for url in urls:
        q.put(url)






    # def req(url):
    #     res = requests.get(url) # make get request
    #     res_json = json.dumps(res.json(), indent=4) # wrap json object in srtings
    #     res_json = json.loads(res_json) # convert json object to dict
    #     # arr = []
    #     # print(f"Fields returned from this request: {res_json['fields'].keys()}")
    #     return res_json
        # return res_json['fields'].keys() # get keys from returned response
        # print(row_keys)
        # return row_keys

    ## get keys from response 

    first_run = True

    # def get_response(url):
    #     res_json = req(url)
    #     res_json_keys = res_json.keys()
    #     total = res_json['total_rows']
    #     return (res_json, total)

    def clean_rows(res_json):

        
                
            # print(res_json['rows'][i])
            row = res_json[0]['rows'][i].values()
            row = [x for x in row]
            row_test = len(row)
            row.pop(0)
            row.pop(1)
            row.pop(2)
            # print(row)
            row = tuple(row)
            return row
        


    for _ in range(q.qsize()):
        p = Process(target=get_url2.get_url, args=(q,))
        p.start()
        


        


        # create connection object
        if first_run:
            conn = psycopg2.connect(f"dbname={os.environ.get('DBNAME')} user={os.environ.get('USER')} password={os.environ.get('PASSWORD')}")
            # open cursor
            first_run = False
            cur = conn.cursor()


        def insert(q):
        #####  TABLE CREATION STATEMENTS ########
            if url == url_polling:
                print('in ur create')
                cur.execute("DROP TABLE IF EXISTS test.polling_places")
                cur.execute("""CREATE TABLE test.polling_places 
                (           objectid varchar(600),
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
            elif url == url_turnout2018:
                cur.execute("DROP TABLE IF EXISTS test.turnout2018")
                cur.execute(""" CREATE TABLE test.turnout2018(
                            election varchar(45),
                            election_date varchar(55),
                            precinct_description varchar(500),
                            precinct_code varchar(500),
                            political_party varchar(500),
                            voter_count varchar(50)
                )
                """)


                # loop over results and insert into database
                count = 0 
                error_count = 0
                # clean_rows(res_json)

                for i in range(p[1]):
                    row = clean_rows(p)
                    
                #     # print(res_json['rows'][i])
                #     row = res_json[0]['rows'][i].values()
                #     row = [x for x in row]
                #     row_test = len(row)
                #     row.pop(0)
                #     row.pop(1)
                #     row.pop(2)
                #     # print(row)
                #     row = tuple(row)
                    

                    # print(f'Tuple : {len(row)}')

                    # try:
                    print(f'\n right before first if cyrrent url: {url}')

                    if url == url_polling:
                        print(' \n in polling if \n')
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
                        conn.commit()
                        print('inserted')
                    if url == url_turnout2018  :
                        cur.execute("""INSERT INTO test.turnout2018 
                        (
                                    election, 
                                    election_date, 
                                    precinct_description, 
                                    precinct_code, 
                                    political_party,
                                    voter_count
                        )
                                    
                                    VALUES (%s, %s, %s, %s, %s, %s)""",
                                    row
                                    )

                        count+=1
                        # conn.commit()
                        # if url == url_polling:

                        #  print(f'Inserted {count} record(s) Remaining: {total-count}')


                    # except Exception as e:
                    #     print(f"ERROR -- exception caught: {e}")
                    #     error_count+=1
                    #     print(error_count)
                    
                        

                conn.commit()
                return "Done"

        
    cur.close()
    conn.close()






