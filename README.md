# img-to-psd

> Convert images (png/jpg/webp…) into true multi-layer Photoshop files.
> 把海报、详情页等平面图片，还原为同尺寸、中文可编辑的多层 PSD。

依据成品图重新整理出可继续编辑的 Photoshop 工程：背景、人物、商品、图标按内容分层；中文（横排/竖排/倾斜）识别后重建为**原生文字层**；无法可靠识别的文字一律以 ♦️ 占位，不猜测、不补写。

## 快速开始

```bash
pip install -r requirements.txt
python make_psd.py 输出.psd
```

运行后生成 800×600 的三层演示文件（背景-白 / 产品-红圆 / 标签-蓝条），可在 Photoshop 中打开核对图层与命名。依赖组合已在 Python 3.11 / Windows 实测通过。

## 仓库结构

| 文件 | 说明 |
|---|---|
| `README.txt` | 完整操作流程与四层验收规范（项目主文档） |
| `SKILL.md` | Agent 执行规则（技能版） |
| `make_psd.py` | pytoshop 像素图层生成模板 |
| `示例_三层.psd` | `make_psd.py` 的演示输出，可直接下载打开 |
| `requirements.txt` | Python 依赖清单 |
| `LICENSE` | MIT |

## 依赖

pytoshop 1.2.1 · numpy 2.4.3 · Pillow 12.3.0（Python 3.11 验证）

## 三条铁律

1. **尺寸不变** —— PSD 像素宽高必须与源图严格一致，不缩放、不裁剪。
2. **中文原生可编辑** —— 交付真正的 Photoshop 文字对象（T 类型）；像素字、图层名、旁附文案不算完成；旧字擦除并补底，防止改字重影。
3. **不明文字用 ♦️** —— 复核后仍无法识别的字，逐字以 ♦️（U+2666 U+FE0F）占位；字数不明时以单个 ♦️ 表示并注明。

## 能力边界

`make_psd.py` 只是像素图层模板：没有 OCR、自动拆图，也不产生原生文字层。完整的「图片 → 可编辑中文 PSD」流程按 `README.txt` 执行：生成路线优先 Photoshop COM/JSX，备选离线 TySh 写入器，交付前须通过应用内改字验证。单张成品图不保证恢复原工程的字体、矢量路径与图层样式。

## License

MIT
