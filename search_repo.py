import requests

GITHUB_TOKEN = ""

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Parâmetros da busca: linguagem Java, mínimo 300 stars, não fork
query = "language:Java stars:>300 fork:false"
url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=100"
def buscar_repositorios():
    repositorios_validos = []
    page = 1

    while True:
        #Olho todas as páginas de pesquisa que encontrei
        print(f"🔎 Buscando página {page}...")
        response = requests.get(f"{url}&page={page}", headers=headers)
        if response.status_code != 200:
            print("Erro:", response.status_code, response.text)
            break

        dados = response.json()
        repositorios = dados.get("items", [])
        if not repositorios:
            break

        for repo in repositorios:
            repositorios_validos.append({
                "nome": repo["full_name"],
                "estrelas": repo["stargazers_count"],
                "linguagem": repo["language"],
                "url": repo["html_url"]
            })

        if 'next' not in response.links:
            break
        page += 1

    return repositorios_validos

repos = buscar_repositorios()

for r in repos[:10]:
    print(f"{r['nome']} - {r['estrelas']} stars - {r['linguagem']} - {r['url']}")
