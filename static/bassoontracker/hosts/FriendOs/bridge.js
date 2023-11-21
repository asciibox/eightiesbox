var HostBridge = function(){
    var me = {};
    var friendCallBackId;

    var isFriendUp = ((typeof Application === "object") && Application.initFriendVR);
    if (isFriendUp) console.log("running on FriendUP");

    // FriendOS maps local urls to filesystem reads, urls paramater won't work
    me.useUrlParams = false;
    
    //FriendOS has its own Dropbox integration
    me.useDropbox = false;

    //FriendOS has its own Menu system
    me.showInternalMenu = false;

    //there something weird with "importscripts" in workers with the Friend paths ... still have to figure it out
    me.useWebWorkers = false;
    
    me.getBaseUrl = function(){
        // use a function - progDir is not available yet at load time
        return Application.progDir
    };
    
    me.getRemoteUrl = function(){
        return "https://www.stef.be/bassoontracker/"
    };
    
    me.init = function(){
        if (!isFriendUp) return;
        Application.receiveMessage = function(msg){
            if (msg.type === 'bassoontracker'){
                // bloody annoying, right, that Friend keeps stealing focus?
                window.focus();
                switch(msg.command){
                    case 'setMessageHandler':
                        friendCallBackId = msg.callbackId;
                        break;
                    case 'loadFile':
                        var file = msg.files[0];
                        if (file && file.Path){
                            var url = getFriendFileUrl(file);
                            me.initialFile = url;
                            if (typeof SETTINGS === "object") SETTINGS.loadInitialFile = false;
                            if (typeof HOST === "object") HOST.initialFile = url;
                            console.log("loading file from FriendOS",url);
                            Tracker.load(url,false,function(){});
                        }
                        break;
                    case 'getFileName':
                        var filename = Tracker.getFileName();
                        if (msg.callbackId){
                            console.warn("setting callback");
                            me.sendMessage({
                                callbackId: msg.callbackId,
                                command: "message",
                                message: filename
                            });
                        }
                        break;
                    case 'saveFile':
                        var filename = msg.files.split("/").pop();
                        Editor.save(filename,function(blob){
                            UI.setStatus("Saving File to FriendOS",true);
                            console.log("Saving File to FriendOS",msg.files);
                            var url = "/system.library/file/upload/?authid=" + Application.authId  + "&path=" + msg.files;

                            var formData = new FormData();
                            formData.append("file",blob,"");
                            FetchService.sendBinary(url,formData,function(data){
                                UI.setStatus(""); 
                                console.log("result from upload: " + data)
                            });
                        });
                        break;
                    default:
                        var command = COMMAND[msg.command];
                        if (command){
                            App.doCommand(command);
                        }else{
                            console.warn("Unhandled message: " + msg);
                        }
                }
            }else{
                // message from the OS
                //console.log("got message",msg);
                switch (msg.command){
                    case "drop":
                        var data = msg.data || [];
                        var file = data[0];
                        var url = getFriendFileUrl(file);
                        Tracker.load(url,false,function(){});
                }

            }
        };
	    
    };
    
    me.sendMessage = function(msg){
        if (friendCallBackId){
            if (typeof msg === "string") msg = {command: "message", message: msg};
            msg = msg || {};
            msg.type = "callback";
            msg.callback = friendCallBackId;
            Application.sendMessage(msg)
        }else{
            console.warn("can't send message, friendCallBackId not setup");
        }
    };
    
    me.getVersionNumber = function(){
       return Application.bsn_versionNumber;  
    };

    me.getBuildNumber = function(){
        return Application.bsn_buildNumber;
    };

    function getFriendFileUrl(file){
        return  "/system.library/file/read?authid=" + Application.authId  + "&path=" + file.Path + "&mode=rs";
    }
    
    return me;
}();