# HPMA 资源与脚本整理

这是《哈利波特：魔法觉醒》相关的图片资源、网页卡牌整理、ADB 自动化和 Frida 调试资料。

## 网页入口

站点首页：<https://stdquantum.github.io/HPMA/>（根目录 `index.html`，三个大按键）

| 入口 | 直接地址 | 内容 |
|---|---|---|
| 服装图鉴 | <https://stdquantum.github.io/HPMA/衣服汇总/> | 205 套服装，多立绘、类型筛选、按上线日期排序 |
| 卡牌收集 | <https://stdquantum.github.io/HPMA/卡牌网页整理/卡牌合成.html> | 141 张卡牌，卡面 + 卡框 + 魔力值合成 |
| 衣柜查看器 | <https://stdquantum.github.io/HPMA/wardrobe-demo/gallery_pc.html> | 3D 换装，69 个模型、324 段动画、8 档肤色 |

三页都只读同目录的 json/图片，路径全是相对的，所以本地起个服务也能看
（`wardrobe-demo\启动.bat` 是自带的一个小服务，双击即可）。

## 目录说明

- 官方下载卡牌：官方卡牌资源的分类图片，包含伙伴卡、召唤卡、咒语卡。图片文件名和资源编号保持原样。
- 卡牌编号下载：按网易资源编号批量下载卡牌图片，包含下载编号卡牌.py、result 和下载结果比对.ipynb。
- 卡牌网页整理：使用 Playwright 获取藏宝阁账号卡牌内容，在内存中解析卡牌信息，下载素材并生成卡牌合成.html。
- Frida调试：获取当前 Android Activity、观察隐藏进程的 Frida 脚本。
- 禁林熟练度：使用 ADB 和 OpenCV 识别按钮、循环执行禁林熟练度操作。
- 舞会与安卓自动化：视频标注、坐标转换、标注合并以及 ADB 回放脚本和数据。
- 其它零散目录：早期视频、图片和预留资源（如果目录仍存在）。

## Python 环境

Notebook 和 Python 脚本统一使用 conda 环境 env3.10：

    conda activate env3.10

卡牌网页整理还需要 Playwright；首次使用时在 env3.10 中安装：

    pip install playwright requests pypinyin
    playwright install chromium

## Frida 基本信息

游戏包名：

    com.netease.harrypotter

查看进程：

    adb shell ps | findstr harrypotter

附加到进程：

    frida -U -l Frida调试\获取当前界面.js -p 进程号

直接启动：

    frida -U -l Frida调试\获取当前界面.js -f com.netease.harrypotter

魔杖、猫头鹰等模型资源记录在游戏的 items.npk 中。
