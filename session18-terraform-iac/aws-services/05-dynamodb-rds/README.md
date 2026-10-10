# DynamoDB & RDS - Database Services

## DynamoDB

DynamoDB is a managed NoSQL database for key-value and document data.

- A table contains items; an item contains attributes.
- A partition key identifies how data is distributed and supports key-based access.
- A composite primary key uses a partition key plus a sort key. Items sharing a partition key can be ordered and queried by sort key.
- Design keys around the application's access patterns.

Common uses: shopping carts, session data, device events and applications needing predictable key-based access at scale.

## RDS

RDS manages relational database instances. Supported engines include PostgreSQL, MySQL, MariaDB, Oracle, SQL Server and Db2. Applications use tables, relationships and SQL.

Place database instances in suitable VPC subnets, restrict Security Groups, protect credentials and use encryption. Automated backups and point-in-time recovery help recover data; snapshots provide additional backups.

A Multi-AZ DB instance deployment maintains a standby for availability and failover. That standby is not used for application read traffic. Read replicas can serve read workloads and use replication; they have different availability and consistency tradeoffs. Multi-AZ DB clusters are a separate deployment option with readable instances.

Common uses: transactional applications, order systems and existing SQL workloads. Choose DynamoDB for suitable NoSQL access patterns and RDS when relational queries and joins are needed.

Sources: [DynamoDB components](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html), [RDS overview](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html), [Multi-AZ DB instances](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html), [Read replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html).
