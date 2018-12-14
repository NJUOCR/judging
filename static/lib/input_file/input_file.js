
function upfile() {
    const url = "http://localhost:5000/media-upload";
    let formdata = new FormData();
    let files = document.getElementById('uploadMedia').files;
    let filenames = []
    for(let i = 0 ; i<files.length;i++){
        let temp = files[i];
        let filename = temp.name;
        formdata.append(filename, temp);
        filenames.push(filename);
    }
    formdata.append("category", "[12,34,56,78,89]");
    formdata.append("filenames", filenames);
    fetch(url, {
        method: "post",
        body: formdata
    }).then(function (response) {
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
    let other = false
    let filename = ""
    for(let i = 0; i<files.length;i++){
        let tempStr = files[i].name;
        if(picture(tempStr.split(".")[1])){
            pic = true;
            filename = filename + tempStr + "  |  "
        }else if(vedio(tempStr.split(".")[1])){
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

function vedio(str){
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