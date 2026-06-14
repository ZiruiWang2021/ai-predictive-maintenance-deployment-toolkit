# Streamlit Deployment Notes / Streamlit 部署说明

## Streamlit Community Cloud / Streamlit Community Cloud

1. Push this repository to GitHub. / 将仓库推送到 GitHub。
2. Create a new Streamlit app from the repository. / 基于该仓库创建新的 Streamlit app。
3. Set the main file path to `app/streamlit_app.py`. / 将 main file path 设置为 `app/streamlit_app.py`。
4. Add a setup command in the app settings if needed. / 如有需要，在 app 设置中添加 setup command：

```bash
python scripts/train_model.py --generate-sample --n-units 90
```

For production-style hosting, pre-generate model artifacts in CI/CD or mount a managed object store containing approved model and scoring outputs.

如果采用更接近生产的托管方式，可以在 CI/CD 中预生成模型产物，或挂载包含已批准模型和评分输出的对象存储。

## Environment Variables / 环境变量

No secrets are required for the offline demo.

离线 demo 不需要 secrets。

A production deployment should add:

生产部署通常需要增加：

- approved data source connection / 已批准的数据源连接；
- model registry URI / 模型注册表 URI；
- monitoring sink or telemetry endpoint / 监控或 telemetry endpoint；
- incident contact list / 事件联系人列表。
