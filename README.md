# 🤖 Robô de Vagas — Web Scraper de Oportunidades de Emprego (Moçambique)

Script em Python que percorre automaticamente sites de emprego moçambicanos, filtra vagas por palavras-chave relevantes (Monitoria, Avaliação, Análise de Dados, Gestão de Dados, etc.), remove duplicados e exporta os resultados para Excel/CSV com data automática no nome do ficheiro.

## Como funciona

1. Faz pedidos HTTP a uma lista de 15 sites de emprego (LinkedIn, Vaga.co.mz, UN Jobs, ImpactPool, entre outros).
2. Usa **BeautifulSoup** para analisar o HTML e extrair todos os links de cada página.
3. Filtra os links cujo texto contém alguma das palavras-chave definidas.
4. Organiza os resultados num **DataFrame do pandas**, remove duplicados e exporta para `.xlsx`/`.csv`.

## Tecnologias

- Python
- `requests` — pedidos HTTP
- `BeautifulSoup4` — parsing de HTML
- `pandas` — organização e exportação de dados

## Como executar

```bash
pip install requests beautifulsoup4 pandas openpyxl
python robo_vagas.py
```

O script gera um ficheiro `vagas_AAAAMMDD.xlsx` com o título, link e site de origem de cada vaga encontrada.

## Possíveis melhorias futuras

- Adicionar mais sites à lista `SITES`
- Paginação automática para sites com múltiplas páginas de resultados
- Agendamento automático (ex.: execução diária via cron) com notificação por e-mail
