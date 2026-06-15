# Sensor Anomaly Guide

Synthetic demo document for portfolio use only. It is not a real OEM manual.

## Purpose

This guide explains how to handle abnormal sensor readings before treating them as true equipment degradation. It is useful for RAG and Agent demos where retrieved evidence must distinguish data quality issues from asset faults.

## Common anomaly patterns

A sudden single-cycle spike, impossible numeric value, missing record, flatlined signal, or reading that disagrees with redundant sensors may indicate sensor or pipeline issues. Sensor mounting, wiring, calibration, timestamp alignment, and unit conversion should be checked before escalating maintenance risk.

## Validation steps

Compare the suspect sensor with related signals, previous cycles, redundant instruments, and operator notes. Check whether the anomaly appears across multiple sensors or only one channel. Validate schema, units, sampling frequency, and data freshness. For impossible values, exclude or flag the record and request a sensor check.

## Recommended action

If evidence suggests a sensor issue, classify uncertainty clearly and avoid making a strong equipment fault claim. If multiple related sensors deteriorate together, continue diagnosis using maintenance manuals and RUL prediction.

## Limitations

This document is synthetic demo data and does not replace site instrumentation procedures or calibrated measurement checks.
