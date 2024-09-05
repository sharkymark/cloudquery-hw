# CloudQuery Hello, World!

CloudQuery is data movement ELT software. You download a CLI, create source and destination configurations (e.g., Postgres to Postgres or Salesforce to Postgres)

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
    connection_string: "${PG_CONNECTION_STRING_1" # set the environment variable in a format like postgres://postgres:pass@localhost:5432/postgres?sslmode=disable
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
    connection_string: "${PG_CONNECTION_STRING_2" # set the environment variable in a format like postgres://postgres:pass@localhost:5432/postgres?sslmode=disable
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

### Postgres

Put the tablename that you want to sync in the source. And create environment variables for the Postgres connection strings.

### Salesforce

Put the objects you want to sync in the source spec. Maybe I'm doing something wrong, but all it syncs is the Salesforce Id, for the Account object, and no other columns.

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

[Ssalesforce source plugin](https://hub.cloudquery.io/plugins/source/cloudquery/salesforce/latest/docs)

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