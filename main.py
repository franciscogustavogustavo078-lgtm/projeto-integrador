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


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5000)