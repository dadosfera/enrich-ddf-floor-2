---
category: documentation
criticality: high
scope: all
---
# /ccon_check_concept_references
<!-- COMMAND_ID: 075 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: cc_check_concept -->

Check that important concepts (marked with CONCEPT markers) are properly referenced in parent READMEs

**Local Reference**: `commands/ccon_check_concept_references.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/ccon_check_concept_references.md`

## Description

Quick command to check that important concepts (marked with `<!-- CONCEPT: <slug> -->`) are properly referenced in parent READMEs to prevent documentation disconnections.

## Usage

`/ccon_check_concept_references`

## Details

Runs the concept reference chain checker to ensure that important concepts documented in deep layers are discoverable and properly referenced in parent READMEs.
