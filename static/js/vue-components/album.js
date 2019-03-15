Vue.component('album', {
    // props: ['forward', 'active', 'urls', 'enableOcr', 'enableCanvas', 'boxes'],
    props: {
        forward: Boolean,
        active: Number,         // current url index
        urls: Array,            // image url list
        enableCanvas: Boolean,
        /**
         * [
         *      // img0
         *      [[x1, y1, x2, y2], ...],
         *      ...
         * ]
         */
        boxes: Array,
        activeBoxIdx: Number
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
                    <div :class="['box', boxIdx===activeBoxIdx?'active-box':'']"  v-for="(box,boxIdx) in getCommentBoxes(active)"
                        :style="{top: box[1]*100+'%',
                                left: box[0]*100+'%', 
                                width: (box[2]-box[0])*100+'%',
                                height: (box[3]-box[1])*100+'%'}" 
                        @click="selectBox(boxIdx)">
                        <span class="box-id" v-text="boxIdx+1"></span>
                        <!--<span class="glyphicon glyphicon-remove remove" @click="removeCommentBox(boxIdx)"></span>-->
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
            let x1 = e.offsetX / w,
                y1 = e.offsetY / h,
                x2 = 0,
                y2 = 0;

            function move(e1) {
                x2 = e1.offsetX / w;
                y2 = e1.offsetY / h;
                if (x2 > x1) {
                    tmpBox.style.left = x1 * 100 + '%';
                    tmpBox.style.width = (x2 - x1) * 100 + '%';
                    tmpBox.style.right = 'unset';
                } else {
                    // tmpBox.style.right = x1 * 100 + '%';
                    tmpBox.style.left = x2 * 100 + '%';
                    tmpBox.style.width = (x1 - x2) * 100 + '%';
                }
                if (y2 > y1){
                    tmpBox.style.top = y1 * 100 + '%';
                    tmpBox.style.height = (y2 - y1) * 100 + "%";
                }else{
                    tmpBox.style.top = y2 * 100 + '%';
                    tmpBox.style.height = (y1 - y2) * 100 + '%';
                }
                console.log(tmpBox.style.top, tmpBox.style.left, tmpBox.style.bottom, tmpBox.style.right)
                console.log(tmpBox.style.width, tmpBox.style.height);
            }

            function up(e2) {
                canvas.removeEventListener('mouseup', up);
                canvas.removeEventListener('mousemove', move);
                x2 = e2.offsetX / w;
                y2 = e2.offsetY / h;

                self.$emit('draw-box', x1, y1, x2, y2);
                // tmpBox.style.height = '0';
            }

            canvas.addEventListener('mousemove', move);
            canvas.addEventListener('mouseup', up);
        },

        getCommentBoxes: function () {
            let boxes = this.boxes;
            if (boxes !== undefined) {
                return boxes
            } else {
                return []
            }
        },

        selectBox: function (boxIdx) {
            this.$emit('select-box')

        }
    }
});