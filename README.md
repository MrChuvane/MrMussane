# MrMussane
robo-vagas-scraper
O problema que resolve
Procurar vaga em Moçambique significa visitar manualmente dezenas de sites diferentes todos os dias. Este script automatiza essa busca: em vez de abrir 15 sites um a um, corre tudo de uma vez e devolve uma lista organizada das vagas relevantes.

Como funciona, passo a passo

Lista de sites-alvo — o script tem uma lista de 15 sites de emprego moçambicanos e internacionais relevantes para Moçambique (LinkedIn Jobs, Vaga.co.mz, UN Jobs, ImpactPool, NGO Jobs in Africa, Trampomoz, entre outros).
Pedido HTTP a cada site (requests.get) — com um timeout de 10 segundos, para não ficar bloqueado se um site não responder.
Leitura do HTML com BeautifulSoup — a biblioteca transforma o HTML bruto da página numa estrutura que o Python consegue percorrer.
Extracção de todos os links (soup.find_all('a')) — depois, para cada link, verifica se o texto contém alguma das palavras-chave definidas (Monitoria, Avaliação, Análise de Dados, Gestão de Dados, Analista, etc.), ignorando maiúsculas/minúsculas.
Resolução de URLs relativas — alguns sites usam links relativos (ex.: /vaga/123); o script detecta isso e completa com o endereço do site de origem.
Consolidação num DataFrame (pandas) — todas as vagas encontradas em todos os sites são juntas numa única tabela, com três colunas: título, link e site de origem.
Remoção de duplicados (drop_duplicates) — evita listar a mesma vaga duas vezes.
Exportação com data automática — gera um ficheiro vagas_AAAAMMDD.xlsx/.csv, para manter um histórico diário das vagas encontradas.
Tratamento de erros — cada site é processado dentro de um try/except, por isso se um site estiver em baixo ou mudar de estrutura, o script não pára — só regista o erro e continua para o próximo.
