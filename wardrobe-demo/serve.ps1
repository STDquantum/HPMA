# 本地静态服务器（PowerShell 版）
# 用 TCP 自己发 HTTP 响应：不需要管理员权限，也不用 netsh 注册 URL，Windows 自带就能跑。
# 由 启动.bat 调用。

$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Split-Path -Parent $MyInvocation.MyCommand.Path))
$listener = $null
$port = 0

for ($p = 8000; $p -le 8029; $p++) {
    try {
        $t = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Loopback, $p)
        $t.Start()
        $listener = $t
        $port = $p
        break
    } catch {
        if ($t) { try { $t.Stop() } catch {} }
    }
}

if (-not $listener) {
    Write-Host "8000-8029 全被占了，关掉一个程序再试。" -ForegroundColor Red
    exit 1
}

$url = "http://127.0.0.1:$port/gallery_pc.html"
Write-Host "服务已启动: $url" -ForegroundColor Green
Write-Host "目录: $root"
Write-Host "关掉这个窗口就停止。"
Write-Host ""
Start-Process $url | Out-Null

$mime = @{
    '.html' = 'text/html; charset=utf-8'
    '.js'   = 'text/javascript; charset=utf-8'
    '.json' = 'application/json; charset=utf-8'
    '.css'  = 'text/css; charset=utf-8'
    '.glb'  = 'model/gltf-binary'
    '.png'  = 'image/png'
    '.jpg'  = 'image/jpeg'
    '.webp' = 'image/webp'
    '.bin'  = 'application/octet-stream'
    '.md'   = 'text/plain; charset=utf-8'
    '.txt'  = 'text/plain; charset=utf-8'
    '.ico'  = 'image/x-icon'
}

while ($true) {
    $client = $listener.AcceptTcpClient()
    try {
        $client.ReceiveTimeout = 3000
        $stream = $client.GetStream()
        $reader = New-Object IO.StreamReader($stream, [Text.Encoding]::ASCII)
        $line = $reader.ReadLine()
        if (-not $line) { continue }
        while ($true) {
            $h = $reader.ReadLine()
            if ($null -eq $h -or $h -eq '') { break }
        }
        $parts = $line.Split(' ')
        if ($parts.Length -lt 2) { continue }
        $method = $parts[0]
        $rawPath = [Uri]::UnescapeDataString(($parts[1].Split('?')[0]))
        if ([string]::IsNullOrWhiteSpace($rawPath) -or $rawPath -eq '/') { $rawPath = '/gallery_pc.html' }
        $rel = ($rawPath.TrimStart('/')) -replace '/', '\'
        $path = [IO.Path]::GetFullPath((Join-Path $root $rel))

        $status = 404
        $type = 'text/plain; charset=utf-8'
        $body = [Text.Encoding]::UTF8.GetBytes('404 Not Found')
        if ($path.StartsWith($root, [StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $path -PathType Leaf)) {
            $body = [IO.File]::ReadAllBytes($path)
            $ext = [IO.Path]::GetExtension($path).ToLower()
            $t2 = $mime[$ext]
            if ($t2) { $type = $t2 } else { $type = 'application/octet-stream' }
            $status = 200
        }

        $verdict = 'OK'
        if ($status -eq 404) { $verdict = 'Not Found' }
        $head = "HTTP/1.1 $status $verdict`r`nContent-Type: $type`r`nContent-Length: $($body.Length)`r`nCache-Control: no-cache`r`nConnection: close`r`n`r`n"
        $hb = [Text.Encoding]::ASCII.GetBytes($head)
        $stream.Write($hb, 0, $hb.Length)
        if ($method -ne 'HEAD') { $stream.Write($body, 0, $body.Length) }
        $stream.Flush()
        if ($status -eq 200) { Write-Host ("{0} {1} {2} KB" -f $method, $rel, [int]($body.Length / 1KB)) }
    } catch {
    } finally {
        try { $client.Close() } catch {}
    }
}