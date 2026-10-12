# As bibliotecas requests, BeautifulSoup (para scraping)
# O pandas (para organizar e remover duplicados)
# O datetime (para nomear o ficheiro com a data)
import requests
from bs4 import BeautifulSoup
import pandas as pd#pd é a forma abreviada de chamar a biblioteca pandas, normalmente importada assim:
from datetime import datetime

# Palavras-chave a procurar previamente escohidas
KEYWORDS = ["Monitoria", "Avaliação", "Análise de dados", "Gestão de dados","Analista de Dados" 
            "Digitação", "Gestão de Programa", "Gestão de Projecto", "Analista","digitador de dados"] # 10 KEYWORDS

# Lista de sites que podem ser adicionados(e futuramente pode-se inverter o processo )
# colocar o requeste para procurar vagas em sites de vagas todos sites de vagas de Moz
SITES = [
    "https://www.trovagas.com",
    "https://www.emprego.co.mz",
    "https://njobs.co.mz/vagas-de-emprego",
    "https://emprego.mmo.co.mz",
    "https://www.linkedin.com/jobs/vagas",
    "https://vaga.co.mz/vagas/view",
    "https://www.careerjet.co.mz/vagas-emprego",
    "https://afrinews24.com/emprego/vaga",
    "https://job.co.mz/",
    "https://trampomoz.com/",
    "https://unjobs.org/duty_stations/mozambique",
    "https://ngojobsinafrica.com/job-location/mozambique/",
    "https://www.impactpool.org/countries/Mozambique",
    "https://vaga.co.mz/",
    "https://vagasempregomoz.com/"
]

#14 sites

def buscar_vagas(url): #def mesmo que função onde temos a variavel buscar_vascas(cujo o parametro é url):
    #def → palavra usada para definir uma função em Python.
    """
    Tenta extrair vagas do site e retorna uma lista de dicionários
    """
    vagas = [] #lista vazia para armazenas as vagas encontradas.
    
    try:
        response = requests.get(url, timeout=10)# faz uma requisição GET. para URL fornecida o  
        #timeout=10 significa nao leva mais de 10segundos
        if response.status_code != 200: #response: é o que a função de requisição (como requests.get
            #como requests.get(...)) retorna. Esse objeto guarda 
            #informação como corpo (conteúdo), cabeçalhos, e o código de status.
            #status_code Atributo do objeto response que contém o código de status HTTP 
            # retornado pelo servidor 
            # (um número inteiro). Exemplos: 200 (OK), 404 (Not Found), 500 (Internal Server Error)
            print(f" Falha ao acessar {url}")#f antes das aspas
            #O f significa que a string é uma f-string (“formatted string”), introduzida no Python 3.6.
            #Ela permite inserir variáveis ou expressões diretamente dentro do texto.
            return vagas

        soup = BeautifulSoup(response.text, 'html.parser')#BeautifulSoup é uma classe da biblioteca 
                #BeautifulSoup4, usada para:
                #Ler HTML;Interpretar HTML,Navegar e extrair informações de uma página web
                #Ela transforma o HTML em uma estrutura organizada que o Python consegue entender.
                #response.text response normalmente é o resultado de algo como:
                # contém o HTML bruto retornado pelo site: Exemplo fictício.'html.parser'
                #Esse é o parsers que o BeautifulSoup vai usar para interpretar o código HTML.
                #'html.parser'parser interno do Python
         
        links = soup.find_all('a')#soup é o objeto criado pelo BeautifulSoup depois de analisar o 
         #HTML da página.Ele representa toda a estrutura da página — como se fosse uma árvore
         #com todas as tags.find_all é um método do BeautifulSoup que:procura todas as ocorrências
         #de uma tag específica.retorna uma lista (um Python list) contendo 
         #todos os elementos encontrados No HTML, a tag <a> é usada para criar links.
         
        for link in links:#lembrar que foi criado com base no soup,Então esse for 
            #está trabalhando link por link encontrado na página.
            texto = link.get_text(strip=True)
            #.get_text() pega o texto dentro da tag <a>.
            #strip=True remove espaços extras no início e final.
            href = link.get('href', '')
            #.get('href') pega o valor do atributo href da tag <a>.
            #Se não existir href, retorna uma string vazia ('').

            if any(k.lower() in texto.lower() for k in KEYWORDS):
                #any(...) significa:“Se qualquer palavra da lista 
                # KEYWORDS está dentro do texto, o if é verdadeiro.”
                #texto.lower() transforma o texto do link em minúsculas
                #k.lower() transforma a keyword em minúsculas
                #k.lower() in texto.lower() verifica se a palavra aparece no texto do link
                #(SEM distinguir maiúsculas/minúsculas)
                vagas.append({
                    #Se o link contiver alguma "keyword", ele é adicionado à lista vagas
                    #Um dicionário com três campos é adicionado:
                    'titulo': texto,#Armazena apenas o texto do link.
                    'link': href if href.startswith('http') else url + href,
                    #Isso resolve a diferença entre URLs completas e URLs relativas.
                    #Explicação:
                    #Se o link começa com "http"  já é um link completo
                    #Ex: https://empresa.com/vaga
                    #Caso contrário o link é relativo (ex: /vaga)
                    #Então ele junta o site + o href
                    'origem': url
                    #Guarda a URL da página onde esse link foi encontrado.
                    #Isso é útil quando você coleta vagas de vários sites e quer saber “de onde veio”.
                })
    except Exception as e:
        #Isso faz parte de um bloco try/except, que serve para capturar erros.
        #Significa:“Se acontecer QUALQUER erro dentro do bloco try, execute este except.”
        #Exception captura praticamente todos os erros possíveis;
        #as e guarda o erro dentro da variável e.
        #Assim você sabe qual erro aconteceu.
        #Exemplo de erros que poderiam cair aqui:
        #Conexão falho,uConversão de dados falhou
        #HTML mal-formado
        #Link sem atributo[]
        
        print(f"Erro ao processar {url}: {e}")
        #Explicando:
        #f"..." f-string (string formatada)
        #{url} mos
        # tra qual URL estava sendo processada
        #{e}  mostra a mensagem de erro capturada
    return vagas

def main():
    #main nome da função "Por convenção, main() é usado como a função principal de um programa, 
    # onde tudo começa.Ela é o “cérebro” ou o “ponto de entrada” do código."
    todas_vagas = [] #criando uma lista vazia chamada todas_vagas.
    #Por que uma lista vazia?Porque ela vai ser usada para acumular todas as vagas 
    # encontradas em vários sites.
    #Exemplo:Você chama a função de scraping para 5 sites diferentes.
    #Cada chamada retorna algumas vagas.Você coloca todas dentro de todas_vagas.

    for site in SITES:
        #O for vai percorrer cada site dessa lista um por um;Em cada repetição:
        #a variável site terá o valor de uma URL da lista.
        print(f" Buscando em {site}...")
        #Imprime na tela qual site está sendo processado naquele momento.
        #{site} é substituído pela URL atual.
        vagas = buscar_vagas(site)
        #chama a função que faz o scraping do site
        todas_vagas.extend(vagas)
        #Essa é uma parte MUITO importante.
        #todas_vagas é sua lista principal (geral).
        #.extend(vagas) adiciona todos os elementos da lista vagas dentro de todas_vagas
    
    # Converter para DataFrame
    df = pd.DataFrame(todas_vagas)
    #pd é a forma abreviada de chamar a biblioteca pandas, normalmente importada assim:
    #DataFrame é a estrutura de tabela do pandas — como uma folha do Excel:
    #É a estrutura mais poderosa do pandas para trabalhar com dados
    if df.empty:
        #O if verifica: “O DataFrame está vazio?”
        #Se estiver, executa o bloco de código abaixo.
        print(" Nenhuma vaga encontrada com as palavras-chave.")
        return
        #return encerra a função imediatamente

    # Remover duplicadas
    df = df.drop_duplicates(subset=['titulo', 'link'])
    #drop_duplicates é um método do pandas que remove linhas duplicadas de um DataFrame.
    #Por padrão, ele compara todas as colunas, mas você pode especificar quais colunas considerar.
    #Retorna um novo DataFrame sem as duplicatas.
    
    # Nome do ficheiro com a data
    nome_ficheiro = f"vagas_{datetime.now().strftime('%Y%m%d')}.csv"
    #O f antes das aspas indica uma f-string, ou seja, uma string formatada.
    #Permite colocar expressões Python dentro de { } e elas serão avaliadas automaticamente.
    #datetime.now() datetime vem da biblioteca datetime do Python (from datetime import datetime).
    #datetime.now() retorna a data e hora atuais, 
    #.strftime() transforma um objeto datetime em string formatada.
    #'%Y%m%d' é o formato.
    #Substitui {datetime.now().strftime('%Y%m%d')} pela data atual, criando algo como:vagas_20251205.csv
    nome_ficheiro = f"vagas_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    # Salvar em CSV e Excel
    df.to_csv(nome_ficheiro, index=False, encoding='utf-8-sig')
    df.to_excel(nome_ficheiro, index=False)
    #df é um DataFrame do pandas (uma tabela com suas vagas).
    #.to_excel() é um método do pandas que salva o DataFrame em um arquivo Excel (.xlsx).
    #Ou seja, transforma a tabela que você tem em um arquivo que pode ser aberto no Excel.
    #nome_ficheiro É a variável que contém o nome do arquivo, criada
    #index=False:
        #Por padrão, o pandas adiciona uma coluna extra chamada “index” com números de 0 até N-1.
        #index=False impede que essa coluna seja salva, deixando apenas as suas 
        #colunas reais (titulo, link, origem).
    print(f" Ficheiro gerado: {nome_ficheiro}")
    #Informa ao usuário que o arquivo Excel foi criado com sucesso.
    #Mostra exatamente o nome do arquivo, incluindo a data, para que ele saiba onde encontrar o arquivo.
    print(df.head(10))# amostra das vagas encontradas
    # Metodo Excel
    #from datetime import datetime
    #nome_ficheiro = f"vagas_{datetime.now().strftime('%Y%m%d')}.xlsx"
    #df.to_excel(nome_ficheiro, index=False)
    #print(f"Ficheiro gerado: {nome_ficheiro}")
    #print(df.head(10))
if __name__ == "__main__":
    #__name__ é uma variável especial do Python que indica o nome do módulo atual.
    #Quando você executa o script diretamente, __name__ vale "__main__".
    #Quando você importa o script de outro arquivo, __name__ vale o nome do arquivo (módulo).
    #Portanto, essa linha significa:
    #“Se este arquivo está sendo executado diretamente, então execute o bloco a seguir.”
    #Isso impede que o código rode automaticamente quando você apenas importar funções 
    #desse arquivo em outro script.
    main()
    #Chama a função main() que você definiu anteriormente.
    #É o ponto de entrada do programa, onde todo o processo começa:
    #Percorre os sites
    #Coleta vagas
    #Filtra por keywords
    #Remove duplicados
    #Salva no Excel
    #Imprime mensagens de status

#adicional:[{}] Lista com um dicionário vazio {}dicionário vazio, sem nenhuma chave ou valor.
#O que é uma string formatada?
    #Uma string formatada é uma string (texto) que pode conter variáveis ou expressões dentro dela, 
    #Que serão avaliadas e substituídas pelo seu valor quando a string for usada.