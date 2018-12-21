Vue.component('album', {
    props: ['leaveToClass', 'active', 'carouselList'],
    template: `
    <div id="carousel-first-level" class="carousel-ground">
        <span @click="ocr(carouselList[active])" class="glyphicon glyphicon-random"></span>
        <transition name="carousel-animates"
                    enter-class="carousel-animate-enter"
                    leave-class="carousel-animate-leave"
                    :leave-active-class="leaveToClass">
            <div id="carousel-second-level" class="carousel-image">
                <div class="image-item" :key="active" id="image-item">
                    <a :href="carouselList[active]" target="_blank" :title="carouselList[active]">
                        <img :src="carouselList[active]" alt="" class="image">
                    </a>
                </div>
            </div>
        </transition>
        <div class="carousel-indicator">
            <a v-for="(item,index) in carouselList" :key="index" v-if="active==index" class="item active">
            {{ (index + 1)+"/"+carouselList.length}}
            </a>
        </div>


        <a @click="move(-1)" class="left carousel-control1">
            <i class="icon1 glyphicon glyphicon-menu-left"></i>
        </a>

        <a @click="move(1)" class="right carousel-control1">
            <i class="icon1 glyphicon glyphicon-menu-right"></i>
        </a>
    </div>
    `,

    methods: {
        move: function (offset) {
            this.$emit('carousel-move', offset);
        },
        
        ocr: function (absPath) {
            this.$emit('ocr', absPath)
        }
    }
});