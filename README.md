# CloudQuery Hello, World!

CloudQuery is data movement ELT software. You download a CLI, create source and destination configurations (e.g., PostgreSQL to PostgresSQL or Salesforce to PostgreSQL)

## Commands

### Install with brew

```sh
brew install cloudquery/tap/cloudquery
```

### Initialize

```sh
cloudquery login
```

### Create configuration `yml`

e.g., `postgres-postgres.yml`

```yaml
kind: source
spec:
  name: "postgresql"
  registry: "cloudquery"
  path: "cloudquery/postgresql"
  version: "v6.7.2"
  tables: ["workspaces"]
  destinations: ["postgresql"]
  # Learn more about the configuration options at https://cql.ink/postgresql_source
  spec:
    connection_string: "${PG_CONNECTION_STRING_1}" # set the environment variable in a format like postgres://postgres:pass@localhost:5432/postgres?sslmode=disable
    # Optional parameters:
    # cdc_id: "postgresql" # Set to a unique string per source to enable Change Data Capture mode (logical replication, or CDC)
    # pgx_log_level: error
    # rows_per_record: 500
---
kind: destination
spec:
  name: "postgresql"
  path: "cloudquery/postgresql"
  registry: "cloudquery"
  version: "v8.5.4"
  write_mode: "overwrite-delete-stale"
  # Learn more about the configuration options at https://cql.ink/postgresql_destination
  spec:
    connection_string: "${PG_CONNECTION_STRING_2}" # set the environment variable in a format like postgres://postgres:pass@localhost:5432/postgres?sslmode=disable
    # you can also specify it in DSN format, which can hold special characters in the password field:
    # connection_string: "user=postgres password=pass+0-[word host=localhost port=5432 dbname=postgres"
    # Optional parameters:
    # pgx_log_level: error
    # batch_size: 10000 # 10K entries
    # batch_size_bytes: 100000000 # 100 MB
    # batch_timeout: 60s

    # create_performance_indexes: false #create indexes that help with performance when using `write_mode: overwrite-delete-stale`

```

### Sync (run)

```sh
cloudquery sync postgres-postgres.yml
```

## Plugins

### PostgreSQL

Put the tablename that you want to sync in the source. And create environment variables for the PostgreSQL connection strings.

### Salesforce

Put the objects you want to sync in the source spec. Maybe I'm doing something wrong, but all it syncs is the Salesforce Id, for the Account object, and no other columns.

## Python app

`sync.py` is a simple CLI app to run the `cloudquery` command line for:
1. PostgreSQL-to-PostgreSQL table sync
1. A Coder cloud dev environment PostgreSQL to PostgreSQL workspaces table sync
1. A Salesforce-to-PostgreSQL sync

The app uses 3 CloudQuery configurations in `.yml` files.

The app assumes environment variables are set for Salesforce and two PostgreSQL database authentication credentials.

The app has logic to create new PostgreSQL tables (e.g., acccounts, contacts) for Salesforce objects discovered in the synced `salesforce_objects` table created by the CloudQuery `sfdc-postgres.yml` example.

> The following Python package is required to retrieve values from the PostgreSQL databases. This is to prove data was synced with PostgreSQL. It is automatically installed in using the Dev Container.

```sh
pip install psycopg2-binary
```

## Dev Container 

If you want to run everything in a Dev Container, this will spin up PostgreSQL and Python containers and the PostgreSQL database can be used in CloudQuery examples.

> If you have also run the CloudQuery CLI on the host, before the Dev Container, delete the `.cq` plugins directory if the architecture of the Dev Container does not match the host. 

## psql client

psql is added to the Python container or add to your local machine like mac to test connectivity

### local machine 

```sh
brew install libpq
```

if `psql` is not found, run

```sh
brew link --force libpq
```

### connect

```sh
psql -h localhost -p 5432 -U postgres -d postgres
```

### commands

* list users `\du`
* list database `\l`
* contact to a database `\c <database>`
* list tables `\dt`
* list schemas `\d <table name>`

### add data

This insert statement could have been added to `init.sql` but here we demonstrate how to run with `psql` from the project directory in the Python container

```sh
psql -h localhost -p 5432 -U postgres -d mydatabase -f insert.sql
```

## Destination PostgreSQL Connection string environment variable


Adjust to your PostgreSQL installation or will be as follows with Dev Container PostgreSQL defined in `docker-compose.yml`
```sh
export PG_CONNECTION_STRING_2="postgres://postgres:postgres@localhost:5432/mydatabase"
export PG_CONNECTION_STRING_3="postgres://postgres:postgres@localhost:5432/mydestinationdatabase"
```

## Coder's PostgreSQL database

Coder is a Cloud Development Environment "CDE" self-hosted OSS platform. It has a PostgreSQL embedded database which is a CloudQuery source in the `sync.py` and `coder-postgres.yml` example.

### Install

```sh
curl -L https://coder.com/install.sh | sh
```

### Get PostgreSQL connection string

```sh
coder server postgres-builtin-url
```

### Coder Connection string environment variable


Actual port and password will vary by Coder installation
```sh
export PG_CONNECTION_STRING_1="postgres://coder@localhost:<assigned port - not 5432>/coder?sslmode=disable&password=<assigned password>"
```

## Resources

[CloudQuery SaaS dashboard](https://cloud.cloudquery.io/)

[CloudQuery OSS](https://github.com/cloudquery/cloudquery)

[CloudQuery docs](https://docs.cloudquery.io/docs)

[Install CLI macOS](https://docs.cloudquery.io/docs/quickstart/macOS)

[Source plugins](https://hub.cloudquery.io/plugins/source)

[Destination plugins](https://hub.cloudquery.io/plugins/destination)

[PostgreSQL source plugin](https://hub.cloudquery.io/plugins/source/cloudquery/postgresql/latest/docs
)
[PostgreSQL destination plugin](https://hub.cloudquery.io/plugins/destination/cloudquery/postgresql/latest/docs)

[Salesforce source plugin](https://hub.cloudquery.io/plugins/source/cloudquery/salesforce/latest/docs)

[Salesforce objects](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_list.htm)

[Basic transformer](https://hub.cloudquery.io/plugins/transformer/cloudquery/basic/latest/docs)

[Coder OSS](https://github.com/coder/coder)

## License

This project is licensed under the [MIT License](LICENSE)

## Contributing

### Disclaimer: Unmaintained and Untested Code

Please note that this program is not actively maintained or tested. While it may work as intended, it's possible that it will break or behave unexpectedly due to changes in dependencies, environments, or other factors.

Use this program at your own risk, and be aware that:
1. Bugs may not be fixed
1. Compatibility issues may arise
1. Security vulnerabilities may exist

If you encounter any issues or have concerns, feel free to open an issue or submit a pull request.