from bs4 import BeautifulSoup
from urllib.parse import urlparse
from telegraph import Telegraph
import database
import json
import requests

telegraph_user = '@queroler_bot'

banned_tags = (
		'span', 'small', 'div', 'label', 'svg', 'g', 'path', 'script'
	)

'''
pastebin_token = '7Fp3iWc0yHZ_J9J85kOQ0bSJt0W62c5-'

def gen_pastebin(content, title): 
	print(title) 
	r = requests.post('http://penyacom.org/api/v1/paste.php', data={'code':title+'\n\n'+content})
	return r.json()['raw_link']
'''

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
	with open('classes', 'r') as f: 
		classes = f.read().split('\n')

	for class_ in classes:
		el = soup.find(class_=class_)
		if el is not None:
			parag = ''
			for p in el.findAll('p'):
				parag += str(remove_tags(p, banned_tags))
			return parag, soup.title.string
	return None, None


def break_paywall(url):
	parag, title = get_news_content(url)
	if parag is None: 
		return None

	#r = gen_pastebin(parag, title)

	telegraph = Telegraph()
	telegraph.create_account(short_name=telegraph_user)

	r = telegraph.create_page(title, html_content=parag, author_name=telegraph_user)

	data = {'telegraph':'http://graph.org/'+r['path'], 'title':title, 'main_url':url}
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
