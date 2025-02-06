# SQL_PlaygroundApp

## About This Application

Welcome to the SQL Query Analyzer app! This tool allows you to interact with databases through SQL queries and file uploads, 
    supporting both SQLite and MySQL databases.

### Key Features

 - **Dual Database Support**:
        - 🗄️ Connect to **SQLite** databases (both file upload and pre-loaded sample database)
        - 🐬 Connect to **MySQL** servers using credentials
    - **Query Execution**:
        - ✏️ Write and execute SQL queries directly in the browser
        - 📊 View results in interactive pandas DataFrames
    - **Database Exploration**:
        - 🔍 Browse available tables/views
        - 📄 View table schemas and column information
    - **File Handling**:
        - 📤 Upload your own SQLite database files (.db/.sql)
        - 🗂️ Work with temporary file storage for uploaded databases

    ### How to Use

    **Sample Database (SQLite)**:
    1. Navigate to the *Home > Sample* tab
    2. Select a table from the dropdown
    3. Write queries in the provided text area
    4. Click *Execute* to run queries against the Sakila sample database

    **My Database Section**:
    1. In the *Home > My Database* tab:
        - For SQLite:
            - Upload your database file (.db/.sql)
            - Explore and query like the sample database
        - For MySQL:
            - 🔒 Enter connection credentials (host, user, password, database)
            - Choose between tables and views
            - Execute queries against your live database

    ### Technologies Used
    - Built with [Streamlit](https://streamlit.io/)
    - Data handling with [pandas](https://pandas.pydata.org/)
    - SQLite integration via [sqlite3](https://docs.python.org/3/library/sqlite3.html)
    - MySQL connectivity using [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)

    ### Important Notes
    - 🔐 MySQL credentials are not stored and remain active only during your session
    - 📁 Uploaded SQLite files are handled through temporary storage
    - ⚠️ Always exercise caution when executing write operations (INSERT/UPDATE/DELETE)
    - 💡 The sample database uses the [Sakila](https://dev.mysql.com/doc/sakila/en/) example database

    ### Safety & Security
    - This is a demonstration application - do not use with sensitive credentials
    - All database interactions happen in your local environment
    - No data is stored or transmitted externally
