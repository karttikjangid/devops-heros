# Azure Blob Storage - Object Storage

A storage account contains blob containers. A container groups blobs; a blob contains object data and metadata. This is the Azure object-storage equivalent used instead of the assignment's S3 bucket.

| Feature | Purpose |
| --- | --- |
| Access tiers | Hot for frequent access; Cool and Cold for less frequent access; Archive for offline archival data |
| Versioning | Keeps previous versions after changes, supporting recovery |
| Lifecycle rules | Transition or expire blobs and previous versions automatically |
| Encryption | Azure Storage encrypts stored data; HTTPS protects transport |
| Access control | Azure RBAC data roles, SAS tokens and storage-account authorization govern access |

A private container does not allow anonymous blob access. The demo also disables public access at the account level. Account names must be globally unique and use lowercase letters and numbers.

Cool, Cold and Archive tiers have retrieval and minimum-retention considerations. The short-lived demo uses Hot storage and LRS replication. Storage-account keys and SAS tokens must stay out of Git.

Common uses: uploads, backups, logs, static assets and data lakes.

Sources: [Blob Storage overview](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-overview), [Access tiers](https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview), [Lifecycle management](https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview).
