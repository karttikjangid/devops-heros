# S3 - Storage

S3 stores objects in buckets. An object contains data, a key and metadata; a general-purpose bucket has a unique name within its AWS partition.

| Feature | Purpose |
| --- | --- |
| Storage classes | Match access frequency and retrieval needs: Standard, Intelligent-Tiering, Standard-IA, One Zone-IA and Glacier options |
| Versioning | Retains multiple versions of an object, helping recover from overwrites and deletions |
| Lifecycle policy | Automatically transitions or expires objects and old versions |
| Encryption | Protects stored data; S3 encrypts new object uploads by default. SSE-S3 uses S3-managed keys; SSE-KMS uses KMS keys |
| Bucket policy | A resource-based JSON policy controlling access to a bucket and its objects |

Choose storage classes carefully: archival and infrequent-access classes can have retrieval charges and minimum storage durations. Versioning also retains data until old versions are removed.

Keep buckets private, use Block Public Access, and grant only required object/bucket actions. Encryption does not replace access control.

Common uses: backups, application uploads, logs, static assets and data lakes.

Sources: [S3 overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html), [Storage classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html), [Encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html).
