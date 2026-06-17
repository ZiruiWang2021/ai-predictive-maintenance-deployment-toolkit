# 36-Week Predictive Maintenance Pilot Deployment Plan / 36 周预测性维护试点部署方案

## Scenario / 场景

This plan frames the project as a Network Rail-style AI predictive maintenance pilot for 100 railway infrastructure assets. The pilot is a decision-support deployment, not an autonomous maintenance scheduler.

本方案将项目设定为类似 Network Rail 的 AI 预测性维护试点，覆盖 100 个铁路基础设施资产。该试点用于决策支持，不是自动化维护调度系统。

## Scope / 项目范围

In scope:

- 100 monitored railway infrastructure assets / 100 个被监测的铁路基础设施资产；
- CMAPSS-style sensor data preparation and RUL modelling / 类 C-MAPSS 传感器数据准备和 RUL 建模；
- Streamlit asset health dashboard / Streamlit 资产健康看板；
- FastAPI backend for RAG and Agent workflows / 支持 RAG 和 Agent 的 FastAPI 后端；
- RAG knowledge base for maintenance guidance, fault case notes, and project delivery documents / 覆盖维护说明、故障案例和项目交付资料的 RAG 知识库；
- governance artefacts: WBS, schedule, budget, risk register, communication plan, go/no-go checklist, stakeholder map, runbook, and model card / 治理交付物：WBS、进度、预算、风险登记表、沟通计划、go/no-go checklist、stakeholder map、runbook 和 model card。

Out of scope:

- live control of maintenance work orders / 直接控制维护工单；
- replacement of OEM manuals or safety procedures / 替代 OEM 手册或安全流程；
- production integration with real Network Rail systems / 与真实 Network Rail 系统生产集成。

## Timeline / 进度计划

| Weeks / 周期 | Phase / 阶段 | Deliverables / 交付物 |
|---|---|---|
| 1-4 | Discovery and initiation / 发现与启动 | Business problem, target assets, success metrics, stakeholder map / 业务问题、目标资产、成功指标、利益相关方地图 |
| 5-10 | Data readiness / 数据准备 | Data profile, quality checks, RUL labels, leakage review / 数据画像、质量检查、RUL 标签、泄漏检查 |
| 11-16 | Modelling / 建模 | Rolling-window time-series features, RUL model, validation metrics / rolling-window 时间序列特征、RUL 模型、验证指标 |
| 17-22 | Dashboard and API / 看板与 API | Streamlit dashboard, FastAPI endpoints, sample requests / Streamlit 看板、FastAPI 接口、示例请求 |
| 23-27 | RAG and Agent / RAG 与 Agent | Knowledge base, retrieval, Agent tools, cited report output / 知识库、检索、Agent 工具、带引用报告 |
| 28-31 | UAT and controls / UAT 与控制 | Planner UAT, risk register, go/no-go checklist, communication plan / 计划人员 UAT、风险登记表、go/no-go checklist、沟通计划 |
| 32-36 | Shadow pilot and handover / 影子试点与交接 | Monitoring plan, rollback route, handover recommendation / 监控计划、回滚路径、交接建议 |

## Budget / 预算

| Category / 类别 | Estimate / 估算 |
|---|---:|
| Data preparation and feature engineering / 数据准备与特征工程 | GBP 35,000 |
| RUL modelling and validation / RUL 建模与验证 | GBP 30,000 |
| Dashboard and FastAPI build / Dashboard 与 FastAPI 开发 | GBP 25,000 |
| RAG and Agent workflow / RAG 与 Agent 工作流 | GBP 20,000 |
| UAT, training, and change management / UAT、培训与变更管理 | GBP 15,000 |
| Contingency / 预备金 | GBP 15,000 |
| **Total / 合计** | **GBP 140,000** |

## Go/No-Go Gates / Go/No-Go 节点

- Gate 1, week 4: scope, target assets, and stakeholder ownership confirmed. / 第 4 周：范围、目标资产和 stakeholder ownership 确认。
- Gate 2, week 10: data quality is acceptable for modelling. / 第 10 周：数据质量达到建模要求。
- Gate 3, week 16: RUL model meets pilot validation threshold. / 第 16 周：RUL 模型达到试点验证阈值。
- Gate 4, week 27: RAG/Agent output includes sources, next action, and limitations. / 第 27 周：RAG/Agent 输出包含来源、下一步行动和局限性。
- Gate 5, week 31: UAT, risk controls, communication plan, and rollback path approved. / 第 31 周：UAT、风险控制、沟通计划和回滚路径通过。

## Risk Closure / 风险闭环

Each risk in `docs/risk_register.md` should have an owner, mitigation, review cadence, and closure condition. High-severity risks remain open until reviewed at a go/no-go gate.

`docs/risk_register.md` 中的每个风险都应有负责人、缓解措施、复盘节奏和关闭条件。高严重性风险必须在 go/no-go 节点复核后才能关闭。
