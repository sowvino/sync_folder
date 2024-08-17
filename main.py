import logging
import hashlib
import os
import shutil
import time
import argparse

#sets logging record in a log_file
def set_logging(file_path):
    logging.basicConfig(
        filename=file_path,
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

#compare two folders using md5 hash
def compare_files(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        return hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()

#synchonize folders
def synchronize_folders(source_folder, replica_folder):
#checks whether all directory and files exists in replica if not it creates directory or copies files
    for file in os.listdir(source_folder):
        source_path = os.path.join(source_folder, file)
        replica_path = os.path.join(replica_folder, file)

        if os.path.isdir(source_path):
            if not os.path.exists(replica_path):
                os.makedirs(replica_path)
                logging.info(f"Directory created: {replica_path}")
                print(f"Directory created: {replica_path}")
            synchronize_folders(source_path, replica_path)
        else:
            if not os.path.exists(replica_path) or not compare_files(source_path, replica_path):
                shutil.copy2(source_path, replica_path)
                logging.info(f"Copied file: {source_path} to {replica_path}")
                print(f"Copied file: {source_path}")

#checks all files present in replica with source if not removes the directory or files
    for file in os.listdir(replica_folder):
        source_path = os.path.join(source_folder, file)
        replica_path = os.path.join(replica_folder, file)

        if not os.path.exists(source_path):
            if os.path.isdir(replica_path):
                shutil.rmtree(replica_path)
                logging.info(f"Removed directory: {replica_path}")
                print(f"Removed directory: {replica_path}")
            else:
                os.remove(replica_path)
                logging.info(f"Removed file: {replica_path}")
                print(f"Removed file: {replica_path}")

#define what arguments should be present in command line
def main():
    parser = argparse.ArgumentParser(description="Synchronize folders")
    parser.add_argument('source_folder', type=str, help="Path to source")
    parser.add_argument('replica_folder', type=str, help="Path to replica")
    parser.add_argument('log_file', type=str, help="Path to log file")
    parser.add_argument('--time_interval', type=int, default=60, help='Time interval for synchronization in seconds')

    args = parser.parse_args()
#if source file not exists it makes source directory
    if not os.path.exists(args.source_folder):
        os.makedirs(args.source_folder)
        print(f"Created source folder: {args.source_folder}")
#if replica filenot exists it makes replica directory
    if not os.path.exists(args.replica_folder):
        os.makedirs(args.replica_folder)
        print(f"Created replica folder: {args.replica_folder}")
#creates log record of the sync in log_file
    set_logging(args.log_file)

    # Loop to synchronize the folders at the given time interval
    while True:
        synchronize_folders(args.source_folder, args.replica_folder)
        logging.info("Files synchronized")
        print("Files synchronized")
        time.sleep(args.time_interval)

if __name__ == "__main__":
    main()
