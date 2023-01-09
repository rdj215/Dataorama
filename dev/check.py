import hashlib
from math import ceil
import os
 
 
 # perfroms checksum on file

    # function that returns the size of a file in bytes 
def get_file_size(file):
    return os.path.getsize(file)
    

def check_file(q):
    for _ in range(q.qsize()):
        file=q.get()
        print(f'Got file {file}')
        print('\ninside of check file\n')
        file_size = get_file_size(file)
        md5 = hashlib.md5()
        md5_2 = hashlib.md5()

        def write_results():
            with open('checksum.text', 'a') as result_file:
                result_file.write(os.path.splitext(file)[0])
                result_file.write(f'{md5.hexdigest()} \n')
                result_file.close()
        
        # opens passed file to be read in bytes 
        with open(file, 'rb') as file2:
            original = file2.read() # read entire file in bytes 
            file2.seek(0) # set current file position back to beginning of file

            # reads bytes in chunks of 32
            for _ in range(ceil(file_size/32)):
                    b = file2.read(32)
                    md5.update(b)
            
            file2.close()
            write_results()
            md5_2.update(original)

        

            if md5.digest() == md5_2.digest():
                print('files match')
            else:
                print('files do not match')