from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, DateField
from wtforms.validators import DataRequired, Email
from wtforms.validators import Optional

class ColaboradorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Adicionar Colaborador')


class ProcessoForm(FlaskForm):

    colaborador = SelectField('Colaborador', coerce=int, validators=[DataRequired()])

    descricao = TextAreaField('Descrição do erro', validators=[Optional()])

    status = SelectField(
        'Status',
        choices=[
            ('Conforme', 'Conforme'),
            ('Desvio', 'Desvio')
        ],
        validators=[DataRequired()]
    )

    observacoes = TextAreaField('Procedimento correto')

    imagem = FileField(
    'Imagens',
    render_kw={"multiple": True},
    validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens são permitidas')]
)

    coordenacao = SelectField(
        'Coordenação',
        choices=[
            ('', 'Selecione'),
            ('larissa.gregoria', 'larissa.gregoria'),
            ('eluane.machado', 'eluane.machado'),
            ('lilian.flores', 'lilian.flores')
        ]
    )

    lideranca = SelectField(
        'Liderança',
        choices=[
            ('', 'Selecione'),
            ('gabriel.militz', 'gabriel.militz'),
            ('tacio.pozzati', 'tacio.pozzati'),
            ('diogo.machado', 'diogo.machado'),
            ('tais.melo', 'tais.melo'),
            ('ilto.rodrigues', 'ilto.rodrigues'),
            ('nathalia.moraes', 'nathalia.moraes'),
            ('mauricio.konig', 'mauricio.konig'),
            ('kerolin.vargas', 'Kerolin.Vargas'),
            ('gabriela.doring', 'gabriela.doring')
        ]
    )

    data_inspecao = DateField('Data da Inspeção', format='%Y-%m-%d')

    inspetor = SelectField(
        'Inspetor',
        choices=[
            ('', 'Selecione'),
            ('andressa.castro', 'andressa.castro'),
            ('andressa.belmiro', 'andressa.belmiro'),
            ('andrieli.bock', 'andrieli.bock'),
            ('emilie.vollmann', 'emilie.vollmann'),
            ('fabiana.soares', 'fabiana.soares'),
            ('erika.figueira', 'erika.figueira'),
            ('gabrielle.pippi', 'gabrielle.pippi'),
            ('guilherme.losekann', 'guilherme.losekann'),
            ('marivane.fernandes', 'marivane.fernandes'),
            ('monica.laucksen', 'monica.laucksen')
        ]
    )

    cpf_cnpj = StringField('CPF/CNPJ')
    coop = StringField('Coop')

    tipo = SelectField(
        'Tipo',
        choices=[
            ('Cooperativa', 'Cooperativa'),
            ('Autorizar', 'Autorizar'),
            ('Autoatendimento', 'Autoatendimento')
        ]
    )

    data_execucao = DateField('Data de Execução', format='%Y-%m-%d')

    interno_externo = SelectField(
        'Interno ou Externo',
        choices=[
            ('Interno', 'Interno'),
            ('Externo', 'Externo'),
            ('Chamado', 'Chamado')
        ]
    )

    tipo_autorizacao = SelectField(
        'Tipo de Autorização',
        choices=[
            ('BEM_NOVO', 'BEM_NOVO'),
            ('CERTIDAO', 'CERTIDAO'),
            ('ENDERECO', 'ENDERECO'),
            ('FONTE_RENDA', 'FONTE_RENDA'),
            ('PESSOA', 'PESSOA'),
            ('PRODUTIVIDADE', 'PRODUTIVIDADE'),
            ('PRODUTOR', 'PRODUTOR'),
            ('RELACIONAMENTO', 'RELACIONAMENTO'),
            ('TRIBUTACAO', 'TRIBUTACAO')
        ]
    )

    tipo_erro = SelectField(
        'Tipo de Erro',
        choices=[
            ('Sem erro', 'Sem erro'),
            ('Aprovacao Incorreta', 'Aprovação Incorreta'),
            ('Preenchimento Incorreto', 'Preenchimento Incorreto'),
            ('Reprovacao Incorreta', 'Reprovação Incorreta'),
            ('Reprovacao Incompleta', 'Reprovação Incompleta'),
            ('Documento Invalido', 'Documento Inválido')
        ]
    )

    gravidade = SelectField(
        'Gravidade',
        choices=[
            ('Sem Erro', 'Sem Erro'),
            ('Grave', 'Grave'),
            ('Gravissimo', 'Gravíssimo')
        ]
    )

    desvio_atencao = SelectField(
        'Desvio de Atenção',
        choices=[('Sim', 'Sim'), ('Nao', 'Não')]
    )

    reversao = SelectField(
        'Reversão',
        choices=[
            ('Grave', 'Grave'),
            ('Gravissimo', 'Gravíssimo'),
            ('Nao', 'Não')
        ]
    )

    fluxos = StringField('Quais Fluxos')
    solicitante = StringField('Solicitante')

    submit = SubmitField('Registrar Processo')


class DeletarTodosForm(FlaskForm):
    submit = SubmitField('Deletar Todos os Registros')

class DeletarPorColaboradorForm(FlaskForm):
    colaborador = SelectField(
        'Selecionar Colaborador',
        coerce=int,
        validators=[DataRequired()]
    )
    submit = SubmitField('Deletar Processos do Colaborador')


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')


class TrocarSenhaForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha_atual = PasswordField('Senha Atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova Senha', validators=[DataRequired()])
    submit = SubmitField('Trocar Senha')


class PerfilForm(FlaskForm):
    foto = FileField('Selecionar Foto', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens.')])
    submit = SubmitField('Salvar')