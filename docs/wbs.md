# Work Breakdown Structure / 工作分解结构

## Pilot Assumptions / 试点假设

- Scenario: Network Rail-style AI predictive maintenance pilot for railway infrastructure assets. / 场景：类似 Network Rail 的铁路基础设施资产 AI 预测性维护试点。
- Duration: 36 weeks from discovery to monitored pilot handover. / 周期：36 周，从发现阶段到受控试点交接。
- Asset scope: 100 monitored infrastructure assets for the pilot cohort. / 资产范围：试点覆盖 100 个被监测的铁路基础设施资产。
- Delivery scope: project scope, WBS, schedule, budget, risk register, communication plan, go/no-go gates, dashboard, RUL model, and RAG/Agent decision-support workflow. / 交付范围：项目范围、任务拆解、进度计划、预算、风险登记表、沟通计划、go/no-go 节点、dashboard、RUL 模型和 RAG/Agent 决策支持流程。

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

## 36-Week Schedule / 36 周进度计划

| Weeks / 周期 | Workstream / 工作流 | Main Output / 主要产出 |
|---|---|---|
| 1-4 | Initiation and scope / 启动与范围定义 | 100-asset pilot scope, success metrics, stakeholder map / 100 资产试点范围、成功指标、利益相关方地图 |
| 5-10 | Data readiness / 数据准备 | Sensor data profile, quality report, RUL labels / 传感器数据画像、质量报告、RUL 标签 |
| 11-16 | Feature engineering and modelling / 特征工程与建模 | Rolling-window time-series features, RUL model, validation metrics / rolling-window 时间序列特征、RUL 模型、验证指标 |
| 17-22 | Dashboard and API / Dashboard 与 API | Streamlit dashboard, FastAPI endpoints, sample inputs and outputs / Streamlit 看板、FastAPI 接口、示例输入输出 |
| 23-27 | RAG and Agent workflow / RAG 与 Agent 工作流 | Knowledge base, retrieval, Agent tool workflow, cited maintenance report / 知识库、检索、Agent 工具流程、带引用维护报告 |
| 28-31 | UAT and governance / 用户验收与治理 | Planner UAT, risk register review, go/no-go checklist / 计划人员 UAT、风险登记复核、go/no-go checklist |
| 32-36 | Shadow pilot and handover / 影子试点与交接 | Monitoring plan, communication rhythm, pilot handover recommendation / 监控计划、沟通节奏、试点交接建议 |

## Budget Estimate / 预算估算

| Cost Area / 成本项 | Estimate / 估算 | Rationale / 依据 |
|---|---:|---|
| Data preparation and engineering / 数据准备与工程 | GBP 35,000 | Source profiling, data cleaning, feature pipeline / 数据画像、清洗、特征 pipeline |
| Model development and validation / 模型开发与验证 | GBP 30,000 | RUL modelling, validation, model card / RUL 建模、验证、model card |
| Dashboard and API build / Dashboard 与 API 开发 | GBP 25,000 | Streamlit dashboard, FastAPI endpoints / Streamlit 看板、FastAPI 接口 |
| RAG and Agent workflow / RAG 与 Agent 工作流 | GBP 20,000 | Knowledge base, retrieval, prompt templates, Agent tools / 知识库、检索、prompt templates、Agent 工具 |
| UAT, training, and change management / UAT、培训与变更管理 | GBP 15,000 | Planner UAT, training, adoption support / 计划人员 UAT、培训、采用支持 |
| Contingency / 预备金 | GBP 15,000 | Delivery and data quality uncertainty / 交付与数据质量不确定性 |
| **Total / 合计** | **GBP 140,000** | 36-week pilot estimate / 36 周试点估算 |

## Milestone View / 里程碑

| Milestone / 里程碑 | Target Outcome / 目标结果 |
|---|---|
| M1 Discovery complete / 发现阶段完成 | Use case, asset scope, and data sources confirmed / 场景、资产范围和数据源确认 |
| M2 Data baseline complete / 数据基线完成 | Training dataset prepared and quality risks logged / 训练数据准备完毕，质量风险已记录 |
| M3 Model pilot ready / 模型试点就绪 | RUL model validated against agreed metrics / RUL 模型通过约定指标验证 |
| M4 Dashboard accepted / Dashboard 验收 | Planner-facing dashboard tested with sample users / 面向计划人员的 dashboard 完成测试 |
| M5 Go/no-go approved / Go/No-Go 通过 | Governance checklist completed / 治理 checklist 完成 |
| M6 Pilot live / 试点上线 | Monitored deployment with human override and rollback / 带监控、人工 override 和回滚机制的试点运行 |
