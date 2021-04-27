from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Programacao

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
            programa = requisicao[b]['title']
            hora_inicio = str(requisicao[b]['human_start_time'])[:5]
            hora_fim = str(requisicao[b]['human_end_time'])[:5]
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