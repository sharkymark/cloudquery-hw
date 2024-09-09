import subprocess
import psycopg2
import json
import os

def remove_plugins_directory():
    command = "rm -rf .cq/plugins"
    subprocess.run(command, shell=True)

def connect_to_db(conn_string):
    conn_string = os.environ.get(conn_string)
    if not conn_string:
        raise ValueError(f"Connection string '{conn_string}' not set.")

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    return conn, cursor

def extract_data_from_json(json_data):
    # Parse the JSON data and extract values
    id = json_data.get('Id')
    return id

def call_cloudquery(command):
    """Calls the CloudQuery CLI with the specified command."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr

def sync_coder_postgres():

    # Remove plugins directory
    remove_plugins_directory()

    # Call the CloudQuery CLI to sync the databases
    command = "cloudquery sync coder-postgres.yml"
    stdout, stderr = call_cloudquery(command)
    print("Output:", stdout)
    print("Error:", stderr)

    # Check if there were any errors
    if stderr:
        print("Error occurred while running CloudQuery CLI. Exiting.")
        return

    # Connect to the PostgreSQL database
    conn, cursor = connect_to_db("PG_CONNECTION_STRING_2")

    # Query the database for the synced data
    cursor.execute("SELECT * FROM workspaces")
    rows = cursor.fetchall()

    # Process the data
    #for row in rows:
    #    for value in row:
    #        print(value)

    # Print the count of rows
    print(f"\n{len(rows)} rows inserted into the 'workspaces' PostgreSQL table.")

    # Close the database connection
    cursor.close()
    conn.close()

def sync_postgres_postgres():

    # Remove plugins directory
    remove_plugins_directory()

    # Call the CloudQuery CLI to sync the databases
    command = "cloudquery sync postgres-postgres.yml"
    stdout, stderr = call_cloudquery(command)
    print("Output:", stdout)
    print("Error:", stderr)

    # Check if there were any errors
    if stderr:
        print("Error occurred while running CloudQuery CLI. Exiting.")
        return

    # Connect to the PostgreSQL database
    conn, cursor = connect_to_db("PG_CONNECTION_STRING_3")

    # Query the database for the synced data
    cursor.execute("SELECT * FROM mytable")
    rows = cursor.fetchall()

    # Process the data
    #for row in rows:
    #    for value in row:
    #        print(value)

    # Print the count of rows
    print(f"\n{len(rows)} rows inserted into the 'mytable' PostgreSQL table in the `mydestinationdatabase` database.")

    # Close the database connection
    cursor.close()
    conn.close()

def sync_salesforce_postgres():

    # Remove plugins directory
    remove_plugins_directory()

    # Call the CloudQuery CLI to sync the databases
    command = "cloudquery sync sfdc-postgres.yml"
    stdout, stderr = call_cloudquery(command)
    print("Output:", stdout)
    print("Error:", stderr)

    # Check if there were any errors
    if stderr:
        print("Error occurred while running CloudQuery CLI. Exiting.")
        return

    # Connect to the PostgreSQL database
    conn, cursor = connect_to_db("PG_CONNECTION_STRING_2")

    # Fetch all data
    cursor.execute("SELECT _cq_raw, object_type FROM salesforce_objects ORDER BY object_type")
    all_rows = cursor.fetchall()

    # Print the Ids (testing)
    for row in all_rows:
        json_data = row[0]
        id = extract_data_from_json(json_data)
        print(f"Id: {id}")

    # creating tables for each object type
    object_types = set(row[1] for row in all_rows)

    for object_type in object_types:
        table_name = object_type.lower() + 's'  # Convert to lowercase and add 's'

        # Drop existing table if it exists
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # Get JSON data for this object_type
        object_type_rows = [row for row in all_rows if row[1] == object_type]

        # Parse JSON data to extract column names and data types
        columns = []
        data_type_map = {
            'int': 'integer',
            'str': 'text',
            'float': 'real',
            'bool': 'boolean',
            'list': 'text',  # Assuming lists will be stored as JSON strings
            'dict': 'text'  # Assuming dicts will be stored as JSON strings
        }

        # Use the first row to determine the columns
        if object_type_rows:
            json_data = object_type_rows[0][0]
            for key, value in json_data.items():
                data_type = data_type_map.get(type(value).__name__, 'text')  # Default to 'text' if unknown
                columns.append((key, data_type))

        # Create new table with extracted columns
        create_table_sql = f"CREATE TABLE {table_name} ("
        for i, column in enumerate(columns):
            create_table_sql += f"{column[0]} {column[1]}"
            if column[0] == 'Id':
                create_table_sql += " PRIMARY KEY"
            if i < len(columns) - 1:
                create_table_sql += ", "
        create_table_sql += ")"
        cursor.execute(create_table_sql)

        # Insert data into new table
        insert_sql = f"INSERT INTO {table_name} ({', '.join([column[0] for column in columns])}) VALUES ({', '.join(['%s'] * len(columns))})"

        # Process rows to extract JSON data and convert to tuples
        rows_to_insert = [tuple(row[0].values()) for row in object_type_rows]

        # Execute the query
        cursor.executemany(insert_sql, rows_to_insert)
        conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()


def main():

    while True:
        try:

            print("\x1b[5 q")

            print("\n===========================================")
            print("*** Welcome to the CloudQuery Sync Tool ***")
            print("===========================================\n")

            action = input("""Enter:
            '1' to sync a table between two PostgreSQL databases,
            '2' to sync a workspaces table between a Coder PostgreSQL and another PostgreSQL database,
            '3' to sync Salesforce with PostgreSQL
            'q' to exit:
            
            """)
            if action == '1':
                sync_postgres_postgres()
            elif action == '2':
                sync_coder_postgres()
            elif action == '3':
                sync_salesforce_postgres()
            elif action == 'q':
                break
            else:
                print("Invalid input. Please try again.")

        except KeyboardInterrupt:
            print("\nExiting the CloudQuery Sync Tool...")
            break

if __name__ == "__main__":
    main()