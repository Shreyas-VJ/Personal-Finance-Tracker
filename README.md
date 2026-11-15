\# Personal Finance Tracker



A Python-based Personal Finance Tracker that helps users manage income, expenses, and monitor their financial activities using MySQL.



\## Features



\- Add income and expense transactions

\- View all recorded transactions

\- Track total income, expenses, and current balance

\- Delete transactions using transaction IDs

\- Filter transactions by date range

\- Generate category-wise expense reports

\- Input validation and error handling

\- MySQL database integration

\- Automated testing with pytest



\## Technology Stack



\- \*\*Language:\*\* Python

\- \*\*Database:\*\* MySQL

\- \*\*Libraries:\*\* mysql-connector-python, python-dotenv

\- \*\*Testing:\*\* pytest, pytest-cov

\- \*\*Development Environment:\*\* VS Code



\## Project Structure



```text

Personal-Finance-Tracker/

├── src/

│   ├── database.py

│   ├── main.py

│   └── transactions.py

├── tests/

│   ├── test\_database.py

│   ├── test\_main.py

│   └── test\_transactions.py

├── .env.example

├── .gitignore

├── requirements.txt

└── README.md

```



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd Personal-Finance-Tracker

```



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



\### 3. Activate the virtual environment



Windows:



```bash

.venv\\Scripts\\activate

```



\### 4. Install dependencies



```bash

python -m pip install -r requirements.txt

```



\### 5. Configure environment variables



Create a `.env` file using `.env.example` as a template.



Enter your local MySQL credentials and database names in `.env`.



\### 6. Set up MySQL



Create the following databases in MySQL:



\- `personal\_finance\_tracker`

\- `personal\_finance\_tracker\_test`



Create the `transactions` table in both databases using the schema provided in the project setup.



\### 7. Run the application



```bash

python -m src.main

```



\## Running Tests



Run all tests:



```bash

python -m pytest -v

```



Generate code coverage:



```bash

python -m pytest --cov=src --cov-report=term-missing

```



\## Current Testing Status



\- \*\*Automated tests:\*\* 33 passing

\- \*\*Code coverage:\*\* 88%



\## Future Improvements



\- Graphical dashboard for financial analytics

\- Monthly and yearly financial reports

\- Export transactions to CSV and PDF

\- User authentication and multiple accounts

\- REST API using FastAPI



\## Author



Shreyas VJ

