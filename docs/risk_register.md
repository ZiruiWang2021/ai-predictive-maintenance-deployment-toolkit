# Risk Register / 风险登记册

| ID | Risk / 风险 | Impact / 影响 | Likelihood / 可能性 | Severity / 严重性 | Mitigation / 缓解措施 | Owner / 负责人 | Status / 状态 |
|---|---|---:|---:|---:|---|---|---|
| R1 | Historical failure labels are incomplete or inconsistent / 历史故障标签不完整或不一致 | High | Medium | High | Reconcile sensor data with work orders and failure codes before training / 训练前对齐传感器数据、工单和故障代码 | Data engineer | Open |
| R2 | Model overestimates RUL for safety-critical assets / 模型高估安全关键资产的 RUL | High | Medium | High | Use conservative thresholds, uncertainty bands, and human approval before deferral / 使用保守阈值、不确定性区间和人工审批 | Data scientist | Open |
| R3 | Asset operating conditions differ from training data / 资产运行条件与训练数据不同 | Medium | Medium | Medium | Monitor input drift by route, asset class, and operating regime / 按线路、资产类型和运行工况监控输入漂移 | ML engineer | Open |
| R4 | Maintenance teams do not trust recommendations / 维护团队不信任模型建议 | High | Medium | High | Co-design dashboard, expose drivers, and run shadow-mode pilot / 共同设计 dashboard，展示影响因素，并先做 shadow-mode 试点 | PM | Open |
| R5 | Dashboard becomes stale because data refresh fails / 数据刷新失败导致 dashboard 过期 | Medium | Medium | Medium | Add freshness checks, alerting, and fallback process / 增加新鲜度检查、告警和 fallback 流程 | Analytics engineer | Open |
| R6 | False positives overload maintenance capacity / 误报过多导致维护资源过载 | Medium | Medium | Medium | Tune threshold with planner capacity and asset criticality / 结合维护容量和资产关键性调整阈值 | Operations lead | Open |
| R7 | Production data contains PII or sensitive operational detail / 生产数据包含个人信息或敏感运营信息 | High | Low | Medium | Complete governance review and role-based access controls / 完成数据治理评审和基于角色的访问控制 | Governance lead | Open |
| R8 | Model ownership is unclear after pilot / 试点后模型 ownership 不清晰 | Medium | Medium | Medium | Assign service owner, monitoring owner, and business decision owner before launch / 上线前明确服务负责人、监控负责人和业务决策负责人 | Sponsor | Open |

## Review Cadence / 复盘节奏

- Weekly during build and pilot. / 构建和试点阶段每周复盘。
- Fortnightly during the first two months after go-live. / 上线后前两个月每两周复盘。
- Monthly once monitoring is stable. / 监控稳定后每月复盘。
