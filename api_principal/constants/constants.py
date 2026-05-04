from dotenv import load_dotenv
import os

load_dotenv()
sex_options =  ['m', 'M', 'f', 'F', 'n', 'N']
default_date_format = '%Y-%m-%d'
api_key= os.getenv("API_KEY")
