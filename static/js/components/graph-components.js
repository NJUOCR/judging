Vue.component('third-level-item', {
    props: ['third'],
    template:
`
    <div class="third-level-container">
        <div class="third-level-text">
            {{ third.name }}
        
        </div>
    </div>
`
});


Vue.component('second-level-item', {
    props: ['second'],
    template:
`
    <div class='second-level-container'>
        <div class="second-level-text">
            <div>{{ second.name.substring(0, (1 + second.name.length)/2^0) }}</div>
            
            <div>{{ second.name.substring((1 + second.name.length)/2^0) }}</div>
        </div>
        <ul class="horizontal-list">
            <li v-for="third in second.thirdLevelItems" 
                :style="{width: parseInt(100 * third.name.length / 
                second.thirdLevelItems.map(i => i.name.length).reduce((x1, x2) => x1+x2)) + '%'}">
                    <third-level-item :third="third"></third-level-item>
            </li>
        </ul>
    </div>
`
});


Vue.component('first-level-item', {
    props: ['first'],
    template:
`
<div class="first-level-container">
    <div class="box-arrow">
        <div class="box-arrow-text">{{ first.name }}</div>
        <div class="box-arrow-bg">
            <div class="box-arrow-bg-top"></div>
            <div class="box-arrow-bg-bottom"></div>
        </div>
    </div>
    <ul class="horizontal-list">
        <li v-for="second in first.secondLevelItems"><second-level-item :second="second"></second-level-item></li>
    </ul>
</div>
`
});