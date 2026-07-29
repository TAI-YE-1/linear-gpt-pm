# Security

Do not commit credentials, API tokens, private issue exports, customer data or repository secrets.

The Skills must follow least privilege:

- Linear writes require explicit user intent or a previously approved automation scope.
- GitHub is read-only by default for evidence verification.
- Automated audit runs may write reports, comments or status updates only when configured.
- Automated runs must not approve changes, close business requirements, accept risks or delete records.

Report security concerns privately to the repository owner.
