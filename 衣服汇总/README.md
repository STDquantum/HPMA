# HPMA 服装图鉴

## 打开方式

不要直接双击 `index.html`。浏览器会阻止网页通过 `file://` 读取同目录的 JSON 数据。

1. 双击 `打开图鉴.bat`。
2. 脚本会自动挑选空闲端口并打开图鉴，不会占用固定端口。
3. 使用完毕后，在黑色命令窗口按 `Ctrl+C` 停止本地服务。

需要安装 Python（Windows 通常可通过 `py` 命令启动）。`index.html`、`hpma_database.json` 和 `HPMA_database.assets` 文件夹请保持在同一目录。

## 更新数据

编辑 `HPMA_database.md` 后，在此目录运行：

```powershell
python generate_json.py
```

生成的 JSON 会由页面读取，图片资源位于 `HPMA_database.assets`。
