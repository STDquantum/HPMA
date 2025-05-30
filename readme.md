包名：

```
com.netease.harrypotter
```

入口：

```
com.netease.ntunisdk.external.protocol.ProtocolLauncher
```

找 pid：

```
adb shell ps | findstr harrypotter
```

结果 be like 

```
u0_a397      31049  6337   29009556 1341328 0                  0 S com.netease.harrypotter
u0_a397      31699  6337    7183544 105536 0                   0 S com.netease.harrypotter:PushService
```

其中 31049 就是 pid，在连接 frida 的时候用这个

```
frida -U -l harrypotter_ui.js -p 31049
```

或者这样：

```
frida -U -l harrypotter_ui.js -f com.netease.harrypotter
```

直接使用 frida 启动它。