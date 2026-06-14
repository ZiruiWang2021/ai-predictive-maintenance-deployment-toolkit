# Limitations and Future Work / 局限性与后续改进

## Current Limitations / 当前局限性

- The default dataset is synthetic and should be treated as a reproducible demo, not operational evidence.
- 默认数据集是 synthetic data，只适合作为可复现 demo，不能作为真实运营证据。
- The model assumes complete run-to-failure histories; real maintenance data is often censored by inspection and component replacement.
- 模型假设存在完整的 run-to-failure 历史，而真实维护数据常被检查、部件更换或维修动作截断。
- The ridge model is transparent, but it does not fully capture sequence dynamics or asset-specific physics.
- Ridge 模型透明可读，但不能完整捕捉序列动态或资产特定物理机制。
- Risk thresholds are illustrative and need calibration with asset criticality, maintenance windows, safety rules, and maintenance capacity.
- 当前风险阈值仅用于演示，需要结合资产关键性、维修窗口、安全规则和维护容量重新校准。
- The dashboard reads batch scoring outputs; it is not a real-time condition monitoring system.
- Dashboard 读取批量评分输出，不是实时状态监测系统。

## Future Work / 后续改进

| Area / 方向 | Improvement / 改进 | Why It Matters / 价值 |
|---|---|---|
| Public benchmark / 公开基准 | Add a full C-MAPSS FD001 benchmark run with documented metrics / 增加完整 C-MAPSS FD001 benchmark 和指标记录 | Makes comparison more credible / 提升结果可信度和可比较性 |
| Model / 模型 | Add random forest, gradient boosting, or sequence model baselines / 增加随机森林、梯度提升或序列模型 baseline | Shows tradeoffs between transparency and accuracy / 展示透明度和准确率之间的权衡 |
| Explainability / 可解释性 | Add feature contribution or sensor trend explanations / 增加特征贡献或传感器趋势解释 | Helps planners understand why an asset is high risk / 帮助用户理解为什么某设备高风险 |
| Uncertainty / 不确定性 | Replace residual bands with calibrated prediction intervals / 用校准后的预测区间替代简单残差区间 | Better supports risk-based planning / 更适合基于风险的计划决策 |
| MLOps / 机器学习运维 | Add model registry, versioned scoring outputs, and drift reports / 增加模型注册、版本化评分输出和漂移报告 | Moves the demo closer to production operation / 让 demo 更接近生产运行 |
| Product workflow / 产品流程 | Add planner feedback capture and override analytics / 增加维护人员反馈和 override 分析 | Connects model performance to real adoption / 将模型表现和真实采用情况连接起来 |
| Costing / 成本收益 | Estimate avoided downtime and inspection cost tradeoffs / 估算避免停机和检查成本之间的权衡 | Makes the business case more concrete / 让业务价值更具体 |
