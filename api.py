from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
app = Flask(__name__)

load_dotenv()
usuario = os.getenv('DB_USER')
senha = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
porta = os.getenv('DB_PORT')
banco = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = (f'postgresql://{usuario}:{senha}@{host}:{porta}/{banco}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Aluno(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    cpf = db.Column(db.String(20))
    tipoPessoa = db.Column(db.CHAR(1))
    status = db.Column(db.CHAR(1))

class Professor(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    cpf = db.Column(db.String(20))
    tipoPessoa = db.Column(db.String(1))
    status = db.Column(db.CHAR(1))
    
CORS(app)

@app.get('/pessoa')
def getPessoa():
    with app.app_context():
        alunos = Aluno.query.limit(50).all()
        professores = Professor.query.limit(50).all()
        
        pessoas = []
        for aluno in alunos:
            pessoas.append({
                "id":aluno.id,
                "name":aluno.name,
                "cpf":aluno.cpf,
                "tipoPessoa":aluno.tipoPessoa,
                "status": aluno.status
            })
        for professor in professores:
            pessoas.append({
                "id": professor.id,
                "name":professor.name,
                "cpf":professor.cpf,
                "tipoPessoa":professor.tipoPessoa,
                "status": professor.status
        })
        return jsonify(pessoas)
        
@app.get('/total-pessoas')
def totalAtivos():
    with app.app_context():
        totalAlunos = Aluno.query.count()
        totalProfessores = Professor.query.count()
        totalAlunosAtivos = Aluno.query.filter_by(status='A').count()
        totalAlunosInativos = Aluno.query.filter_by(status='I').count()
        totalProfessoresAtivos = Professor.query.filter_by(status='A').count()
        totalProfessoresInativos = Professor.query.filter_by(status='I').count()
        cards = [{
            "id": 1,
            "name": 'Total Alunos',
            "total": totalAlunos   
        },
        {
            "id": 2,
            "name": 'Total Alunos Ativos',
            "total": totalAlunosAtivos       
        },
        {
            "id": 3,
            "name": 'Total Alunos Inativos',
            "total": totalAlunosInativos       
        },  
        {
            "id": 4,
            "name": 'Total Professores',
            "total": totalProfessores     
        },  
        {
            "id": 5,
            "name": 'Total Professores ativos',
            "total": totalProfessoresAtivos       
        },
        {
            "id": 6,
            "name": 'Total Professores inativos',
            "total": totalProfessoresInativos       
        },
        ]
        return jsonify(cards)
app.run(debug=True, host="0.0.0.0", port=5000)
