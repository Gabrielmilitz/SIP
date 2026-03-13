from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, DateField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectField
class ColaboradorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Adicionar Colaborador')


class ProcessoForm(FlaskForm):
    colaborador = SelectField('Colaborador', coerce=int, validators=[DataRequired()])
    descricao = TextAreaField('Descrição do Processo', validators=[DataRequired()])
    status = SelectField(
        'Status',
        choices=[('Conforme', 'Conforme'), ('Desvio', 'Desvio')],
        validators=[DataRequired()]
    )
    observacoes = TextAreaField('Observações')
    imagem = FileField('Imagem', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens são permitidas')])

    # Novos campos para a tabela DetalhesProcesso
    coordenacao = StringField('Coordenação')
    lideranca = StringField('Liderança')
    data_inspecao = DateField('Data da Inspeção', format='%Y-%m-%d')
    inspetor = StringField('Inspetor')
    cpf_cnpj = StringField('CPF/CNPJ')
    coop = StringField('Coop')
    tipo = SelectField('Tipo', choices=[
    ('Cooperativa', 'Cooperativa'),
    ('Autorizar', 'Autorizar'),
    ('Autoatendimento', 'Autoatendimento')
])
    data_execucao = DateField('Data de Execução', format='%Y-%m-%d')
    interno_externo = SelectField('Interno ou Externo', choices=[('Interno', 'Interno'), ('Externo', 'Externo')])
    tipo_autorizacao = SelectField('Tipo de Autorização', choices=[
    ('BEM_NOVO', 'BEM_NOVO'),
    ('CERTIDAO', 'CERTIDAO'),
    ('ENDERECO', 'ENDERECO'),
    ('FONTE_RENDA', 'FONTE_RENDA'),
    ('PESSOA', 'PESSOA'),
    ('PRODUTIVIDADE', 'PRODUTIVIDADE'),
    ('PRODUTOR', 'PRODUTOR'),
    ('RELACIONAMENTO', 'RELACIONAMENTO'),
    ('TRIBUTACAO', 'TRIBUTACAO')])
    tipo_erro = SelectField('Tipo de Erro', choices=[
    ('Sem erro', 'Sem erro'),
    ('Aprovacao Incorreta', 'Aprovação Incorreta'),
    ('Preenchimento Incorreto', 'Preenchimento Incorreto'),
    ('Reprovacao Incorreta', 'Reprovação Incorreta'),
    ('Reprovacao Incompleta', 'Reprovação Incompleta'),
    ('Documento Invalido', 'Documento Inválido')
])
    gravidade = SelectField('Gravidade', choices=[
    ('Sem Erro', 'Sem Erro'),
    ('Grave', 'Grave'),
    ('Gravissimo', 'Gravíssimo')
])
    desvio_atencao = SelectField('Desvio de Atenção', choices=[('Sim', 'Sim'), ('Nao', 'Não')])
    reversao = SelectField('Reversão', choices=[
    ('Grave', 'Grave'),
    ('Gravissimo', 'Gravíssimo'),
    ('Nao', 'Não')
])
    fluxos = StringField('Quais Fluxos')
    solicitante = StringField('Solicitante')

    submit = SubmitField('Registrar Processo')


class DeletarTodosForm(FlaskForm):
    submit = SubmitField('🗑️ Deletar Todos os Registros')


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

# segurança = precisa melhorar muito
class TrocarSenhaForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha_atual = PasswordField('Senha Atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova Senha', validators=[DataRequired()])
    submit = SubmitField('Trocar Senha')



from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField

class PerfilForm(FlaskForm):
    foto = FileField('Selecionar Foto', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens.')])
    submit = SubmitField('Salvar')