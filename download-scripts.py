#!python3.6
import urllib3
from bs4 import BeautifulSoup
import re

# A script to download TV & movie scripts from https://www.springfieldspringfield.co.uk/

def get_urls(http, url):
	"""
	Returns list of links to episode scripts.
	Params:
		http: PoolManager
		url: string with url of show page with links to episode transcripts
	"""
	request = http.request('GET', url)
	base_url = 'https://www.springfieldspringfield.co.uk'
	episode_urls = []

	if request.status == 200:
		html = request.data
		soup = BeautifulSoup(html, 'html.parser')
		episode_container = soup.find_all('div', {'class': 'season-episodes'})

		for container in episode_container:
			for link in container.find_all('a', {'class': 'season-episode-title'}):
				href = link.get('href')
				full_link = '{}/{}'.format(base_url, href)
				episode_urls.append(full_link)
	else: 
		print('Request failed for url: {}'.format(url))

	return episode_urls

def get_script_text(http, url):
	"""
	Grab script title and text from url. Returns [title, text].
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
	file_name = '-'.join(title.split())
	with open('./scripts/{}.txt'.format(file_name), 'w') as f:
		print('Writing to ./scripts/{}.txt'.format(file_name))
		f.write(text.strip())


def main():
	http = urllib3.PoolManager()

	main_url = "https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=master-of-none-2015"
	urls = get_urls(http, main_url)

	for url in urls:
		title, text = get_script_text(http, url)
		if title != '' and text != '':
			save_script(title, text)

if __name__=='__main__':
	main()
