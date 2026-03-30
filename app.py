from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- MODEL BAZY DANYCH ---
class Transaction(db.Model):
    """Model bazy danych reprezentujący pojedynczą transakcję (przychód lub wydatek)."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)


with app.app_context():
    db.create_all()


# --- WIDOKI (ROUTING) ---
@app.route('/')
def index():
    """Pobiera transakcje z bazy, oblicza saldo i renderuje stronę główną."""
    transactions = Transaction.query.all()
    # Obliczanie salda: dodajemy przychody, odejmujemy wydatki
    balance = sum(t.amount if t.type == 'income' else -t.amount for t in transactions)
    return render_template('index.html', transactions=transactions, balance=balance)


@app.route('/add', methods=['POST'])
def add():
    """Pobiera dane z formularza, tworzy nowy obiekt Transaction i zapisuje w bazie."""
    title = request.form.get('title')
    amount = float(request.form.get('amount'))
    t_type = request.form.get('type')

    new_transaction = Transaction(title=title, amount=amount, type=t_type)
    db.session.add(new_transaction)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    """Usuwa transakcję z bazy na podstawie podanego ID."""
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)