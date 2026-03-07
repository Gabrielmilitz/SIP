from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


#Classes

class Colaborador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    processos = db.relationship('Processo', backref='colaborador', lazy=True)


class Processo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'), nullable=False)
    data_analise = db.Column(db.DateTime, nullable=False) 
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    observacoes = db.Column(db.Text)
    imagem = db.Column(db.String(200))
    detalhes = db.relationship('DetalhesProcesso', backref='processo', uselist=False)


class DetalhesProcesso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    processo_id = db.Column(db.Integer, db.ForeignKey('processo.id'), nullable=False)

    coordenacao = db.Column(db.String(120)) 
    lideranca = db.Column(db.String(120)) 
    data_inspecao = db.Column(db.Date) 
    inspetor = db.Column(db.String(120)) 
    cpf_cnpj = db.Column(db.String(20)) 
    coop = db.Column(db.String(120)) 
    tipo = db.Column(db.String(120)) 
    data_execucao = db.Column(db.Date) 
    interno_externo = db.Column(db.String(50))
    tipo_autorizacao = db.Column(db.String(120))
    tipo_erro = db.Column(db.String(120))
    gravidade = db.Column(db.String(120))
    desvio_atencao = db.Column(db.String(10))
    reversao = db.Column(db.String(10))
    fluxos = db.Column(db.String(255))
    solicitante = db.Column(db.String(120))


class SenhaUsuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)