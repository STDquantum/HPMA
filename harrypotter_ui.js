Java.perform(function() {
    // 获取 ActivityThread 实例
    var ActivityThread = Java.use('android.app.ActivityThread');
    var currentActivityThread = ActivityThread.currentActivityThread();
    
    // 获取 mActivities 字段（一个 ArrayMap）
    var mActivities = currentActivityThread.mActivities.value;
    
    // 遍历 mActivities 找到最顶层的 Activity
    var iterator = mActivities.values().iterator();
    while (iterator.hasNext()) {
        var activityRecord = iterator.next();
        var activity = activityRecord.activity.value;
        if (activity != null) {
            console.log("Current Activity:", activity.getClass().getName());
            break; // 只取第一个（通常是当前显示的 Activity）
        }
    }
});