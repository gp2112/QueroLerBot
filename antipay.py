from bs4 import BeautifulSoup
from urllib.parse import urlparse
import database
import json
import requests

telegraph_user = '@queroler_bot'

banned_tags = (
		'span', 'small', 'div', 'label', 'svg', 'g', 'path', 'script'
	)

pastebin_token = '7Fp3iWc0yHZ_J9J85kOQ0bSJt0W62c5-'

def gen_pastebin(token, content, title):
	print(title)
	data = {
		'api_dev_key':token,
		'api_paste_code':content.strip("'"),
		'api_option':'paste',
		'api_paste_name':title.strip()[0:100]
	}
	r = requests.post('https://pastebin.com/api/api_post.php', data=data) 
	return r.text

def remove_tags(el, tags):
	for tag in tags:
		for match in el.findAll(tag):
			match.unwrap()
	return el

def get_news_content(url):
	domain = urlparse(url).netloc
	r = requests.get(url)
	r.encoding = r.apparent_encoding
	soup = BeautifulSoup(r.text, 'html.parser')
	with open('news_classes.json', 'r') as f: 
		domains = json.load(f)
	if domain in domains:
		class_ = domains[domain]
		el = soup.find(class_=class_)
		parag = ''
		for p in el.findAll('p'):
			parag += '\n'+p.getText()
		return parag, soup.title.string
	return None, None


def break_paywall(url):
	parag, title = get_news_content(url)
	if parag is None: 
		return None

	r = gen_pastebin(pastebin_token, parag, title)
	data = {'telegraph':r, 'title':title, 'main_url':url}
	return data


if __name__ == '__main__':
	if len(sys.argv) > 1:
		if sys.argv[1] == '--db':
			database.create_db()
	url = input('url: ')
	article = database.get_article(url)
	if article is None:
		article = break_paywall(url)
		if article is None:
			print('Não foi possivel')
		else:
			database.insert_article(**article)
			article = article['telegraph']

	else: article = article[0]

	print(article)