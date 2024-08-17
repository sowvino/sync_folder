import logging
import hashlib

#set logging info which displays in log file
def set_logging(file_path):
    logging.basicConfig (
        filename=file_path,
        filemode='a',
        format= '%(asctime)s - %(levelname)s-%(message)s',
        level=logging.INFO
    )


#compare the hash md5 in both source and replica folder
def compare_files(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        return hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
