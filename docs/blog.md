# Building an AI Predictive Maintenance Deployment Toolkit / 构建 AI 预测性维护部署工具包

## Problem / 问题

Maintenance teams often have large volumes of equipment sensor data, but the decision they need to make is very practical: which assets should be inspected first, and which predictions are reliable enough to support action?

维护团队通常拥有大量设备传感器数据，但真正要解决的问题很直接：哪些设备应该优先检查？哪些预测结果足够可靠，可以支撑维护行动？

A predictive maintenance model can estimate Remaining Useful Life (RUL), but a useful deployment needs more than a model notebook. It needs a repeatable data pipeline, a dashboard, and a clear operating plan.

预测性维护模型可以估计 Remaining Useful Life（RUL，剩余可用寿命），但落地应用不能只停留在 notebook。它还需要可复现的数据 pipeline、可理解的 dashboard，以及清晰的运行和治理流程。

This project builds a deployment-oriented toolkit for a Network Rail-style maintenance scenario: a 36-week AI predictive maintenance pilot covering 100 railway infrastructure assets, predicting RUL from sensor histories, highlighting high-risk assets, and showing how the system could move from pilot to operational decision support.

本项目构建了一个面向部署的工具包，场景类似 Network Rail 的资产维护：设计一个为期 36 周、覆盖 100 个铁路基础设施资产的 AI 预测性维护试点，根据传感器历史预测 RUL，识别高风险设备，并展示系统如何从试点走向运维决策支持。

## Why It Matters / 为什么重要

Unplanned failures can cause service disruption, safety risk, emergency repair cost, and poor customer experience. Replacing assets too early is also expensive. Predictive maintenance sits between these two extremes: it helps teams intervene earlier, but only when the evidence is strong enough.

设备突发故障可能带来服务中断、安全风险、紧急维修成本和用户体验下降；但过早更换设备也会造成资源浪费。预测性维护的价值就在于：在证据足够强时提前干预，而不是盲目保守或盲目冒险。

For AI projects, the biggest challenge is often not model training. It is adoption. Maintenance planners need clear recommendations, asset engineers need to trust the assumptions, and project sponsors need visibility into delivery risk.

对 AI 项目来说，难点往往不只是训练模型，而是让模型被业务流程真正使用。维护计划人员需要清晰建议，资产工程师需要理解假设，项目负责人需要看到交付风险和上线条件。

## My Approach / 方法

I designed the repo as both a technical demo and a deployment pack:

我把这个仓库设计成“技术 demo + 部署包”的形式：

1. Generate or prepare CMAPSS-style run-to-failure sensor data. / 生成或准备 CMAPSS 风格的 run-to-failure 传感器数据。
2. Clean and label the data at asset-cycle level. / 按设备和运行周期清洗数据并生成标签。
3. Build rolling-window time-series features that capture degradation trends. / 构建 rolling-window 时间序列特征，捕捉退化趋势。
4. Train a transparent RUL regression model. / 训练透明的 RUL 回归模型。
5. Score the latest record for each asset and assign risk tiers. / 对每个设备最新记录打分，并划分风险等级。
6. Present the results in a Streamlit dashboard. / 用 Streamlit dashboard 展示结果。
7. Add delivery artefacts: 36-week pilot plan, budget, WBS, risk register, communication plan, go/no-go checklist, stakeholder map, deployment runbook, and model card. / 增加 36 周试点计划、预算、WBS、风险登记册、沟通计划、Go/No-Go checklist、stakeholder map、部署 runbook 和 model card。
8. Add a RAG and Agent layer that retrieves maintenance guidance, fault case notes, and delivery governance documents before generating a cited maintenance recommendation. / 增加 RAG 和 Agent 层，在生成带引用来源的维护建议前检索维护说明、故障案例和项目交付资料。

## Technical Implementation / 技术实现

The model pipeline is implemented in `src/pdm_toolkit/`:

核心 pipeline 位于 `src/pdm_toolkit/`：

- `data.py` generates or loads sensor logs, handles cleaning, and adds RUL labels.
- `data.py` 负责生成或加载传感器日志、清洗数据并添加 RUL 标签。
- `features.py` builds rolling-window time-series features, including rolling means, rolling standard deviations, deltas, and engineering proxy features.
- `features.py` 构建 rolling-window 时间序列特征，包括滚动均值、滚动标准差、变化量和工程代理特征。
- `model.py` trains a ridge regression model using `numpy`, keeping the core algorithm transparent.
- `model.py` 使用 `numpy` 训练 ridge regression，保持核心算法透明可读。
- `pipeline.py` orchestrates data generation, training, evaluation, and output creation.
- `pipeline.py` 串联数据生成、模型训练、评估和输出生成。
- `scoring.py` converts predicted RUL into operational risk tiers and maintenance actions.
- `scoring.py` 将 RUL 预测转化为风险等级和维护建议。

The dashboard in `app/streamlit_app.py` reads generated CSV outputs rather than raw model internals. This mirrors a practical deployment pattern: scoring jobs publish approved outputs, and the dashboard focuses on decision support.

`app/streamlit_app.py` 中的 dashboard 读取生成后的 CSV 输出，而不是直接依赖模型内部对象。这更接近真实部署方式：评分任务产出经过批准的结果，dashboard 专注于支持决策。

## Results / Demo / 结果与演示

The demo produces:

这个 demo 会生成：

- a fleet-level intervention queue / 设备级维护干预队列；
- high, medium, and low risk asset tiers / 高、中、低风险设备分层；
- RUL prediction intervals / RUL 预测区间；
- validation metrics including MAE, RMSE, bias, precision, and recall / 包括 MAE、RMSE、bias、precision、recall 在内的验证指标；
- a dashboard preview image for GitHub readers / 用于 GitHub 展示的 dashboard 预览图。

Example output / 示例输出：

```text
unit_id=1, predicted_rul=22.6, failure_risk=high
action=Plan intervention in next maintenance window
```

Run locally / 本地运行：

```bash
pip install -r requirements.txt
python scripts/train_model.py --generate-sample --n-units 90
streamlit run app/streamlit_app.py
```

## Limitations / 局限性

The included demo data is synthetic, so it should not be used as operational evidence. The model is intentionally simple and transparent; production environments may need richer sequence models, calibrated uncertainty, drift monitoring, and tighter asset-domain validation.

内置 demo 数据是 synthetic data，不能作为真实运维证据。当前模型故意保持简单透明；生产环境可能需要更强的序列模型、校准后的不确定性估计、漂移监控，以及更严格的资产领域验证。

The RUL labelling approach assumes complete run-to-failure histories. In real rail or industrial settings, asset histories can be censored by inspections, repairs, component swaps, or data gaps.

RUL 标签生成假设存在完整的 run-to-failure 历史。但在真实铁路或工业场景中，资产历史可能会被检查、维修、部件更换或数据缺口打断。

## What I Learned / 复盘

The most valuable part of a predictive maintenance project is connecting model outputs to operational decisions. A model score is only useful if planners understand the next action, asset engineers understand the assumptions, and owners can monitor whether the system remains reliable.

预测性维护项目最有价值的部分，是把模型输出连接到真实决策。一个模型分数只有在维护人员知道下一步怎么做、资产工程师理解假设、系统负责人能持续监控可靠性时，才真正有用。

This project helped me frame AI delivery as an end-to-end system: data readiness, modelling, dashboard design, stakeholder adoption, governance, and post-launch monitoring.

这个项目也让我把 AI 交付理解成一个端到端系统：数据就绪、建模、dashboard 设计、利益相关方协同、治理控制，以及上线后的持续监控。

## GitHub Link / GitHub 链接

```text
https://github.com/ZiruiWang2021/ai-predictive-maintenance-deployment-toolkit
```
