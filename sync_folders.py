import os
import shutil
import time
import argparse
import utilis


#synchronize folders from source to replica. 
def synchronize_folders(source_folder,replica_folder):
    #check whether all directory is present in replica
    for file in os.listdir(source_folder):
        source_path = os.path.join(source_folder,file)
        replica_path = os.path.join(replica_folder,file)

        if os.path.isdir(source_folder):
            if not os.path.exists(replica_folder):
                os.makedirs(replica_path)
                utilis.logging.info(f"Directory is created:{replica_path}")
                print(f"Directory created: {replica_path}")
                synchronize_folders(source_path,replica_path)

            else:
                if not os.path.exists(replica_path) or utilis.compare_files(source_path,replica_path):
                    shutil.copy2(source_path,replica_path)
                    utilis.logging.info(f"Copied file from {source_path}")
                    print(f"Copied file :{source_path}")

    
    for file in os.listdir(replica_folder):
        source_path = os.path.join(source_folder,file)
        replica_path = os.path.join(replica_folder,file)

        if not os.path.exists(source_path):
            if os.path.exists(replica_path):
                shutil.rmtree(replica_path)
                utilis.logging.info(f"Removed directory from {replica_path}")
                print(f"Removed directory:{replica_path}")
            
            else:
                os.remove(replica_path)
                utilis.logging.info(f"Removed file :{replica_path}")
                print(f"Removed file:{replica_path}")

def main():
    parser = argparse.ArgumentParser(description="Synchronisation folders")
    parser.add_argument('source_folder',type=str,help="Path to source")
    parser.add_argument('replica_folder',type=str,help="path to replica")
    parser.add_argument('log_file',type=str,help="path to log_file")

    args = parser.parse_args()

     # Ensure that source and replica folders exist
    if not os.path.exists(args.source_folder):
        os.makedirs(args.source_folder)
        print(f"Created source folder: {args.source_folder}")

    if not os.path.exists(args.replica_folder):
        os.makedirs(args.replica_folder)
        print(f"Created replica folder: {args.replica_folder}")

    utilis.set_logging(args.log_file)

    while True:
        synchronize_folders(args.source_folder,args.replica_folder)
        utilis.logging.info("File Synchronized")
        print("File Synchronized")
        time.sleep(60)

main()

