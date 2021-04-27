from flask import Flask, render_template, request, flash
from datetime import datetime
import requests, json
from grade import Grade
from model import Programacao
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SECRET_KEY'] = '01d47391683dc0465d17a607'
grade = Grade()
engine = create_engine('sqlite:///db/programacao.db')
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/', methods=['GET', 'POST'])
def index():
    url = 'https://epg-api.video.globo.com/programmes/1337?date={}'
    str_date = request.form.get('data')
    if str_date is None or str_date == '':
        str_date_atual = datetime.today()
        data_correta = datetime.strftime(str_date_atual, '%Y-%m-%d')
    else:
        data_correta = str_date
    if request.method == 'POST' or data_correta != '':
        try: 
            requisicao = requests.get(url.format(data_correta)).json()['programme']['entries'] 
        except json.JSONDecodeError:
            str_date_atual = datetime.today()
            data_correta = datetime.strftime(str_date_atual, '%Y-%m-%d')
            requisicao = requests.get(url.format(data_correta)).json()['programme']['entries']
            flash('Data escolhida está indisponível. Mostrando a grade de horários de hoje.', category='danger')
    grade.insere_dados_grade(data_correta, requisicao)
    programacao_diaria = session.query(Programacao).filter_by(data = data_correta).all()
    session.close()
    str_date_hoje = datetime.today()
    str_date_hoje = datetime.strftime(str_date_hoje, '%d/%m/%Y')
    str_date = datetime.strptime(data_correta, '%Y-%m-%d')
    str_date = datetime.strftime(str_date, '%d/%m/%Y')
    return render_template('index.html', dados=programacao_diaria, str_date=str_date, str_date_hoje=str_date_hoje)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/404")
def error_404():
    return render_template('404.html')

if __name__ == '__main__':
    app.run()