python 
import http.client
import json 
import os 
from dotenv import load_dotenv 

load_dotenv()
API_KEY = os.getenv("IMDB_API_KEY")
API_HOST = os.getenv("IMDB_HOST","imdb236.p.rapidapi.com")
OUTPUT_DIR = "data"

if not API_KEY: 
    raise ValueError("Please set IMDB_API_KEY in the .env file.")   


os.makedirs(OUTPUT_DIR,exist_ok=True)   
conn = http.client.HTTPSConnection(API_HOST) 
headers = {
    'x-rapidapi-key':API_KEY,
    'x-rapidapi-host':API_HOST
}

conn.request("GET","/api/imdb/top250_movies", headers=headers)   
res = conn.getresponse()   
data = res.read()
movies = json.loads(data.decode("utf-8"))
print(f"Fetched {len(movies)} tv shows successfully.")

json_path = os.path.join(OUTPUT_DIR,"top250_tvshows.json")
with open(json_path,"w",encoding="utf-8") as f:
    json.dump(movies,f,indent=4, ensure_ascii=False)
    
print(f"saved : {json_path}")

ndjson_path = os.path.join(OUTPUT_DIR,"top250_tvshows.ndjson")
with open(ndjson_path,"w",encoding="utf-8") as f:
    for movie in movies:
        f.write(json.dumps(movie) + "\n")

print(f"saved : {ndjson_path}")
print("Done! :) ")
