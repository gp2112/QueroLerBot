from bs4 import BeautifulSoup
from urllib.parse import urlparse
from telegraph import Telegraph
import database
import json
import requests

telegraph_user = '@queroler_bot'

banned_tags = (
		'span', 'small', 'div', 'label', 'svg', 'g', 'path', 'script', 'sub'
	)


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
		classes = json.load(f)

	if domain in classes:
		el = soup.find(class_=classes[domain])
		if el is not None:
			parag = ''
			for p in el.findAll(('p', 'img')):
				parag += str(remove_tags(p, banned_tags))
			return parag, soup.title.string
	return None, None


def break_paywall(url):
	parag, title = get_news_content(url)
	if parag is None: 
		return None

	#r = gen_pastebin(parag, title)

	parag += f'<a href="{url}">Artigo Original</a>'

	telegraph = Telegraph()
	telegraph.create_account(short_name=telegraph_user)

	r = telegraph.create_page(title, html_content=parag, author_name=urlparse(url).netloc)

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
