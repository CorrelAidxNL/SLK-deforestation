########################################################################################
# The code assumes that the sourse links came from https://www.chelsa-climate.org/datasets/chelsa_monthly
# and saved in text files. The folders should be created for every output.
# To run the script print in command prompt:
#   1. conda activate Deforestation   # activate your anaconda environment
#   2. cd "C:\Users\oleks\Desktop\DEFORESTATION\2 Logistic regression"
#   3. python "1 download_CHELSA.py"
# The rasters will be saved into specified folders
#######################################################################################






# import packages
import os
import re
import requests
from time import sleep

###################################################################
# 1. List of input txt files and their corresponding output folders
###################################################################
#tasks = [
    #{
        #"txt_file": r"C:\Users\oleks\Desktop\DEFORESTATION\2 Logistic regression\1 RAW DATA\5 CHELSA 1 km\tasmax.txt",
        #"output_folder": r"C:\Users\oleks\Desktop\DEFORESTATION\2 Logistic regression\1 RAW DATA\5 CHELSA 1 km\1 tasmax"
    #},
    #{
        #"txt_file": r"C:\Users\oleks\Desktop\DEFORESTATION\2 Logistic regression\1 RAW DATA\5 CHELSA 1 km\tasmin.txt",
        #"output_folder": r"C:\Users\oleks\Desktop\DEFORESTATION\2 Logistic regression\1 RAW DATA\5 CHELSA 1 km\2 tasmin"
    #},
    #{
        #"txt_file": r"C:\Users\oleks\Desktop\DEFORESTATION\2 Logistic regression\1 RAW DATA\5 CHELSA 1 km\vpd.txt",
        #"output_folder": r"C:\Users\oleks\Desktop\DEFORESTATION\2 Logistic regression\1 RAW DATA\5 CHELSA 1 km\3 vpd"
    #},
    #{
        #"txt_file": r"C:\Users\oleks\Desktop\DEFORESTATION\2 Logistic regression\1 RAW DATA\5 CHELSA 1 km\pr.txt",
        #"output_folder": r"C:\Users\oleks\Desktop\DEFORESTATION\2 Logistic regression\1 RAW DATA\5 CHELSA 1 km\4 pr"
    #},
#]


tasks = [
        {
        "txt_file": r"C:\Users\oleks\Desktop\DEFORESTATION\2 Logistic regression\1 RAW DATA\5 CHELSA 1 km\spei12.txt",
        "output_folder": r"C:\Users\oleks\Desktop\DEFORESTATION\2 Logistic regression\1 RAW DATA\5 CHELSA 1 km\4 spei"
    },
]



###################################################################
# 2. Extract year from URL
###################################################################
def extract_year(url):
    match = re.search(r"_(19|20)\d{2}_", url)
    if match:
        return int(match.group(0).replace("_", ""))
    return None


###################################################################
# 3. Extract year from URL
###################################################################
def download_file(url, out_path, retries=3):
    if os.path.exists(out_path):
        print(f"[SKIP] {out_path} already exists")
        return

    for attempt in range(retries):
        try:
            print(f"[DOWNLOADING] {url}")
            response = requests.get(url, stream=True, timeout=60)
            if response.status_code == 200:
                with open(out_path, "wb") as f:
                    for chunk in response.iter_content(1024*1024):
                        f.write(chunk)
                print(f"[DONE] {out_path}")
                return
            else:
                print(f"[ERROR] Status {response.status_code} for {url}")
        except Exception as e:
            print(f"[ERROR] Attempt {attempt+1}: {e}")
            sleep(2)

    print(f"[FAILED] Could not download {url}")


###################################################################
# 4. Looping and downloading rasters
###################################################################
for task in tasks:
    txt_file = task["txt_file"]
    base_folder = task["output_folder"]

    # create folder if it does not exist
    os.makedirs(base_folder, exist_ok=True)

    # read URLs from txt file
    with open(txt_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"\nProcessing {txt_file} ({len(urls)} URLs) -> {base_folder}")

    for url in urls:
        year = extract_year(url)
        if year is None:
            print(f"[WARNING] Could not extract year: {url}")
            continue

        # download years 2000–2020
        if not (2000 <= year <= 2020):
            continue

        year_folder = os.path.join(base_folder, str(year))
        os.makedirs(year_folder, exist_ok=True)

        filename = os.path.basename(url)
        out_path = os.path.join(year_folder, filename)

        download_file(url, out_path)

print("\nAll downloads completed for 2000–2020.")