# Specyfikacja Projektu: SmartBudget

## 1. Opis i Funkcjonalności
SmartBudget to prosta aplikacja webowa do zarządzania budżetem domowym.
- **Dodawanie transakcji:** Użytkownik może dodać wydatek lub przychód (kwota, kategoria, opis, data).
- **Historia transakcji:** Wyświetlanie tabeli z ostatnimi transakcjami.
- **Podsumowanie salda:** Automatyczne wyliczanie obecnego stanu konta (Przychody - Wydatki).
- **Usuwanie:** Możliwość usunięcia błędnie wprowadzonej transakcji.

## 2. Wygląd aplikacji (UI)
- Aplikacja typu Single Page.
- Na górze: Duży nagłówek z aktualnym saldem (na zielono lub czerwono).
- Po lewej stronie: Formularz dodawania nowej transakcji.
- Po prawej stronie: Tabela z historią transakcji i przyciskiem "Usuń" przy każdej z nich.
- Stylizacja: Czysty minimalizm, wykorzystanie frameworka np. Bootstrap lub prosty CSS.

## 3. Wymagania techniczne
- **Backend:** Python 3.10+, framework Flask.
- **Baza danych:** SQLite (biblioteka SQLAlchemy).
- **Frontend:** HTML5, podstawowy CSS.
- **Testy:** biblioteka `pytest`.

## 4. Schemat bazy danych
**Tabela `Transaction`**
- `id` (Integer, Primary Key)
- `type` (String) - 'income' lub 'expense'
- `amount` (Float) - kwota
- `category` (String) - kategoria (np. Jedzenie, Wypłata)
- `description` (String) - opcjonalny opis
- `date` (DateTime) - data dodania