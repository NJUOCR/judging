Vue.component('album', {
    // props: ['forward', 'active', 'urls', 'enableOcr', 'enableCanvas', 'boxes'],
    props: {
        forward: Boolean,
        active: Number,
        urls: Array,
        enableOcr: Boolean,
        enableCanvas: Boolean,
        /**
         * [
         *      // img0
         *      [[x1, y1, x2, y2], ...],
         *      ...
         * ]
         */
        boxes: Array
    },
    template: `
    <div class="album-ground">
        <span v-if="enableOcr" @click="ocr(urls[active])" class="glyphicon glyphicon-random"></span>
        <transition name="album-animates"
                    enter-class="album-animate-enter"
                    leave-class="album-animate-leave"
                    :leave-active-class="forward? 'album-animate-leave-to-right' : 'album-animate-leave-to-left'">
            <div class="album-image">
                <div class="image-item" :key="active">
                    <img :src="urls[active]" alt="" class="image">
                    <div v-if="enableCanvas" class="canvas" @mousedown="comment">
                        
                    </div>
                    <div class="box"  v-for="(box,boxIdx) in getCommentBoxes(active)"
                        :style="{top: box[1]+'%',
                                left: box[0]+'%', 
                                width: box[2]-box[0]+'%',
                                height: box[3]-box[1]+'%'}">
                        <span class="glyphicon glyphicon-remove remove" @click="removeCommentBox(boxIdx)"></span>
                    </div>
                </div>
            </div>
        </transition>
        <div class="album-indicator">
            <span v-for="(item,index) in urls" :key="index" v-if="active==index" class="item active">
            {{ (index + 1)+"/"+urls.length}}
            </span>
        </div>


        <a @click="move(-1)" class="left album-control1">
            <i class="icon1 glyphicon glyphicon-menu-left"></i>
        </a>

        <a @click="move(1)" class="right album-control1">
            <i class="icon1 glyphicon glyphicon-menu-right"></i>
        </a>
    </div>
    `,

    methods: {
        move: function (offset) {
            this.$emit('album-move', offset);
        },
        
        ocr: function (absPath) {
            this.$emit('ocr', absPath)
        },

        comment: function (e) {
            let canvas = e.target;
            let self = this;
            let w = canvas.offsetWidth,
                h = canvas.offsetHeight;
            let x1 = e.offsetX * 100 / w,
                y1 = e.offsetY * 100 / h,
                x2 = 0,
                y2 = 0;
            function up(e2) {
                canvas.removeEventListener('mouseup', up);
                x2 = e2.offsetX * 100 / w;
                y2 = e2.offsetY * 100 / h;

                self.$emit('draw-box', x1, y1, x2, y2);
            }

            canvas.addEventListener('mouseup', up);
        },

        getCommentBoxes: function (idx) {
            if(this.boxes !== undefined && this.boxes.length > idx){
                return this.boxes[idx]
            }else{
                return []
            }
        },

        removeCommentBox: function (idx) {
            this.$emit('remove-box', idx);
        }
    }
});