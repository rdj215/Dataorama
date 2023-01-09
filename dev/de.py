if __name__ == '__main__' :
    from ast import NamedExpr
    from math import ceil
    from msilib.schema import File
    import multiprocessing as mp
    import hashlib
    import os
    import threading
    import multiprocessing
    from check import check_file

    q = mp.Queue()
    pcs = []


    file_names = ['C:\\Users\\ryanj\\Dataorama\\dev\\file1.txt', 'C:\\Users\\ryanj\Dataorama\\dev\\file2.txt', 'C:\\Users\\ryanj\\Dataorama\\dev\\file3.txt']
   
    # def file_handler(file, directory):
    #     """Function that takes file names as argumments and returns the file path"""
    #     file

    def checksum(files, num_threads, q): 
        """Performs checksum on files using seperate proccesses"""

        for i in range(len(files)):
            q.put(files[i])

        chunk_size = ceil(len(files)/num_threads) #calculates chunk size based on number of fils in file_names
        for i in range(0, num_threads, chunk_size): # will determine how many proccesses are created
            print('\n for loop \n')
            p = mp.Process(target=check_file, args=(q,))
            p.start()
            pcs.append(p)

        for p in pcs:
            print('about to join')
            p.join()

        

    checksum(file_names, 2, q )
    print(q.qsize())
    print(check_file.__doc__)



        

        
            
            

        
        


                
    
    




            


