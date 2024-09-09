import subprocess
import psycopg2
import json
import os

def connect_to_db(conn_string, table_name):
    conn_string = os.environ.get(conn_string)
    if not conn_string:
        raise ValueError(f"Connection string '{conn_string}' not set.")

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    return conn, cursor

def extract_data_from_json(json_data):
    # Parse the JSON data and extract values
    data = json_data
    id = data.get('Id')
    name = data.get('Name')
    #description = data.get('Description')
    website = data.get('Website')
    industry = data.get('Industry')
    return id, name, website, industry

def call_cloudquery(command):
    """Calls the CloudQuery CLI with the specified command."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr

def sync_coder_postgres():
    # Call the CloudQuery CLI to sync the databases
    command = "cloudquery sync coder-postgres.yml"
    stdout, stderr = call_cloudquery(command)
    print("Output:", stdout)
    print("Error:", stderr)

    # Connect to the PostgreSQL database
    conn, cursor = connect_to_db("PG_CONNECTION_STRING_2", "workspaces")

    # Query the database for the synced data
    cursor.execute("SELECT * FROM workspaces")
    rows = cursor.fetchall()

    # Process the data
    for row in rows:
        for value in row:
            print(value)

    # Close the database connection
    cursor.close()
    conn.close()

def sync_salesforce_postgres():
    # Call the CloudQuery CLI to sync the databases
    command = "cloudquery sync sfdc-postgres.yml"
    stdout, stderr = call_cloudquery(command)
    print("Output:", stdout)
    print("Error:", stderr)

    # Connect to the PostgreSQL database
    conn, cursor = connect_to_db("PG_CONNECTION_STRING_2", "salesforce_objects")

    # Query the database for the synced data
    cursor.execute("SELECT _cq_raw FROM salesforce_objects")
    rows = cursor.fetchall()

    # Process the data
    for row in rows:
        json_data = row[0]
        id, name, website, industry = extract_data_from_json(json_data)
        print(f"Id: {id}")
        print(f"Name: {name}")
        print(f"Website: {website}")
        print(f"Industry: {industry}")

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
            '1' to sync Coder PostgreSQL with another PostgreSQL database,
            '2' to sync Salesforce with PostgreSQL,
            'q' to exit:
            
            """)
            if action == '1':
                sync_coder_postgres()
            elif action == '2':
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