from flask import render_template, redirect, url_for, flash, send_file, request, session, Response
from flask import current_app as app
from app import db
from app.forms import ColaboradorForm, ProcessoForm, DeletarTodosForm, LoginForm
from werkzeug.utils import secure_filename
import os, csv, io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from openpyxl import Workbook
from flask import send_file
from io import BytesIO
from app.models import Colaborador, Processo, DetalhesProcesso, SenhaUsuario
from reportlab.lib.utils import ImageReader, simpleSplit
from datetime import datetime, timedelta


@app.route('/')
def home_redirect():
    return redirect(url_for('inicio'))

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/index')
def index():
    if not session.get('logado'):
        return redirect(url_for('login'))

    page = request.args.get('page', 1, type=int)
    processos = Processo.query.order_by(Processo.data_analise.desc()).paginate(page=page, per_page=10)

    return render_template('index.html', processos=processos, deletar_form=DeletarTodosForm())



@app.route('/colaborador/novo', methods=['GET', 'POST'])
def novo_colaborador():
    form = ColaboradorForm()
    if form.validate_on_submit():
        colaborador = Colaborador(nome=form.nome.data, email=form.email.data)
        db.session.add(colaborador)
        db.session.commit()
        flash('Colaborador adicionado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('novo_colaborador.html', form=form)


@app.route('/processo/novo', methods=['GET', 'POST'])
def novo_processo():
    form = ProcessoForm()
    form.colaborador.choices = [(c.id, c.nome) for c in Colaborador.query.all()]

    if form.validate_on_submit():
        filename = None
        if form.imagem.data:
            filename = secure_filename(form.imagem.data.filename)
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.imagem.data.save(caminho)

        # Corrige a hora com fuso de Brasília
        brasil_time = datetime.utcnow() - timedelta(hours=3)

        processo = Processo(
            colaborador_id=form.colaborador.data,
            descricao=form.descricao.data,
            status=form.status.data,
            observacoes=form.observacoes.data,
            imagem=filename,
            data_analise=brasil_time  # Agora é salvo corretamente
        )
        db.session.add(processo)
        db.session.commit()

        # ✅ Adiciona os detalhes extras agora
        detalhes = DetalhesProcesso(
            processo_id=processo.id,
            coordenacao=form.coordenacao.data,
            lideranca=form.lideranca.data,
            data_inspecao=form.data_inspecao.data,
            inspetor=form.inspetor.data,
            cpf_cnpj=form.cpf_cnpj.data,
            coop=form.coop.data,
            tipo=form.tipo.data,
            data_execucao=form.data_execucao.data,
            interno_externo=form.interno_externo.data,
            tipo_autorizacao=form.tipo_autorizacao.data,
            tipo_erro=form.tipo_erro.data,
            gravidade=form.gravidade.data,
            desvio_atencao=form.desvio_atencao.data,
            reversao=form.reversao.data,
            fluxos=form.fluxos.data,
            solicitante=form.solicitante.data
        )
        db.session.add(detalhes)
        db.session.commit()

        flash('Processo registrado com sucesso!', 'success')
        return redirect(url_for('index'))

    return render_template('novo_processo.html', form=form)


from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from datetime import datetime
from io import BytesIO

@app.route('/exportar-xlsx')
def exportar_xlsx():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

    if not data_inicio or not data_fim:
        flash('Informe o intervalo de datas para exportar.', 'warning')
        return redirect(url_for('index'))

    processos = Processo.query.filter(
        Processo.data_analise.between(data_inicio, data_fim)
    ).order_by(Processo.data_analise.asc()).all()

    wb = Workbook()
    ws = wb.active

    # ✅ Título seguro: sem risco de exceder 31 caracteres
    titulo = f"{data_inicio}_a_{data_fim}"
    ws.title = titulo[:31]

    # Estilos
    header_font = Font(bold=True, color="000000")
    header_fill = PatternFill("solid", fgColor="D9D9D9")
    alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    border = Border(left=Side(style='thin'), right=Side(style='thin'),
                    top=Side(style='thin'), bottom=Side(style='thin'))

    # Cabeçalhos
    cabecalhos = [
        "COORDENACAO", "LIDERANCA", "DATA DA INSPECAO", "INSPETOR", "CPF/CNPJ", "COOP", "TIPO",
        "DATA DE EXECUCAO", "INTERNO OU EXTERNO", "TIPO DE AUTORIZACAO", "COLABORADOR",
        "TIPO DE ERRO", "DESCRICAO", "GRAVIDADE", "DESVIO DE ATENCAO", "REVERSAO",
        "QUAIS FLUXOS", "OBSERVACOES", "SOLICITANTE"
    ]
    ws.append(cabecalhos)

    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = alignment
        cell.border = border

    for p in processos:
        d = p.detalhes
        linha = [
            d.coordenacao if d else '',
            d.lideranca if d else '',
            d.data_inspecao.strftime('%d/%m/%Y') if d and d.data_inspecao else '',
            d.inspetor if d else '',
            d.cpf_cnpj if d else '',
            d.coop if d else '',
            d.tipo if d else '',
            d.data_execucao.strftime('%d/%m/%Y') if d and d.data_execucao else '',
            d.interno_externo if d else '',
            d.tipo_autorizacao if d else '',
            p.colaborador.nome,
            d.tipo_erro if d else '',
            p.descricao,
            d.gravidade if d else '',
            d.desvio_atencao if d else '',
            d.reversao if d else '',
            d.fluxos if d else '',
            p.observacoes or '',
            d.solicitante if d else ''
        ]
        ws.append([str(c) if c is not None else '' for c in linha])  # evita erro com tipos inválidos

    # Estilização das células
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(cabecalhos)):
        for cell in row:
            cell.alignment = alignment
            cell.border = border

    # Ajustar largura das colunas
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = max_length + 2

    # Congela a primeira linha
    ws.freeze_panes = 'A2'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name=f'processos_{data_inicio}_a_{data_fim}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@app.route('/deletar-todos', methods=['POST'])
def deletar_todos():
    form = DeletarTodosForm()
    if form.validate_on_submit():
        db.session.query(Processo).delete()
        db.session.commit()
        flash('Todos os registros de processo foram apagados.', 'warning')
    return redirect(url_for('index'))


@app.route('/painel', methods=['GET'])
def painel():
    colaboradores = Colaborador.query.all()

    colaborador_id = request.args.get('colaborador', type=int)
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    status = request.args.get('status')
    palavra = request.args.get('palavra')
    page = request.args.get('page', 1, type=int)

    query = Processo.query

    if colaborador_id:
        query = query.filter_by(colaborador_id=colaborador_id)
    
    if status:
        query = query.filter_by(status=status)
    
    if palavra:
        query = query.filter(Processo.descricao.ilike(f"%{palavra}%"))

    if data_inicio:
        query = query.filter(Processo.data_analise >= data_inicio)
    if data_fim:
        query = query.filter(Processo.data_analise <= data_fim)

    total = query.count()
    conformes = query.filter_by(status='Conforme').count()
    desvios = query.filter_by(status='Desvio').count()

    processos = query.order_by(Processo.data_analise.desc()).paginate(page=page, per_page=10)

    return render_template('painel.html',
                           colaboradores=colaboradores,
                           colaborador_id=colaborador_id,
                           total=total,
                           conformes=conformes,
                           desvios=desvios,
                           processos=processos)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data

        senha_registrada = SenhaUsuario.query.filter_by(email=email).first()

        if senha_registrada:
            # Se já existe senha trocada, só aceita com hash
            if senha_registrada.verificar_senha(senha):
                session['logado'] = True
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Senha incorreta.', 'danger')
        else:
            # Só aceita senha padrão se ainda não foi trocada
            colaborador = Colaborador.query.filter_by(email=email).first()
            if colaborador and senha == '123456':
                session['logado'] = True
                flash('Login com senha padrão.', 'warning')
                return redirect(url_for('index'))
            else:
                flash('Senha incorreta ou colaborador inexistente.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('logado', None)
    flash('Sessão encerrada com sucesso.', 'info')
    return redirect(url_for('login'))


@app.route('/processo/<int:id>/pdf')
def gerar_pdf(id):
    processo = Processo.query.get_or_404(id)
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    y = 800
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "PARECER DE INSPEÇÃO DE PROCESSO")
    y -= 30

    pdf.setFont("Helvetica", 12)

    # ✅ Usa data_execucao se existir, senão usa data_analise
    data_execucao = (
        processo.detalhes.data_execucao.strftime('%d/%m/%Y')
        if processo.detalhes and processo.detalhes.data_execucao
        else processo.data_analise.strftime('%d/%m/%Y %H:%M')
    )
    pdf.drawString(50, y, f"Data: {data_execucao}")
    y -= 20

    pdf.drawString(50, y, f"Colaborador: {processo.colaborador.nome}")
    y -= 20
    pdf.drawString(50, y, f"Status: {processo.status}")
    y -= 20
    pdf.drawString(50, y, f"Descrição: {processo.descricao}")
    y -= 40

    if processo.observacoes:
        pdf.drawString(50, y, "Observações:")
        y -= 20
        linhas_obs = simpleSplit(processo.observacoes, "Helvetica", 12, 500)
        text = pdf.beginText(50, y)
        text.setFont("Helvetica", 12)
        for linha in linhas_obs:
            text.textLine(linha)
        pdf.drawText(text)
        y = text.getY() - 20

    if processo.status == 'Desvio':
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "PARECER:")
        y -= 20
        pdf.setFont("Helvetica", 12)
        parecer = (
            "Conforme análise realizada, identificamos um ponto de atenção neste processo. "
            "Recomenda-se avaliação complementar e plano de ação conforme aplicável."
        )
        linhas_parecer = simpleSplit(parecer, "Helvetica", 12, 500)
        text = pdf.beginText(50, y)
        for linha in linhas_parecer:
            text.textLine(linha)
        pdf.drawText(text)
        y = text.getY() - 20

    if processo.imagem:
        imagem_path = os.path.join(app.root_path, 'static', 'uploads', processo.imagem)
        if os.path.exists(imagem_path):
            try:
                pdf.drawImage(ImageReader(imagem_path), 130, y - 200, width=300, height=200)
            except Exception:
                pass

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'processo_{id}.pdf', mimetype='application/pdf')


from app.forms import TrocarSenhaForm
from app.models import SenhaUsuario


@app.route('/trocar-senha', methods=['GET', 'POST'])
def trocar_senha():
    form = TrocarSenhaForm()
    if form.validate_on_submit():
        email = form.email.data
        senha_atual = form.senha_atual.data
        nova_senha = form.nova_senha.data

        senha_registrada = SenhaUsuario.query.filter_by(email=email).first()

        if senha_registrada:
            # Se existe hash, validar senha atual
            if not senha_registrada.verificar_senha(senha_atual):
                flash('Senha atual incorreta.', 'danger')
                return render_template('trocar_senha.html', form=form)
        else:
            # Se ainda não existe hash, só aceita padrão '123456'
            if senha_atual != '123456':
                flash('Senha atual incorreta.', 'danger')
                return render_template('trocar_senha.html', form=form)

            # Cria registro novo na tabela
            senha_registrada = SenhaUsuario(email=email)
            db.session.add(senha_registrada)

        # Salva nova senha
        senha_registrada.set_senha(nova_senha)
        db.session.commit()
        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('trocar_senha.html', form=form)

#====

@app.route('/meu_perfil')
def meu_perfil():
    hoje = datetime.today()
    inicio_mes_atual = hoje.replace(day=1)
    inicio_mes_anterior = (inicio_mes_atual - timedelta(days=1)).replace(day=1)
    fim_mes_anterior = inicio_mes_atual - timedelta(days=1)

    processos_atual = Processo.query.filter(Processo.data_analise >= inicio_mes_atual).all()
    processos_anterior = Processo.query.filter(Processo.data_analise.between(inicio_mes_anterior, fim_mes_anterior)).all()

    total_mes_atual = len(processos_atual)
    conformes_mes_atual = len([p for p in processos_atual if p.status == 'Conforme'])
    desvios_mes_atual = len([p for p in processos_atual if p.status == 'Desvio'])

    total_mes_anterior = len(processos_anterior)
    conformes_mes_anterior = len([p for p in processos_anterior if p.status == 'Conforme'])
    desvios_mes_anterior = len([p for p in processos_anterior if p.status == 'Desvio'])

    diff_total = total_mes_atual - total_mes_anterior
    diff_conformes = conformes_mes_atual - conformes_mes_anterior
    diff_desvios = desvios_mes_atual - desvios_mes_anterior

    return render_template('meu_perfil.html',
                           total_mes_atual=total_mes_atual,
                           conformes_mes_atual=conformes_mes_atual,
                           desvios_mes_atual=desvios_mes_atual,
                           diff_total=diff_total,
                           diff_conformes=diff_conformes,
                           diff_desvios=diff_desvios)
