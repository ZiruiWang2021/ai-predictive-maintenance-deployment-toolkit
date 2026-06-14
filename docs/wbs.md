# Work Breakdown Structure / 工作分解结构

| Phase / 阶段 | Work Package / 工作包 | Key Deliverables / 关键交付物 | Owner / 负责人 | Exit Criteria / 退出标准 |
|---|---|---|---|---|
| 1. Initiation / 启动 | Business framing / 业务定义 | Problem statement, success metrics, stakeholder map / 问题陈述、成功指标、利益相关方地图 | Product / PM | Maintenance use case and target assets agreed / 维护场景和目标资产达成一致 |
| 2. Data readiness / 数据准备 | Source access / 数据源接入 | Sensor history, maintenance events, asset metadata / 传感器历史、维护事件、资产元数据 | Data engineer | Data access approved and profiled / 数据访问获批并完成 profiling |
| 2. Data readiness / 数据准备 | Data quality / 数据质量 | Missingness, sampling, label quality, leakage checks / 缺失率、采样、标签质量、泄漏检查 | Data scientist | Data quality report accepted / 数据质量报告通过 |
| 3. Modelling / 建模 | Feature engineering / 特征工程 | Reusable feature pipeline and labelled training table / 可复用特征 pipeline 和带标签训练表 | Data scientist | Features reproducible from source data / 特征可从源数据复现 |
| 3. Modelling / 建模 | Model training / 模型训练 | RUL model, validation metrics, model card / RUL 模型、验证指标、model card | Data scientist | Metrics meet pilot threshold / 指标达到试点阈值 |
| 4. Dashboard / 仪表盘 | Planner workflow / 维护计划流程 | Streamlit monitoring dashboard and intervention queue / 监控 dashboard 和干预队列 | Analytics engineer | Users can interpret outputs / 用户能理解输出 |
| 5. Deployment / 部署 | Pilot release / 试点发布 | Runbook, go/no-go checklist, rollback plan / Runbook、go/no-go checklist、回滚计划 | PM / ML engineer | Go-live decision recorded / 上线决策已记录 |
| 6. Adoption / 采用 | Training and handover / 培训和交接 | User guide, ownership model, feedback loop / 用户指南、ownership 模型、反馈闭环 | PM | Users trained and support route live / 用户完成培训且支持路径可用 |
| 7. Monitoring / 监控 | Post-release controls / 上线后控制 | Data drift, model performance, incident review cadence / 数据漂移、模型表现、事件复盘节奏 | ML engineer | Monitoring thresholds and owners active / 监控阈值和负责人已生效 |

## Milestone View / 里程碑

| Milestone / 里程碑 | Target Outcome / 目标结果 |
|---|---|
| M1 Discovery complete / 发现阶段完成 | Use case, asset scope, and data sources confirmed / 场景、资产范围和数据源确认 |
| M2 Data baseline complete / 数据基线完成 | Training dataset prepared and quality risks logged / 训练数据准备完毕，质量风险已记录 |
| M3 Model pilot ready / 模型试点就绪 | RUL model validated against agreed metrics / RUL 模型通过约定指标验证 |
| M4 Dashboard accepted / Dashboard 验收 | Planner-facing dashboard tested with sample users / 面向计划人员的 dashboard 完成测试 |
| M5 Go/no-go approved / Go/No-Go 通过 | Governance checklist completed / 治理 checklist 完成 |
| M6 Pilot live / 试点上线 | Monitored deployment with human override and rollback / 带监控、人工 override 和回滚机制的试点运行 |
