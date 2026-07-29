# Audit Examples

## Orphan task

Task:

> Improve caching mechanism

Relations: none.

Result:

- High exception: execution task has no governance source.
- Suggested action: relate it to a current REQ/PROB/DEC/CR/RISK/Q or document approved operational maintenance.

## Done without evidence

Task state: Done.
Description: "Implemented and tested."
No PR, commit, test output, document, screenshot or acceptance record is accessible.

Result:

- High exception: completion claim lacks verifiable evidence.
- Do not automatically reopen or close the source requirement.

## GitHub conflict

Linear claims release deployment completed. The referenced PR is still Draft and no deployment evidence is available.

Result:

- Critical or High exception depending on release impact.
- Report the conflict; do not claim the deployment failed if the connector cannot inspect the actual environment.
