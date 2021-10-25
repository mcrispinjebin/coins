# Coins Wallet

A general purpose wallet that allows customer to view their account, transfer funds between accounts with Django REST framework.

---

[Django REST](https://www.django-rest-framework.org/)

---

**Contents**

1. [Setup](#setup)
1. [API docs](#api-docs)
1. [DB Schema](#db-schema)
1. [Quality](#quality)
1. [Future Scope](#future-scope)

---

### Setup ###

1. Python (>3.0)
1. PostgreSQL
1. Clone the repo in local
1. Link the postgreSQL config in `coins/settings.py` file
1. Install python dependencies  `pip intall -r requirements.txt`
1. Do django migrations
1. Run development server - `python manage.py runserver`

---

### API docs ###

API documentation is available in `coins/spec/api_spec.txt`

Swagger is also used for API documentation and is configured in below endpoint.

```http://127.0.0.1:8000/apidocs```

---

### DB Schema ###
Three tables will be migrated along with django migrations.

- Account
- Wallet
- Transactions

Account and wallet has one - one mapping.

---

### Quality ###

Unit Test cases are available in `coins/tests/` folder.\
Flake8 is used as static code analyzer to improve code quality.

---

### Future Scope ###

1. Expose apis to add money to wallet, extending payment transfer to merchant transfer.
1. To move the code to containerised version - Docker.
1. To add code analyzer in pre commit hook.

---
