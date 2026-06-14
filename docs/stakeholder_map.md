# Stakeholder Map / 利益相关方地图

| Stakeholder / 利益相关方 | Interest / 关注点 | Influence / 影响力 | What They Need / 需要什么 | Engagement / 沟通方式 |
|---|---|---:|---|---|
| Maintenance planners / 维护计划人员 | Prioritized intervention queue and confidence in recommendations / 优先级队列和对建议的信心 | High | Clear risk tiers, action owner, and override path / 清晰风险等级、行动负责人和 override 路径 | Weekly build reviews and UAT / 每周评审和 UAT |
| Asset engineers / 资产工程师 | Technical validity and asset-specific thresholds / 技术有效性和资产特定阈值 | High | Sensor features, failure modes, and threshold rationale / 传感器特征、故障模式和阈值依据 | Design workshops and model review / 设计工作坊和模型评审 |
| Operations control / 运营控制 | Service reliability and disruption reduction / 服务可靠性和减少中断 | High | Impact on incidents, delays, and capacity / 对事故、延误和容量的影响 | Pilot steering group / 试点 steering group |
| Data engineering / 数据工程 | Reliable data pipelines and source ownership / 稳定数据 pipeline 和数据源 ownership | Medium | Source schema, refresh SLA, data quality rules / 源 schema、刷新 SLA、数据质量规则 | Data readiness workstream / 数据准备工作流 |
| Data science / ML / 数据科学与机器学习 | Model performance and monitoring / 模型表现和监控 | Medium | Feature pipeline, validation metrics, drift signals / 特征 pipeline、验证指标、漂移信号 | Model governance forum / 模型治理会议 |
| Safety and compliance / 安全与合规 | Safe use of decision-support outputs / 安全使用决策支持输出 | High | Limitations, controls, human approval, audit trail / 局限性、控制、人工审批、审计轨迹 | Formal approval gate / 正式审批节点 |
| Senior sponsor / 项目负责人 | Business case and delivery confidence / 业务价值和交付信心 | High | Benefits, risks, timeline, go/no-go recommendation / 收益、风险、时间线、上线建议 | Milestone updates / 里程碑汇报 |
| Frontline technicians / 一线维修人员 | Practical maintenance work and trust in outputs / 实际维修工作和对输出的信任 | Medium | Work order context and feedback route / 工单背景和反馈路径 | Training and feedback sessions / 培训和反馈会 |

## Communication Rhythm / 沟通节奏

- Steering update: every two weeks. / Steering update 每两周一次。
- Technical working group: weekly. / 技术工作组每周一次。
- Planner UAT: at each dashboard release candidate. / 每个 dashboard release candidate 进行计划人员 UAT。
- Post-pilot review: after four weeks of shadow-mode operation. / Shadow-mode 运行四周后进行试点复盘。
