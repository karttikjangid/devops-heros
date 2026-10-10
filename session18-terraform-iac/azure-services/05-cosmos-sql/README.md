# Cosmos DB & Managed Relational Databases

## Cosmos DB

Azure Cosmos DB is a managed NoSQL database. In its NoSQL API, a database contains containers, and containers contain JSON items with properties.

A partition key distributes items across partitions and helps route queries. An item is identified by its `id` within its logical partition. Choose a partition key that fits access patterns and spreads traffic. DynamoDB's partition-key/sort-key design does not map directly to an identical Cosmos DB sort-key feature.

Common uses: product catalogs, user profiles, device data and globally distributed JSON applications.

## Managed relational databases

Azure SQL Database provides managed SQL Server database capabilities. Azure Database for PostgreSQL and Azure Database for MySQL Flexible Server are separate managed services for those engines.

These services use relational tables and SQL. Secure them with suitable identities, restricted networking, protected credentials and encryption. Automated backups support recovery; retention and availability options depend on the chosen service and tier.

High availability protects against failures. Read-scale and read-replica features serve read workloads where the specific service supports them; they are not interchangeable with backup or failover.

Common uses: order systems, transactional applications and existing SQL workloads. No database service is deployed for this research task.

Sources: [Cosmos DB components](https://learn.microsoft.com/en-us/azure/cosmos-db/resource-model), [Partitioning](https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning-overview), [Azure SQL Database](https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview), [PostgreSQL](https://learn.microsoft.com/en-us/azure/postgresql/overview), [MySQL](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/overview).
