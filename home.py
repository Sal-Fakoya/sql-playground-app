
import streamlit as st
import numpy as np
import pandas as pd
import sqlite3
from mysql.connector import Error
from mysql.connector import Error as MySQLError
from sqlite3 import Error as SQLiteError
import tempfile

# Define constant variables:

# SQLite
db_file = "data/sakila_master.db"
db_connection = sqlite3.connect("data/sakila_master.db")
c = db_connection.cursor()

# Function that prints db
def user_db_layout(db):
    st.success(f"""
            You are now conneted to \"{db}\"
            """)
    
# -------------SQLite Functions
# Function to create sqlite query section and results
def sqlite_cols(form_key, key, connection):
    col1, col2 = st.columns(2)
       
    with col1:
        with st.form(key = form_key):
            raw_query = st.text_area("SQLite Query", 
                                     placeholder="SELECT * FROM table_name")
            
            submit_query = st.form_submit_button("Execute")
            
        # Results layout
        with col2:
            if submit_query is True:
                st.success("Query Submitted")
                with st.expander("Your Query:", expanded = True):
                    st.write(raw_query)
    
    with st.expander("Query Results", expanded = True):   
        try: 
            query_results = all_sql_executor(query=raw_query, 
                                                        connection=connection, 
                                                        db_type="SQLite")
            if query_results is not None:
                table = pd.read_sql(raw_query, connection)
                st.dataframe(table, use_container_width = True)
                        
        except sqlite3.Error as e:
            st.warning(f"Invalid: {e}")
        except TypeError as e:
            st.info("Write a query to see results")  
        except Exception as e:
            st.info("Ensure your query is valid")
                
# Function to create sqlite3 layout
def create_sqlite3_layout(key, form_key, db_file, db_type):
   
    # Fetch the table names
        db_type = "SQLite"
        connection = createSQLiteConnection(db_file)
        
        tables = table_nameSQLite(connection, db_type)   # Create a drop-down menu (select box)
        
        
        selected_table = st.selectbox("View the tables", tables, index=None, key=key)
        
        # table info:
        with st.expander("Table Info"):
            if selected_table:
                selected_table_info = table_infoSQLite(selected_table=selected_table, 
                                                       connection=connection,
                                                       dbtype="SQLite")
                
                st.dataframe(selected_table_info, use_container_width = True)
                
        sqlite_cols(form_key=form_key, key=key, connection=connection)

# Function to get sqlite table names
def table_nameSQLite(connection, db_type):
    query = query = """
            SELECT name FROM sqlite_master 
             WHERE type='table';
             """
    return all_sql_executor(connection = connection, db_type = db_type, query = query)

# Function to get table info of table name in sqlite database
def table_infoSQLite(selected_table, connection, dbtype,):
    query = f"""
    PRAGMA table_info({selected_table});
    """
    return all_sql_executor(query, connection, db_type="SQLite")


# Function to get .db file for sqlite option from user in the My Database section and 
# displays layout for query and query results
def optionSQLite():
    db_file = st.file_uploader("Upload your db file", type=[".db", ".sql"])  
    
    
    if db_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(db_file.read())
            tmp_file_path = tmp_file.name
            
        connection = createSQLiteConnection(tmp_file_path)
        
        tables = table_nameSQLite(connection, db_type="SQLite")
        
        # Create a drop-down menu (select box)
        selected_table = st.selectbox("View the tables", tables, index=None, key="user_sqlite")
        
        # table info:
        with st.expander("Table Info"):
            if selected_table:
                selected_table_info = table_infoSQLite(selected_table=selected_table, connection=connection, dbtype="SQlite")
                st.dataframe(selected_table_info, use_container_width = True)
        
        sqlite_cols(form_key="user_sqlite_form", key="user_db_key", connection=connection)




#------------- MySQL Functions
# Function to connect to MySQL database
def connect_to_MySQL_database(host_name, user_name, user_password, database_name):
    connection = None
    
    if len(host_name.strip(" ")) == 0:
        st.warning("Host name cannot be empty!")
        return connection
    
    if len(database_name.strip(" ")) == 0:
        st.warning("Database name cannot be empty!")
        return connection
    
    try:
        connection = mysql.connector.connect(
            host=host_name.strip(" "),
            user=user_name.strip(" "),
            passwd=user_password.strip(" "),
            database=database_name.strip(" ")
        )
        st.success(f"Connection to database {database_name} successful!")
        return connection
    
    except Error as err:
        st.warning(f"Database connection failed. Error: {err}")
        return None

# Function to create MySQL query section and results
def mysql_cols(form_key, key, connection):
    col1, col2 = st.columns(2)
       
    with col1:
        with st.form(key = form_key):
            raw_query = st.text_area("MySQL Query", 
                                     placeholder="SELECT * FROM table_name", key=key)
            
            submit_query = st.form_submit_button("Execute")
        
        # Results layout
        with col2:
            if submit_query is True:
                st.success("Query Submitted")
                with st.expander("Your Query:", expanded = True):
                    st.write(raw_query)
            
    with st.expander("Query Results", expanded = True):   
        try: 
            if len(raw_query.strip(" ")) != 0:
                query_results = all_sql_executor(query=raw_query, 
                                                            connection=connection, 
                                                            db_type="MySQL")
                if query_results is not None:
                    table = pd.read_sql(raw_query, connection)
                    st.dataframe(table, use_container_width = True)
                    
        except MySQLError as e:
            st.warning(f"Invalid: {e}")
        except TypeError as e:
            st.info("Write a query to see results")  
        except Exception as e:
            st.info("Ensure your query is valid")
         
# Function to execute Any SQL query
def all_sql_executor(query, connection, db_type):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        if db_type == 'MySQL':
            result = cursor.fetchall()
            columns = [i[0] for i in cursor.description]
        elif db_type == 'SQLite':
            result = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
        return pd.DataFrame(result, columns=columns)
    except (MySQLError, SQLiteError) as e:
        st.warning(f"Invalid: {e}")
        return None
    


# Function to create a SQLite database connection
def createSQLiteConnection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print("SQLite connection successful")
    except SQLiteError as e:
        st.error(f"SQLite error: '{e}' occurred")
    
    return connection

# Function to get table names from MySQL database
def table_names_MySQL(database_connection, database_name, db_type, table_type):
    try:
        if table_type == "BASE TABLE":
            query = f"""
            SELECT table_name
            FROM information_schema.tables 
            WHERE table_schema = '{database_name}' && table_type = 'BASE TABLE';
            """
        elif table_type == "VIEWS":
            query = f"""
            SELECT table_name
            FROM information_schema.views 
            WHERE table_schema = '{database_name}';
            """
        
        return all_sql_executor(query=query, connection=database_connection, db_type=db_type)
    
    except MySQLError as e:
        return None
   
# Function to get table info on a selected table in MySQL
def table_info_MySQL(connection, table_name, db_type="MySQL"):
    # Query to describe the table structure
    query = f"DESCRIBE {table_name};"
    
    return all_sql_executor(query=query, connection=connection, db_type=db_type)


# Function that initalizes state variables for the MySQL section and 
# calls the other functions to build the query section
def optionMySQL():
    # Initialize session state variables
    if 'connection_established' not in st.session_state:
        st.session_state.connection_established = False
    if 'connection' not in st.session_state:
        st.session_state.connection = None
    if 'database_name' not in st.session_state:
        st.session_state.database_name = ''
    if 'host_name' not in st.session_state:
        st.session_state.host_name = ''
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ''
    if 'user_password' not in st.session_state:
        st.session_state.user_password = ''
    if 'table_type' not in st.session_state:
        st.session_state.table_type = None
        
        
    with st.expander("Enter your database info:", expanded=True):
        # Only display the form if the connection isn't established yet
        if not st.session_state.connection_established:
            with st.form("Enter info"):
                # User inputs for database connection
                host_name = st.text_input("Host name")
                user_name = st.text_input("Username")
                user_password = st.text_input("Password", type="password")
                database_name = st.text_input("Database name:")

                submit = st.form_submit_button("Submit")

            if submit:
                connection = connect_to_MySQL_database(host_name, user_name, user_password, database_name)

                if connection:
                    # Store connection details in session state
                    st.session_state.connection_established = True
                    st.session_state.connection = connection
                    st.session_state.database_name = database_name
                    st.success("Connection established! You can now select a table.")
                    
                else:
                    st.warning("Please enter valid information")
        else:
            st.info(f"Connected to database: {st.session_state.database_name}")
            if st.button("Reset Connection"):
                st.session_state.connection_established = False
                st.session_state.connection = None
                st.session_state.database_name = ''
                st.session_state.host_name = ''
                st.session_state.user_name = ''
                st.session_state.user_password = ''
                st.session_state.table_type = None
                st.session_state.mysql_selected_table = None
                st.rerun()
    
    # Display the rest of the interface if the connection is established
    if st.session_state.connection_established:
        
        # Use session state to store the selected table type
        if "table_type" not in st.session_state:
            st.session_state.table_type = None

        # Radio button to select table type
        option = st.radio(
            "Select a table type:", ["BASE TABLE", "VIEWS"],
            key="radio_table_type"
        )
        
        if option:
            st.session_state.table_type = option
    
        if st.session_state.table_type is not None:
            with st.expander(f"{st.session_state.table_type}", expanded=True):
                table_names = table_names_MySQL(
                    st.session_state.connection,
                    st.session_state.database_name,
                    db_type="MySQL",
                    table_type=st.session_state.table_type
                )
                
                selected_table = st.selectbox(
                    f"",
                    table_names,
                    index=0,
                    key="mysql_selected_table"
                )

                if selected_table:
                    st.write(f"You selected: {selected_table}")
                    table = table_info_MySQL(connection=st.session_state.connection,
                                             table_name=selected_table,
                                             db_type="MySQL")
                    st.dataframe(table, use_container_width = True)
                
            mysql_cols(form_key="mysql_cols", key="mysql_query", connection=st.session_state.connection)
                    
                    

# Function that calls the option functions in my database tab
def user_database():
    db_type = st.radio("Choose the DBMS you want to connect to", 
                        ["SQLite", "MySQL"], horizontal=True)  
    if db_type == "SQLite":
        optionSQLite()
            
    elif db_type == "MySQL":
       optionMySQL() 
       
                    
            
# Function that creates the tabs for the Home tab section
def createTabs():
    tab1, tab2 = st.tabs(["Sample", "My database"])
    
    with tab1:
        st.info("""
            The sample database used here is the sakila_master.db. 
            Use the dropdown to see the tables in the sakila database. 
            Write your query and click \"Execute\" button to run the sample query""")
        
        create_sqlite3_layout(key = "tab1", form_key="form_key1", db_file=db_file, db_type="SQLite")
    
    with tab2:
        user_database()
        pass


# Home page display
def home_page():
    st.markdown("# Home :house:")
    createTabs()

home_page()

