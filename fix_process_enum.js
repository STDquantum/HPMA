// 脚本：fix_process_enum.js
Interceptor.attach(Module.findExportByName(null, "readdir"), {
    onLeave: function(retval) {
        var dirEntry = retval;
        if (dirEntry != 0) {
            var name = dirEntry.add(0x11).readPointer().readCString();
            console.log(name);
            if (name.includes("harrypotter")) {
                console.log("[*] Found hidden process:", name);
            }
        }
    }
});