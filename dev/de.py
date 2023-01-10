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


    # file_names = ['C:\\Users\\ryanj\\Dataorama\\dev\\file1.txt', 'C:\\Users\\ryanj\Dataorama\\dev\\file2.txt', 'C:\\Users\\ryanj\\Dataorama\\dev\\file3.txt']
    file_names = []
    def file_handler():
        """Function that takes file names as argumments and returns the file path"""
        file_name = input("Enter file name: ")
        directory_name = input("Enter the diretory the path is located in: ")
        # path =os.path.join("C:\\Users\\",file_name)
        path = os.path.relpath(file_name)
        file_names.append(path)
        return

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

        
    file_handler()
    checksum(file_names, 1, q )
    print(q.qsize())
    print(check_file.__doc__)



        

        
            
            

        
        


                
    
    




            


