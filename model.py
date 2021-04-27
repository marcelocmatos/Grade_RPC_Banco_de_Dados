from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///db/programacao.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Programacao(Base):
    __tablename__ = 'programacao'

    id = Column(Integer, primary_key=True)
    data = Column(String)
    programa = Column(String)
    sinopse = Column(Text)
    hora_inicio = Column(String)
    hora_fim = Column(String)
    classificacao = Column(String)
    genero = Column(String)

Base.metadata.create_all(engine)