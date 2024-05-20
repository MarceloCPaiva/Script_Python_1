import pandas as pd
import requests
import config


def obter_emails_da_api(api_url, token, max_pages=10):
    emails = []
    headers = {'x-token-beeviral': token}
    page = 1
    total_pages_lidas = 0

    try:
        while page <= max_pages:
            print(f"Processando página {page}...")
            params = {'limit': 200, 'page': page}
            response = requests.get(api_url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                for result in data:
                    for item in result.get('Result', []):
                        email = item.get('EMAIL')
                        if email:
                            emails.append(email)

                total_records = data[0].get('Paging', {}).get('RECORDS') if data else 0
                total_pages_lidas += 1

                if len(emails) >= total_records:
                    break

                page += 1
            else:
                print(f"Erro ao obter dados da API (página {page}). Código de status: {response.status_code}")
                break

        print(f"Total de páginas lidas: {total_pages_lidas}")
        print(f"Total de emails obtidos da API: {len(emails)}")
        return emails
    except Exception as e:
        print(f"Erro ao obter dados da API (página {page}). Código de status: {response.status_code}")
        return emails



def verificar_emails_na_planilha(planilha_caminho, coluna_email_index):
    try:
        # Lê a planilha Excel
        df = pd.read_excel(planilha_caminho)

        # Extrai os emails da coluna especificada
        emails_planilha = df.iloc[:, coluna_email_index].dropna().tolist()
        total_emails_planilha = len(emails_planilha)

        print(f"Total de emails obtidos da planilha: {total_emails_planilha}")
        return emails_planilha
    except Exception as e:
        print(f"Erro ao verificar a planilha: {e}")
        return []


# Exemplo de uso
api_url = config.api_url
token = config.token
planilha_caminho = config.planilha_caminho
coluna_email_index = 0  # Coluna A

emails_api = obter_emails_da_api(api_url, token)
emails_planilha = verificar_emails_na_planilha(planilha_caminho, coluna_email_index)

# Comparar os emails
emails_em_comum = set(emails_api) & set(emails_planilha)
total_emails_comum = len(emails_em_comum)
print(f"Total de emails em comum: {total_emails_comum}\n")
print("Emails encontrados em comum:")
for email in emails_em_comum:
    print(email)
