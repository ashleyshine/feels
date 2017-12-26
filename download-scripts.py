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

		show_info = soup.find('h1').get_text()
		season_and_ep = extract_season_and_episode(show_info)
		title = soup.find('h3').get_text()

		text = soup.find('div', {'class': 'scrolling-script-container'}).get_text()
	else:
		print("Request failed for url: {}".format(url))

	return ['-'.join([season_and_ep, title]), text]


def extract_season_and_episode(text):
	"""
	Extract episode season & number info from string.
	Params:
		text: string
	"""
	regex_str = ".*(s\d+e\d+).*"
	mo = re.search(regex_str, text, re.IGNORECASE)
	if mo:
		return mo.group(1)
	else:
		return ''


def save_script(title, text, directory):
	"""
	Save script to text file in directory.
	Params:
		title: string
		text: string
        directory: string
	"""
	file_name = '-'.join(title.split())
	with open('{}/{}.txt'.format(directory, file_name), 'w') as f:
		print('Writing to {}/{}.txt'.format(directory, file_name))
		f.write(text.strip())


def main():
	save_directory = './master-of-none'

	http = urllib3.PoolManager()
	main_url = "https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=master-of-none-2015"
	urls = get_urls(http, main_url)
   
	for url in urls:
		title, text = get_script_text(http, url)
		if title != '' and text != '':
			save_script(title, text, save_directory)

if __name__=='__main__':
	main()
