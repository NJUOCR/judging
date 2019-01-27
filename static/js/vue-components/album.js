Vue.component('album', {
    // props: ['forward', 'active', 'urls', 'enableOcr', 'enableCanvas', 'boxes'],
    props: {
        forward: Boolean,
        active: Number,
        urls: Array,
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
        <transition name="album-animates"
                    enter-class="album-animate-enter"
                    leave-class="album-animate-leave"
                    :leave-active-class="forward? 'album-animate-leave-to-right' : 'album-animate-leave-to-left'">
            <div class="album-image">
                <div class="image-item" :key="active">
                    <img :src="urls[active]" alt="" class="image">
                    <div v-if="enableCanvas" class="canvas" @mousedown="comment">
                        
                    </div>
                    <div v-if="enableCanvas" ref="bounding" class="bounding"></div>
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

        comment: function (e) {
            let canvas = e.target;
            let tmpBox = this.$refs.bounding;
            let self = this;
            let w = canvas.offsetWidth,
                h = canvas.offsetHeight;
            let x1 = e.offsetX * 100 / w,
                y1 = e.offsetY * 100 / h,
                x2 = 0,
                y2 = 0;
            function move(e1){
                x2 = e1.offsetX / w;
                y2 = e1.offsetY / h;
                tmpBox.style.left = x1*100 + '%';
                tmpBox.style.top = y1*100 + '%';
                tmpBox.style.width = (x2 - x1)*100 + '%';
                tmpBox.style.height = (y2 - y1)*100 + "%";
            }
            function up(e2) {
                canvas.removeEventListener('mouseup', up);
                canvas.removeEventListener('mousemove', move);
                x2 = e2.offsetX / w;
                y2 = e2.offsetY / h;

                self.$emit('draw-box', x1, y1, x2, y2);
                tmpBox.style.height = '0';
            }

            canvas.addEventListener('mousemove', move);
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