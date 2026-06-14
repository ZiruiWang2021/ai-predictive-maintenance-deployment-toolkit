# Data Directory / 数据目录

This project keeps raw, external, and processed data out of git by default.

本项目默认不把 raw、external 和 processed 数据提交到 git。

- `external/`: manually downloaded public benchmark files, such as NASA C-MAPSS ZIPs. / 手动下载的公开基准数据，例如 NASA C-MAPSS ZIP。
- `raw/`: generated or prepared asset-cycle sensor logs. / 生成或准备后的设备-周期级传感器日志。
- `processed/`: feature tables, validation predictions, and latest fleet scores. / 特征表、验证预测和最新设备评分结果。

Run / 运行：

```bash
python scripts/train_model.py --generate-sample --n-units 90
```

to generate the demo data and dashboard inputs.

即可生成 demo 数据和 dashboard 输入。
