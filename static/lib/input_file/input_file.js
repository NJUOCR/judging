
function upfile() {
    const url = "/media-upload";
    let formdata = new FormData();
    let files = document.getElementById('uploadMedia').files;
    let filenames = []
    for(let i = 0 ; i<files.length;i++){
        let temp = files[i];
        let filename = temp.name;
        formdata.append(filename, temp);
        filenames.push(filename);
    }
    formdata.append("category", "测试案号123/查找被害人，确认死者身份/死亡时间/视听材料/图片集1");
    formdata.append("description", "这是关于媒体1文件的描述，这个描述可以很长");

    // todo #解释 文件名可以在后端得到
    // formdata.append("filenames", filenames);
    fetch(url, {
        method: "post",
        body: formdata
    }).then(function (response) {
        console.log(response)
        if (response.status !== 200) {
            console.log("上传失败，状态码为：" + response.status);
            return;
        }
        //检查响应文本
        response.json().then(function (data) {
            console.log(data);
        });
    }).catch(function (err) {
        console.log("Fetch错误:" + err);
    });
}

function validate() {
    let files = document.getElementById("uploadMedia").files;
    let pic = false;
    let ved = false;
    let aud = false;
    let other = false;
    let filename = "";
    for(let i = 0; i<files.length;i++){
        let tempStr = files[i].name;
        if(picture(tempStr.split(".")[1])){
            pic = true;
            filename = filename + tempStr + "  |  "
        }else if(video(tempStr.split(".")[1])){
            if(files.length===1){
                ved = true;
                filename = filename + tempStr + "  |  "
            }else {
                break;
            }
        }else if(audio(tempStr.split(".")[1])){
            if(files.length===1){
                aud = true;
                filename = filename + tempStr + "  |  "
            }else {
                break;
            }
        }else {
            other = true;
            break;
        }
        //alert(tempStr);
    }
    if((pic&&!ved&&!aud&&!other)||(!pic&&ved&&!aud&&!other)||(!pic&&!ved&&aud&&!other)){
        document.getElementById("validateLabel").innerHTML = filename;
        document.getElementById("uploadButton").style = "display:block";
    }else {
        document.getElementById("validateLabel").innerHTML = "上传错误，请重新上传";
        document.getElementById("uploadButton").style = "display:none";
    }

}

function picture(str){
    let s = str.toString().toLocaleLowerCase()
    if (s === "jpg"||s === "png" || s === "bmp" || s === "svg"){
        return true
    }
}

function video(str){
    let s = str.toString().toLocaleLowerCase()
    if(s === "mpeg" || s ==="avi" || s === "mov" || s === "asf" || s === "rmvb" ||
        s === "mpg" || s === "mp4"){
        return true
    }
}

function audio(str){
    let s = str.toString().toLocaleLowerCase()
    if(s === "mp3" || s === "midi" || s === "wma"){
        return true
    }
}