import os
import kagglehub
from dotenv import load_dotenv
import shutil

# 1. Environment Setup: Load API credentials from .env file
load_dotenv()
os.environ['KAGGLE_USERNAME'] = os.getenv('KAGGLE_USERNAME')
os.environ['KAGGLE_KEY'] = os.getenv('KAGGLE_KEY')

# 2. Data Acquisition: Download dataset from Kaggle
path = kagglehub.dataset_download("prashant111/the-simpsons-dataset")
print(f"Success! Data is at: {path}")

# 3. Target directory for project data
local_data_dir = "data/simpsons_raw"

# 4. To copy files from global cache to local project folder
if not os.path.exists(local_data_dir):
    os.makedirs("data", exist_ok=True)
    shutil.copytree(path, local_data_dir) # copytree copies the entire folder structure
    print(f"Files moved to your project! Look in: {local_data_dir}")
else:
    print(f"Files already exist in {local_data_dir}")