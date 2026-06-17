# Synthetic Fault Case Notes

Synthetic demo document for portfolio use only. It is not a real incident log.

## Case 1: Motor overheating with high current

Observed symptoms: rising motor temperature, high current, and reduced airflow. Recommended analysis: validate the temperature sensor, inspect cooling path blockage, check fan condition, compare current imbalance across phases, and review recent load changes. If the trend continues upward, classify risk as high and plan inspection in the next safe maintenance window.

## Case 2: Bearing vibration after lubrication

Observed symptoms: elevated vibration after lubrication, mild temperature increase, and operator-reported noise. Recommended analysis: check lubrication quantity and type, inspect bearing temperature, review alignment, and compare vibration trend across recent cycles. If vibration and temperature rise together, escalate the asset for planned intervention.

## Case 3: Single-cycle sensor spike

Observed symptoms: one sensor jumps to an impossible value for a single record while related sensors remain stable. Recommended analysis: treat this as a data quality issue first. Validate sensor calibration, wiring, timestamp alignment, and unit conversion before classifying an equipment fault.

## Uncertainty note

These cases are synthetic examples included to support RAG retrieval and Agent evaluation. Real investigations require site records, OEM guidance, and engineer review.
