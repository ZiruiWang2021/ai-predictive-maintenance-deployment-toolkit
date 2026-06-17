# Project Delivery Governance Notes

Synthetic demo document for portfolio use only. It summarises delivery governance context for the predictive maintenance pilot.

## Pilot scope

The pilot is framed as a 36-week Network Rail-style AI predictive maintenance deployment covering 100 railway infrastructure assets. The goal is to test whether RUL prediction, dashboard triage, RAG retrieval, and Agent-generated maintenance reports can support planner decision-making.

## Delivery artefacts

Required delivery artefacts include project scope, WBS, schedule, budget, risk register, stakeholder map, communication plan, go/no-go checklist, deployment runbook, rollback route, and model card. These artefacts help non-coding stakeholders understand how the AI system would be governed in a real deployment.

## Go/no-go criteria

A go decision requires acceptable data quality, validated RUL performance, clear limitations, human approval path, rollback process, monitoring owner, and evidence that planners can interpret the dashboard and Agent report. A no-go decision is triggered by unresolved safety risk, stale data, weak model recall, unclear ownership, or missing rollback process.

## Communication plan

Senior sponsors receive fortnightly scope, budget, risk, and go/no-go updates. Maintenance planners join UAT workshops at each dashboard release candidate. Asset engineers review model assumptions and risk thresholds weekly during modelling. Safety and compliance review intended use, limitations, human approval, and rollback at approval gates.

## Uncertainty note

This document is synthetic project delivery context for a portfolio RAG workflow. It is not a real Network Rail delivery document.
