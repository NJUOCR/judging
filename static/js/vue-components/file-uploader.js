Vue.component('file-uploader', {
    props: ['forbidUpload', 'inputText', 'btnText'],
    template: `
        <div class="up-file">
            <div class="up-file-control input-file">
                <input type="file" name="filename" multiple="multiple" ref="inp"
                       @change="validate"/>
                       {{ inputText }}
            </div>
            <button class="up-file-control up-button" 
            @click="upload" 
            :disabled="forbidUpload"
            v-html="btnText || '上传'"
            ></button>
        </div>
    `,
    methods: {
        upload: function () {
            this.$emit('upload', Array(...this.$refs.inp.files));
        },


        validate: function () {
            this.$emit('validate', Array(...this.$refs.inp.files));
        }
    }
});