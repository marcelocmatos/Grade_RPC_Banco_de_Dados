from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Programacao
from datetime import datetime, timedelta

class Grade():
    def insere_dados_grade(self, str_date, requisicao):
        engine = create_engine('sqlite:///db/programacao.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        requisicao = requisicao
        str_date=str_date
        
        b=0
        session.query(Programacao).delete()
        for i in requisicao:
            utf = float(requisicao[b]['custom_info']['BaseUTCOffset'][2:3])
            delta = timedelta(hours=utf)
            programa = requisicao[b]['title']
            hora_inicio = datetime.strftime((datetime.strptime((str(requisicao[b]['human_start_time'])[:5]), '%H:%M')-delta), '%H:%M')
            hora_fim = datetime.strftime((datetime.strptime((str(requisicao[b]['human_end_time'])[:5]), '%H:%M')-delta), '%H:%M')
            sinopse = requisicao[b]['custom_info']['Resumos']['Sinopse']
            classificacao = requisicao[b]['custom_info']['Classificacao']['Idade']
            genero = requisicao[b]['custom_info']['Genero']['Descricao']
            programacao = Programacao(
                data = str_date,
                programa = programa,
                sinopse = sinopse,
                hora_inicio = hora_inicio,
                hora_fim = hora_fim,
                classificacao = classificacao,
                genero = genero,
            )
            session.add(programacao)
            b += 1
        session.commit()