# Deployment Runbook / 部署运行手册

## Purpose / 目的

Deploy the predictive maintenance model as decision support for maintenance planners. The model recommends inspection or intervention priority; it does not automatically defer safety-critical work.

将预测性维护模型部署为维护计划人员的决策支持工具。模型用于推荐检查或干预优先级，不会自动推迟任何安全关键维护工作。

## Pre-Deployment / 部署前检查

1. Confirm asset scope, data sources, and refresh cadence. / 确认资产范围、数据源和刷新频率。
2. Run data quality checks against recent production extracts. / 对最新生产数据抽取结果运行数据质量检查。
3. Train or load the approved model artifact. / 训练或加载已批准的模型产物。
4. Review model card, risk register, and go/no-go checklist. / 复核 model card、risk register 和 go/no-go checklist。
5. Complete planner UAT with representative high, medium, and low risk assets. / 使用高、中、低风险代表性资产完成计划人员 UAT。

## Local Demo Deployment / 本地演示部署

```bash
pip install -r requirements.txt
python scripts/train_model.py --generate-sample --n-units 90
streamlit run app/streamlit_app.py
```

## Container Deployment / 容器部署

```bash
docker build -f deployment/Dockerfile -t predictive-maintenance-toolkit .
docker run -p 8501:8501 predictive-maintenance-toolkit
```

## Production Pattern / 生产部署模式

1. Source systems export sensor readings and asset metadata. / 源系统导出传感器读数和资产元数据。
2. Feature job creates asset-cycle features on a controlled schedule. / 特征任务按受控周期生成设备-周期级特征。
3. Model scoring job writes latest asset predictions and uncertainty bands. / 模型评分任务写入最新设备预测和不确定性区间。
4. Dashboard reads only approved scoring outputs. / Dashboard 只读取经过批准的评分输出。
5. Planner actions and overrides are logged for retraining and audit. / 维护人员的行动和 override 会被记录，用于再训练和审计。

## Monitoring / 监控

| Monitor / 监控项 | Threshold / 阈值 | Action / 响应动作 |
|---|---|---|
| Data freshness / 数据新鲜度 | No successful refresh within expected SLA / 超过 SLA 未成功刷新 | Alert data owner and mark dashboard stale / 通知数据负责人并标记 dashboard 数据过期 |
| Feature drift / 特征漂移 | Any core sensor PSI above agreed threshold / 核心传感器 PSI 超过阈值 | Review asset mix and retraining need / 检查资产分布并评估是否再训练 |
| Prediction drift / 预测漂移 | High-risk count shifts outside expected band / 高风险数量超出预期区间 | Compare with incidents and maintenance context / 对比事故和维护背景 |
| Model performance / 模型表现 | Recall below pilot threshold / Recall 低于试点阈值 | Freeze automated recommendations and retrain / 暂停自动建议并再训练 |
| User feedback / 用户反馈 | Repeated rejected recommendations / 建议反复被拒绝 | Review with planners and asset engineers / 与计划人员和资产工程师复盘 |

## Rollback / 回滚

Rollback means reverting to the previous approved scoring output and marking the dashboard as advisory only. If data quality or model safety is in doubt, maintenance planners should use existing inspection prioritization until the issue is resolved.

回滚意味着恢复到上一版已批准的评分输出，并将 dashboard 标记为 advisory only。如果数据质量或模型安全性存在疑问，维护计划应回到现有检查优先级流程，直到问题解决。
