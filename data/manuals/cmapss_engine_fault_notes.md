# C-MAPSS Engine Fault Notes

Synthetic demo document for portfolio use only. It is not an official NASA document or OEM manual.

## Purpose

These notes explain how C-MAPSS-style run-to-failure sensor data can support Remaining Useful Life prediction in a predictive maintenance demo.

## Degradation patterns

C-MAPSS-style data represents assets observed over operating cycles until failure. RUL is usually labelled as the final observed cycle minus the current cycle. Sensor drift, compressor efficiency changes, temperature-related signals, pressure shifts, and operating settings can provide evidence of degradation.

## Interpretation

A low predicted RUL should not be treated as a standalone instruction to replace equipment. It should trigger review of sensor trends, data quality, asset criticality, maintenance history, and operational constraints. If low RUL appears together with abnormal vibration, high temperature, or a fault description, the overall risk should increase.

## Recommended use

Use C-MAPSS-style data to demonstrate feature engineering, model validation, risk tiering, and decision support. Use asset-level holdout validation to reduce leakage between training and testing data.

## Limitations

This document is synthetic demo data. Real production RUL systems require calibrated labels, maintenance reset handling, censored history treatment, and site-specific validation.
