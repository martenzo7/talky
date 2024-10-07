from tqdm import tqdm
import requests

chunk_size = 1024

url = ""


r = requests.get(url, stream = True)

total_size = int(r.headers['content-length'])
filename = url.split('/')[-1]

with open('/tmp/'+filename, 'wb') as f:
	for data in tqdm(iterable = r.iter_content(chunk_size = chunk_size), total = total_size/chunk_size, unit = 'KB'):
		f.write(data)


print("Download complete!")
