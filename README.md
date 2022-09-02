# QueroLerBot
Bot para driblar os paywalls no Twitter

<a href="https://twitter.com/QuerolerBot">@QueroLerBot</a>

## Como o Bot funciona ?

Quando uma pessoa marca o @QueroLerBot em um Tweet com uma URL, o bot 
irá procurar pelo conteúdo do artigo baseado nas classes do elemento HTML do conteúdo,
previamente coletados, no arquivo "news_classes.json". O nome da classe pode variar no mesmo site,
dependendo da página.
Com o conteúdo coletado, ele envia para o graph.org, onde ficará armazenado.
Para evitar fazer o mesmo processo para os mesmos artigos, tanto a url do artigo quanto a url do
conteúdo no graph.org, ficam salvos num simples banco de dados sqlite. 
Assim, quando o bot é acionado, a primeira coisa que ele faz é verificar se o artigo já existe na db.

## Como rodar ?

1. Faça o download ou clone o repositório:
  ```bash 
  git clone https://github.com/gp2112/QueroLerBot.git
  ```
2. Usando o poetry:
  ```bash
  poetry install
  ```
3. Rode o database.py para gerar o banco de dados.
4. Coloque seus tokens e keys da api do twitter nas variáveis de ambientes especificadas:
```bash
export QUEROLER_CONSUMER_KEY='sua consumer_key'
export QUEROLER_CONSUMER_SECRET='sua consumer_secret'
export QUEROLER_ACCESS_KEY='sua access_key'
export QUEROLER_ACCESS_SECRET='sua access_secret'

```

5. Rode `poetry run querolerbot`

## Como contribuir ?
Sinta-se a vontade para contribuir com o que quiser.
Umas ideias pra contribuir são:
* Simplificar ao máximo a interação com o usuário
* Adicionar novas classes de conteúdo para dar suporte a novos sites em news_classes.json
* Adicionar mensagens legais na tupla succ_msgs em app.py.
* Organizar mais o código, deixar limpo,

## Como achar as classes de conteúdo nos sites?
Na página do artigo, selecione algum trecho do conteúdo do artigo e inspecione o elemento.
Agora só buscar pelo elemento "pai" e coletar sua classe.
Feito isso, adicione o endereço do site e sua classe no news_classes.json, seguindo o modelo dos outros.
Segue um exemplo abaixo com um artigo do Globo:

![image](https://user-images.githubusercontent.com/26512375/114201969-20ee5380-992d-11eb-9616-31e16f8bfc87.png)
