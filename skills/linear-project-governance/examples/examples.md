# Governance Examples

## Intake without immediate write

User input:

> Customers report that long uploads occasionally freeze the browser. We do not know whether the current release still reproduces it.

Correct classification:

- `Q`: Does the current release still reproduce browser freezing during long uploads?
- Analysis task: establish a reproducible test matrix.

Do not create a confirmed `PROB` until current evidence confirms it.

## Material change

Existing REQ:

> Support files up to 10 GB.

New approved constraint:

> Limit uploads to 5 GB for the first release.

Correct action:

- create or update a `CR`;
- relate it to the original REQ;
- identify implementation and validation tasks that still assume 10 GB;
- do not silently rewrite history.

## Explicit confirmation

User:

> Create the two confirmed items and their validation task now.

This is confirmation for those exact actions. Execute, read back and report the identifiers and relations. Do not ask for redundant confirmation.
