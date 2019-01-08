function upFile(category, description) {
    const url = "/media-upload";
    let formData = new FormData();
    let files = document.getElementById('upload_media').files;

    // let filenames = files.map(f => f.name);
    files.forEach((temp) => {
        let filename = temp.name;
        formData.append(filename, temp);
    });

    formData.append("category", "测试案号123/查找被害人，确认死者身份/死亡时间/视听材料/图片集1");
    formData.append("description", "这是关于媒体1文件的描述，这个描述可以很长");

    fetch(url, {
        method: "post",
        body: formData
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
        console.error("Fetch错误:" + err);
    });
}

function validate(uploadBtn) {
    let files = document.getElementById("uploadMedia").files;

    // 二进制
    let image = 0b0001;
    let video = 0b0010;
    let audio = 0b0100;
    let other = 0b1000;

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
    let typeBit = new Array(...files).map(fileObj => getMediaTypeBits(fileObj.name.split('.').pop())).reduce((suffix1, suffix2) => suffix1 | suffix2);
    let isSingleType = (typeBit & typeBit - 1) === 0;

    if (!isSingleType || (files.length > 1 && typeBit !== image)) {
        let msg = '除了图片，每次只能上传一个文件';
        console.error(msg);
        uploadBtn.disabled = true;
        return msg;
    } else if (files.length === 0) {
        let msg = '请选择文件';
        console.error(msg);
        uploadBtn.disabled = true;
        return msg;
    } else {
        console.log('validation passed');
        uploadBtn.disabled = false;
        return true;
    }
}
let uploader = new Vue({
    el: '#file-up-container',
    data: {
        forbidUpload: true,
    },
    method: {
        validate: function (files) {
            // 二进制
            let image = 0b0001;
            let video = 0b0010;
            let audio = 0b0100;
            let other = 0b1000;

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

            let typeBit = new Array(...files).map(fileObj => getMediaTypeBits(fileObj.name.split('.').pop())).reduce((suffix1, suffix2) => suffix1 | suffix2);
            let isSingleType = (typeBit & typeBit - 1) === 0;

            if (!isSingleType || (files.length > 1 && typeBit !== image)) {
                let msg = '除了图片，每次只能上传一个文件';
                console.error(msg);
                this.forbidUpload = true;
            } else if (files.length === 0) {
                let msg = '请选择文件';
                console.error(msg);
                this.forbidUpload = true;
                return msg;
            } else {
                console.log('validation passed');
                this.forbidUpload = false;
                return true;
            }
        },

    }
});