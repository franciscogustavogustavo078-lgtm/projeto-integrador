from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'nexus'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'

db = SQLAlchemy(app)


class Contrato(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    numero = db.Column(db.String(50))

    tipo = db.Column(db.String(100))

    parte = db.Column(db.String(100))

    descricao = db.Column(db.String(300))

    inicio = db.Column(db.String(50))

    fim = db.Column(db.String(50))

    valor = db.Column(db.String(50))

    status = db.Column(db.String(50))


class Parte(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100))

    tipo = db.Column(db.String(100))

    documento = db.Column(db.String(100))

    contato = db.Column(db.String(100))

    email = db.Column(db.String(100))

    telefone = db.Column(db.String(100))

    endereco = db.Column(db.String(300))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        usuario = request.form['usuario']

        senha = request.form['senha']

        if usuario == 'admin' and senha == '123':

            session['usuario'] = usuario

            return redirect('/dashboard')

    return render_template('login.html')


@app.route('/logout')
def logout():

    session.pop('usuario', None)

    return redirect('/login')


@app.route('/dashboard')
def dashboard():

    if 'usuario' not in session:

        return redirect('/login')

    contratos = Contrato.query.all()

    total = Contrato.query.count()

    ativos = Contrato.query.filter_by(status='Ativo').count()

    vencidos = Contrato.query.filter_by(status='Vencido').count()

    rescindidos = Contrato.query.filter_by(status='Rescindido').count()

    return render_template(

        'index.html',

        contratos=contratos,

        total=total,

        ativos=ativos,

        vencidos=vencidos,

        rescindidos=rescindidos
    )


@app.route('/')
def home():

    if 'usuario' not in session:

        return redirect('/login')

    contratos = Contrato.query.all()

    return render_template(

        'contratos.html',

        contratos=contratos
    )


@app.route('/cadastro')
def cadastro():

    if 'usuario' not in session:

        return redirect('/login')

    return render_template(

        'cadcontratos.html'
    )


@app.route('/salvar', methods=['POST'])
def salvar():

    novo = Contrato(

        numero=request.form['numero'],

        tipo=request.form['tipo'],

        parte=request.form['parte'],

        descricao=request.form['descricao'],

        inicio=request.form['inicio'],

        fim=request.form['fim'],

        valor=request.form['valor'],

        status=request.form['status']
    )

    db.session.add(novo)

    db.session.commit()

    return redirect('/')


@app.route('/vercontrato/<int:id>')
def vercontrato(id):

    if 'usuario' not in session:

        return redirect('/login')

    contrato = Contrato.query.get(id)

    return render_template(

        'vercontrato.html',

        contrato=contrato
    )


@app.route('/editar/<int:id>')
def editar(id):

    if 'usuario' not in session:

        return redirect('/login')

    contrato = Contrato.query.get(id)

    return render_template(

        'editarcontrato.html',

        contrato=contrato
    )


@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):

    contrato = Contrato.query.get(id)

    contrato.numero = request.form['numero']

    contrato.tipo = request.form['tipo']

    contrato.parte = request.form['parte']

    contrato.descricao = request.form['descricao']

    contrato.inicio = request.form['inicio']

    contrato.fim = request.form['fim']

    contrato.valor = request.form['valor']

    contrato.status = request.form['status']

    db.session.commit()

    return redirect('/')


@app.route('/excluir/<int:id>')
def excluir(id):

    contrato = Contrato.query.get(id)

    db.session.delete(contrato)

    db.session.commit()

    return redirect('/')


@app.route('/partes')
def partes():

    if 'usuario' not in session:

        return redirect('/login')

    partes = Parte.query.all()

    return render_template(

        '/partes',

        partes=partes
    )


@app.route('/cadpartes')
def cadpartes():

    if 'usuario' not in session:

        return redirect('/login')

    return render_template(

        'cad/partes'
    )


@app.route('/salvarparte', methods=['POST'])
def salvarparte():

    nova = Parte(

        nome=request.form['nome'],

        tipo=request.form['tipo'],

        documento=request.form['documento'],

        contato=request.form['contato'],

        email=request.form['email'],

        telefone=request.form['telefone'],

        endereco=request.form['endereco']
    )

    db.session.add(nova)

    db.session.commit()

    return redirect('/partes')


@app.route('/verparte/<int:id>')
def verparte(id):

    if 'usuario' not in session:

        return redirect('/login')

    parte = Parte.query.get(id)

    return render_template(

        'verparte.html',

        parte=parte
    )


@app.route('/editarparte/<int:id>')
def editarparte(id):

    if 'usuario' not in session:

        return redirect('/login')

    parte = Parte.query.get(id)

    return render_template(

        'editarparte.html',

        parte=parte
    )


@app.route('/atualizarparte/<int:id>', methods=['POST'])
def atualizarparte(id):

    parte = Parte.query.get(id)

    parte.nome = request.form['nome']

    parte.tipo = request.form['tipo']

    parte.documento = request.form['documento']

    parte.contato = request.form['contato']

    parte.email = request.form['email']

    parte.telefone = request.form['telefone']

    parte.endereco = request.form['endereco']

    db.session.commit()

    return redirect('/partes')


@app.route('/excluirparte/<int:id>')
def excluirparte(id):

    parte = Parte.query.get(id)

    db.session.delete(parte)

    db.session.commit()

    return redirect('/partes')


@app.route('/relatorios')
def relatorios():

    if 'usuario' not in session:

        return redirect('/login')

    contratos = Contrato.query.all()

    total = Contrato.query.count()

    ativos = Contrato.query.filter_by(status='Ativo').count()

    valor_total = 0

    for contrato in contratos:

        try:

            valor_total += float(contrato.valor)

        except:

            pass

    return render_template(

        'relatorios.html',

        contratos=contratos,

        total=total,

        ativos=ativos,

        valor_total=valor_total
    )


@app.route('/config')
def config():

    if 'usuario' not in session:

        return redirect('/login')

    return render_template(

        'config.html'
    )


if __name__ == '__main__':

    with app.app_context():

        db.create_all()

    app.run(debug=True, port=5000)