# IAM - Governance

IAM controls who can access AWS resources and which actions they can perform.

| Concept | Meaning |
| --- | --- |
| User | An identity in an AWS account; can have console or API credentials |
| Group | A collection of IAM users that share permissions |
| Role | An identity assumed by a person or service using temporary credentials |
| Policy | A JSON document defining allowed or denied actions, resources and conditions |
| Permission | Authorization to perform an action on a resource |

Least privilege means granting only the access needed for a task. For example, a reader of one S3 bucket needs access to that bucket, not administrator access to the account.

Use federation/IAM Identity Center for people, roles for workloads, MFA and temporary credentials. Protect the root user and avoid routine root use. Review unused permissions and credentials, and remove access when it is no longer needed.

Common uses: read-only support access, an EC2 role accessing S3, and a deployment role restricted to one project's resources.

Sources: [Policies and permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html), [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html).
