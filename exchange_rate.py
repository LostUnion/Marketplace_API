import requests
from decouple import Config, RepositoryIni

config = Config(RepositoryIni('config.ini'))
url = config('URL_CRB', cast=str)


res = requests.get(url=url)
data = res.json()
valute = data['Valute']

rub = 1

# Парсинг данных о валютах
for key, value in valute.items():
    if key in ("USD"):
        summ = rub / value['Value']
        print(f'{summ:.2f}')