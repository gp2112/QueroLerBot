from querolerbot.config import read_config
import sqlite3

config = read_config()
db_name = config['database']['name']

def create_db():
	print(f'Criando {db_name}...')
	conn = sqlite3.connect(db_name)
	print('Banco de dados criado!\n')

	print('Criando tabela articles... ')
	cursor = conn.cursor()
	query = '''
	CREATE TABLE articles (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		title VARCHAR(255) NOT NULL,
		main_url VARCHAR(300) NOT NULL,
		telegraph VARCHAR(255) NOT NULL
	);

	'''
	cursor.execute(query)
	print('Tabela criada com sucesso!\n')
	
	print('Indexando title...')
	query = '''
	CREATE UNIQUE INDEX title_index
	ON articles (title);
	'''
	cursor.execute(query)

	print('Indexando main_url...')
	query = '''
	CREATE UNIQUE INDEX main_url_index
	ON articles (main_url);
	'''
	cursor.execute(query)

	print('Indexando telegraph...\n')
	query = '''
	CREATE UNIQUE INDEX telegraph_index
	ON articles (telegraph);
	'''
	cursor.execute(query)

	print('articles.db criado com sucesso!')

	conn.close()


def insert_article(title=None, main_url=None, telegraph=None):
	if None not in (title, main_url, telegraph):
		conn = sqlite3.connect(db_name)

		cursor = conn.cursor()
		query = '''
		INSERT INTO articles (title, main_url, telegraph)
		VALUES (?, ?, ?)
		'''
		cursor.execute(query, (title, main_url, telegraph))
		conn.commit()

		conn.close()

def get_article(main_url=None, title=None):
	if (main_url, title) == (None, None):
		return None
	conn = sqlite3.connect(db_name)
	cursor = conn.cursor()
	if main_url is not None:
		cursor.execute('SELECT telegraph FROM articles WHERE main_url=?', (main_url,))
	if title is not None:
		cursor.execute('SELECT telegraph FROM articles WHERE title=?', (title,))
	r = cursor.fetchone()
	conn.close()
	return r

def get_all_articles():
	conn = sqlite3.connect(db_name)
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM articles')
	r = cursor.fetchall()
	conn.close()
	return r

def delete_article(main_url=None, title=None):
	conn = sqlite3.connect(db_name)
	cursor = conn.cursor()
	if main_url is not None:
		cursor.execute('DELETE FROM articles WHERE main_url=?', (main_url,))
	elif title is not None:
		cursor.execute('DELETE FROM articles WHERE title=?', (title,))
	else:
		cursor.execute('DELETE FROM articles')
	conn.commit()
	conn.close()

if __name__ == '__main__':
	create_db()
