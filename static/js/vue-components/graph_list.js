Vue.component('graph-list', {
    props: ['leaveToClass', 'active', 'carouselList'],
    template: `
    <div class="graph-list-box">
                    <ul class="graph-list">
                        <li class="graph-item" v-for="(item, index) in graphlist">
                            <div class="item-top">
                                <span class="item-text">{{ item }}</span>
                                <div class="item-button-box">
                                    <a class="item-button glyphicon glyphicon-plus" v-on:click="newCase()"></a>
                                    <a class="item-button glyphicon glyphicon-minus"></a>
                                </div>
                            </div>
                            <div class="item-bottom" :class="[ isNewCase ? 'show-input' : 'hide-input']">
                                <input id="case-id-input" class="case-input" type="text" >
                                <div class="item-button-box">
                                    <a class="item-button glyphicon glyphicon-ok"></a>
                                    <a class="item-button glyphicon glyphicon-remove" v-on:click="newCase()"></a>
                                </div>
                            </div>
                        </li>
                    </ul>
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