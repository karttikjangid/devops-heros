# Identity & RBAC - Governance

Microsoft Entra ID manages identities. Azure RBAC authorizes access to Azure resources.

| Concept | Azure meaning |
| --- | --- |
| User | A person's identity in the tenant |
| Group | A collection of users; assigning a role to a group simplifies access management |
| Service principal | An application's identity |
| Managed identity | An Azure-managed workload identity that avoids storing application credentials |
| Role definition | A set of allowed actions and data actions |
| Role assignment | A principal, role and scope, such as one resource group |

Least privilege means granting only the needed permissions at the narrowest useful scope. A reader of one storage container should not receive subscription Owner access.

Use MFA, managed identities for Azure workloads, limited role scopes and regular access reviews. Separate resource-management permissions from data-access permissions. Azure Policy governs resource compliance; it does not grant RBAC access.

Common uses: read-only resource inspection, a VM reading Blob Storage and a deployment identity managing one resource group.

Sources: [Azure role assignments](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments), [Role assignment steps](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-steps).
