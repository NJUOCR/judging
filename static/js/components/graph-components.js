Vue.component('second-level-item', {
    props: ['second'],
    template:
`
<div class='second-level-container'>
    <div class="second-level-text">
        <div>{{ second.name.substring(0, (1 + second.name.length)/2^0) }}</div>
        
        <div>{{ second.name.substring((1 + second.name.length)/2^0) }}</div>
    </div>
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
        <li v-for="item in first.secondLevelItems"><second-level-item :second="item"></second-level-item></li>
    </ul>
</div>
`
});