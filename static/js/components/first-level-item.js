Vue.component('first-level-item', {
    props: ['item'],
    template:
`
<div class="first-level-container">
    <div class="box-arrow">
        <div class="box-arrow-text">{{ item.name }}</div>
        <div class="box-arrow-bg">
            <div class="box-arrow-bg-top"></div>
            <div class="box-arrow-bg-bottom"></div>
        </div>
    </div>
</div>
`
});