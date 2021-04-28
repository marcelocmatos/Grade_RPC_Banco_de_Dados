import requests, json
from datetime import datetime, timedelta
import pandas as pd

url = 'https://epg-api.video.globo.com/programmes/1337?date={}'
str_date_atual = datetime.today()
data_correta = datetime.strftime(str_date_atual, '%Y-%m-%d')
requisicao = requests.get(url.format(data_correta)).json()['programme']['entries']
programacao = []


b = 0
for i in requisicao:
    programa = requisicao[b]['title']   
    utf = float(requisicao[b]['custom_info']['BaseUTCOffset'][2:3])
    delta = timedelta(hours=utf)
    hora_inicio = str(requisicao[b]['human_start_time'])[:5]
    hora_inicio = datetime.strptime(hora_inicio, '%H:%M')-delta
    hora_inicio = datetime.strftime(hora_inicio, '%H:%M')

    hora_fim = str(requisicao[b]['human_end_time'])[:5]
    hora_fim = datetime.strptime(hora_fim, '%H:%M')-delta
    hora_fim = datetime.strftime(hora_fim, '%H:%M')

    sinopse = requisicao[b]['custom_info']['Resumos']['Sinopse']
    classificacao = requisicao[b]['custom_info']['Classificacao']['Idade']
    genero = requisicao[b]['custom_info']['Genero']['Descricao']
    programacao_diaria = {
                'Programa': programa,
                'Sinopse': sinopse,
                'Início': hora_inicio,
                'Fim': hora_fim,
                'Classificação': classificacao,
                'Gênero': genero,
                            }
    b += 1
    programacao.append(programacao_diaria)

    context = json.dumps(programacao, ensure_ascii=False)
    df = pd.read_json(context)
print(df)


# print(f'Hora de fim: {hora_fim}')