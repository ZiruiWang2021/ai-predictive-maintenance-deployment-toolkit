# Go/No-Go Checklist / 上线决策清单

| Area / 领域 | Check / 检查项 | Evidence / 证据 | Decision / 决策 |
|---|---|---|---|
| Business / 业务 | Maintenance use case has named owner and agreed success metric / 维护场景有明确负责人和成功指标 | Signed pilot brief / 已签署试点说明 | Pending |
| Data / 数据 | Sensor data, work orders, and asset metadata reconcile at asset-cycle grain / 传感器数据、工单和资产元数据可在设备-周期粒度对齐 | Data quality report / 数据质量报告 | Pending |
| Data / 数据 | Refresh cadence is reliable and has freshness alerting / 数据刷新频率可靠，并具备新鲜度告警 | Pipeline run history / Pipeline 运行记录 | Pending |
| Model / 模型 | Validation metrics meet threshold for pilot assets / 试点资产的验证指标达到阈值 | Model card and metrics / Model card 和指标 | Pending |
| Model / 模型 | Failure-risk threshold is calibrated with maintenance capacity / 故障风险阈值结合维护容量完成校准 | Threshold review notes / 阈值复盘记录 | Pending |
| Model / 模型 | Human override process is documented / 人工 override 流程已记录 | Runbook / 运行手册 | Pending |
| Safety / 安全 | Recommendations cannot automatically defer safety-critical maintenance / 模型建议不能自动推迟安全关键维护 | Control design / 控制设计 | Pending |
| Dashboard / 仪表盘 | Maintenance planners can interpret risk tiers and action queue / 维护计划人员能理解风险等级和行动队列 | UAT notes / UAT 记录 | Pending |
| Operations / 运维 | Monitoring, incident response, and rollback owners are assigned / 监控、事件响应和回滚负责人已明确 | RACI / support rota | Pending |
| Governance / 治理 | Limitations and intended use are approved / 局限性和预期用途已批准 | Model card | Pending |
| Training / 培训 | Users know how to read the dashboard and challenge outputs / 用户知道如何阅读 dashboard 并质疑输出 | Training completion / 培训完成记录 | Pending |

## No-Go Triggers / 不上线触发条件

- Missing or stale production data with no manual fallback. / 生产数据缺失或过期，且没有人工 fallback。
- Evidence that the model systematically overestimates RUL for high-criticality assets. / 有证据表明模型系统性高估高关键资产的 RUL。
- No named owner for operational response to high-risk predictions. / 高风险预测没有明确运营响应负责人。
- Users cannot interpret or challenge model outputs during UAT. / UAT 中用户无法理解或质疑模型输出。
- Safety, compliance, or cybersecurity approval is incomplete. / 安全、合规或网络安全审批未完成。
