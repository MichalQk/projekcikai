import pytest
from app import app, db, Transaction


@pytest.fixture
def client():
    # Konfiguracja środowiska testowego: używamy bazy w pamięci RAM,
    # aby testy były izolowane i nie modyfikowały głównej bazy aplikacji.
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client

            # Sprzątanie po testach, aby każdy kolejny test startował z pustą bazą
            db.session.remove()
            db.drop_all()


def test_index_page_loads(client):
    # Weryfikacja, czy widok główny ładuje się bez błędów i zawiera poprawny tytuł
    response = client.get('/')
    assert response.status_code == 200
    assert b'SmartBudget' in response.data


def test_add_income(client):
    # Test endpointu dodawania transakcji - sprawdzamy, czy przychód zapisuje się w bazie
    client.post('/add', data=dict(title='Wypłata', amount='4000', type='income'))
    with app.app_context():
        assert Transaction.query.count() == 1
        assert Transaction.query.first().amount == 4000.0


def test_add_expense(client):
    # Sprawdzenie poprawnego mapowania danych formularza na obiekt wydatku w bazie
    client.post('/add', data=dict(title='Kino', amount='50', type='expense'))
    with app.app_context():
        assert Transaction.query.first().title == 'Kino'
        assert Transaction.query.first().type == 'expense'


def test_balance_calculation(client):
    # Symulacja ruchu na koncie w celu przetestowania logiki obliczania salda
    client.post('/add', data=dict(title='Zysk', amount='1000', type='income'))
    client.post('/add', data=dict(title='Strata', amount='200', type='expense'))

    response = client.get('/')
    # Aplikacja powinna poprawnie wyświetlić różnicę: 1000 - 200 = 800
    assert b'800.00 PLN' in response.data


def test_delete_transaction(client):
    # Test usuwania rekordu po jego ID wygenerowanym w bazie
    client.post('/add', data=dict(title='Bilet', amount='10', type='expense'))
    with app.app_context():
        t = Transaction.query.first()
        client.get(f'/delete/{t.id}')

        # Upewniamy się, że po akcji usunięcia baza jest znowu pusta
        assert Transaction.query.count() == 0