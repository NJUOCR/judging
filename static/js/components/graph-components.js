function clickItem(elem){
    let e = window.event;
    console.log(e);
    console.log(Array.apply(this, arguments))
}

let selector = {
    methods: {
        thirdLevelSelect: function(idx){
            let e = window.event;
            e['selection'] = [-1, -1, idx];
        },

        secondLevelSelect: function (idx) {
            let e = window.event;
            if (e['selection']){
                e['selection'][1] = idx;
            }else{
                e['selection'] = [-1, idx];
            }
        },

        firstLevelSelect: function (idx) {
            /*
             * 这个方法会最后一个收到事件，即，点击事件会从子元素逐一冒泡到根元素
             */
            let e = window.event;
            if (e['selection']){
                e['selection'][0] = idx;
            }else{
                e['selection'] = [idx];
            }
        }
    }
};

Vue.component('third-level-item', {
    mixins: [selector],
    props: ['third', 'thirdLevelIdx'],
    template:
`
    <div class="third-level-container" @click="thirdLevelSelect(thirdLevelIdx)" data-level="3">
        <div class="third-level-text">
            {{ third.name }}
        
        </div>
    </div>
`
});


Vue.component('second-level-item', {
    mixins: [selector],
    props: ['second', 'secondLevelIdx'],
    template:
`
    <div class='second-level-container' @click="secondLevelSelect(secondLevelIdx);">
        <div class="second-level-text">
            <div>{{ second.name.substring(0, (1 + second.name.length)/2^0) }}</div>
            
            <div>{{ second.name.substring((1 + second.name.length)/2^0) }}</div>
        </div>
        <ul class="horizontal-list">
            <li v-for="(third, thirdLevelIdx) in second.thirdLevelItems" 
                :style="{width: parseInt(100 * third.name.length / 
                second.thirdLevelItems.map(i => i.name.length).reduce((x1, x2) => x1+x2)) + '%'}">
                    <third-level-item :third="third" :third-level-idx="thirdLevelIdx"></third-level-item>
            </li>
        </ul>
    </div>
`
});


Vue.component('first-level-item', {
    mixins: [selector],
    props: ['first', 'firstLevelIdx'],
    template:
`
<div class="first-level-container" @click="firstLevelSelect(firstLevelIdx);">
    <div class="box-arrow">
        <div class="box-arrow-text">{{ first.name }}</div>
        <div class="box-arrow-bg">
            <div class="box-arrow-bg-top"></div>
            <div class="box-arrow-bg-bottom"></div>
        </div>
    </div>
    <ul class="horizontal-list">
        <li v-for="(second, secondLevelIdx) in first.secondLevelItems">
            <second-level-item :second="second" :second-level-idx="secondLevelIdx"></second-level-item>
        </li>
    </ul>
</div>
`
});