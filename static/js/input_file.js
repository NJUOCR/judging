function upFile(category, description) {
    const url = "/media-upload";
    let formData = new FormData();
    let files = document.getElementById('uploadMedia').files;

    // let filenames = files.map(f => f.name);
    files.forEach((temp) => {
        let filename = temp.name;
        formData.append(filename, temp);
    });

    // todo #tips @杨关 使用map/reduce提高可读性；使用forEach来迭代数组，更优雅。看完后可以删掉这个todo和下方被注释掉的代码
    // for(let i = 0 ; i<files.length;i++){
    //     let temp = files[i];
    //     let filename = temp.name;
    //     formData.append(filename, temp);
    //     filenames.push(filename);
    // }
    formData.append("category", "测试案号123/查找被害人，确认死者身份/死亡时间/视听材料/图片集1");
    formData.append("description", "这是关于媒体1文件的描述，这个描述可以很长");

    // todo #解释 文件名可以在后端得到
    // formdata.append("filenames", filenames);
    fetch(url, {
        method: "post",
        body: formData
    }).then(function (response) {
        // todo @杨关 上传成功后将按钮恢复为disabled, 加上这个属性会让按钮无法点击
        if (response.status !== 200) {
            console.log("上传失败，状态码为：" + response.status);
            return;
        }
        //检查响应文本
        response.json().then(function (data) {
            console.log(data);
        });
    }).catch(function (err) {
        console.error("Fetch错误:" + err);
    });
}

function validate() {
    let files = document.getElementById("uploadMedia").files;
    let image = 0b0001;
    let video = 0b0010;
    let audio = 0b0100;
    let other = 0b1000;

    // todo #tips js可以这样声明一个函数
    let getMediaTypeBits = (suffix) => {
        suffix = suffix.toLowerCase();
        if (suffix === "jpg" || suffix === "png" || suffix === "bmp" || suffix === "svg") {
            return image;
        } else if (suffix === "mpeg" || suffix === "avi" || suffix === "mov" || suffix === "asf" || suffix === "rmvb" || suffix === "mpg" || suffix === "mp4") {
            return video;
        } else if (suffix === "mp3" || suffix === "midi" || suffix === "wma") {
            return audio;
        } else {
            return other;
        }
    };

    // 将files转为数组
    let typeBit = Array.apply(this, files)
        .map(fileObj => getMediaTypeBits(fileObj.name.split('.').pop()))
        .reduce((suffix1, suffix2) => suffix1 | suffix2);
    // map 将文件数组转为后缀名的二进制表示数组
    // reduce 的结果是一个数，如果数组中全是图片，则为1；如果既有图片又有视频则为3.
    // 我们已经规定，如果有多个文件，则它们必须全部是图片类型，所以可以认为任何数组内都是同一类型文件（其他类型文件只能上传一个）
    // 显然typeBit必须是2的整数幂，判断它是否为2的整数幂
    let isSingleType = (typeBit & typeBit - 1) === 0;

    // todo @杨关 验证不通过则在按钮上加`disabled`属性，通过则去掉
    if(!isSingleType || (files.length>1 && typeBit !== image)){
        let msg = '除了图片，每次只能上传一个文件';
        console.error(msg);
        return msg;
    }else if(files.length === 0){
        let msg = '请选择文件';
        console.error(msg);
        return msg;
    }else{
        console.log('validation passed');
        return true;
    }
    /* 我已经在上方重构了以下的逻辑，使代码
    let pic = false;
    let ved = false;
    let aud = false;
    let other = false;
    let filename = "";
    for (let i = 0; i < files.length; i++) {
        let tempStr = files[i].name;
        // fixme @杨关 [不用改，知道就好了]潜在bug，`你猜猜我是.哪种类型的文件.jpg.mp3.rmvb.pdf.txt`, hint: `let suffix = filename.split('.').pop();`
        if (picture(tempStr.split(".")[1])) {
            pic = true;
            filename = filename + tempStr + "  |  "
        } else if (video(tempStr.split(".")[1])) {
            if (files.length === 1) {
                ved = true;
                filename = filename + tempStr + "  |  "
            } else {
                break;
            }
        } else if (audio(tempStr.split(".")[1])) {
            if (files.length === 1) {
                aud = true;
                filename = filename + tempStr + "  |  "
            } else {
                break;
            }
        } else {
            other = true;
            break;
        }
        //alert(tempStr);
    }
    if ((pic && !ved && !aud && !other)
        || (!pic && ved && !aud && !other)
        || (!pic && !ved && aud && !other)) {
            document.getElementById("validateLabel").innerHTML = filename;
            document.getElementById("uploadButton").style = "display:block";
    } else {
        document.getElementById("validateLabel").innerHTML = "上传错误，请重新上传";
        document.getElementById("uploadButton").style = "display:none";
    }
    */
}


// function picture(str) {
//     let s = str.toString().toLocaleLowerCase();
//     if (s === "jpg" || s === "png" || s === "bmp" || s === "svg") {
//         return true
//     } else {
//         return false
//     }
// }
//
// function video(str) {
//     let s = str.toString().toLocaleLowerCase();
//     if (s === "mpeg" || s === "avi" || s === "mov" || s === "asf" || s === "rmvb" ||
//         s === "mpg" || s === "mp4") {
//         return true
//     } else {
//         return false
//     }
// }
//
// function audio(str) {
//     let s = str.toString().toLocaleLowerCase();
//     if (s === "mp3" || s === "midi" || s === "wma") {
//         return true
//     } else {
//         return false
//     }
// }