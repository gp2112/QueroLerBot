import toml
import os


config_path = os.environ.get('QUEROLER_CONFIG_PATH', '')

default = {
        'general': {
            'delay': 15
        },
        'twitter': {
            'username': 'querolerbot',
            'api_url': 'https://api.twitter.com/'
        },
        'telegraph': {
            'username': '@querolerbot',
            'url': 'https://graph.org/'
        },
        'messages': {
            'success': [
                "Aqui está seu artigo sem paywall :)",
                "Bip, bop",
                "Saindo do forno ;)",
                "Tá sentindo? Cherinho de artigo sem paywall <3",
                "Ahoy",
                "Hello There..."
            ],
            'error': {
                'url_not_found': 'Não achei nenhum link :(',
                'text_not_found': 'Infelizmente não consegui encontrar o texto ou o site ainda não é suportado :(\nVeja os sites compatíveis no meu perfil :)'
            }
        },
        'database': {
            'name': 'articles.db'
        }
}


def read_config():
    with open(config_path) as f:
        config = toml.load(f)
    return config


def generate_config_file():
    with open(config_path, 'w') as f:
        toml.dump(default, f)


def check_config_file():
    try:
        with open(config_path, 'r') as _:
            pass
    except FileNotFoundError as err:
        print(err)
        print('Generating config file...')
        generate_config_file()
