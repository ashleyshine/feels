#!python3.6
import urllib3
from bs4 import BeautifulSoup

def get_script_text(http, url):
	"""
	Grab script title and text from url. 
	Params:
		http: PoolManager
		url: string with url of script
	"""
	request = http.request('GET', url)
	title, text = ['', '']

	if request.status == 200:
		html = request.data
		soup = BeautifulSoup(html, 'html.parser')
		title = soup.find('h3').get_text()
		text = soup.find('div', {'class': 'scrolling-script-container'}).get_text()
	else:
		print("Request failed for url: {}".format(url))

	return [title, text]


def save_script(title, text):
	"""
	Save script to text file.
	Params:
		title: string
		text: string
	"""
	with open('./scripts/{}.txt'.format(title), 'w') as f:
		print('Writing to ./scripts/{}.txt'.format(title))
		f.write(text.strip())


def main():
	http = urllib3.PoolManager()
	urls = ['https://www.springfieldspringfield.co.uk/view_episode_scripts.php?tv-show=master-of-none-2015&episode=s02e08']

	for url in urls:
		title, text = get_script_text(http, url)
		if title != '' and text != '':
			save_script(title, text)

if __name__=='__main__':
	main()
