function showOrClose(elem) {
    let root = elem.parentElement.parentElement.parentElement;
    root.attributes['data-show-candidates'] =
        root.attributes['data-show-candidates'] === 'true' ? 'false' : 'true';
    let show = root.attributes['data-show-candidates'] === 'true';
    console.log(show);
    elem.className = `glyphicon glyphicon-triangle-${show ? 'top' : 'bottom'}`;
    let list = root.querySelector('ol');
    list.className = show ? '' : 'hide-candidates';
}


Vue.component('selectable-header', {
    props: {
        candidates: Array,
        selected: Number,
        name: String
    },
    template:
        `
<div class="selecting" data-show-candidates="false">
    <div class="header-container">
        <div class="glyphicon glyphicon-menu-left header-component hover"></div>
        <div class="header-component header-text hover"> 
            <span onclick="showOrClose(this)" class="glyphicon glyphicon-triangle-bottom"></span>
            <span>{{ selected >= 0 ? candidates[selected] : '' }}</span>
        </div>
        <div class="glyphicon glyphicon-menu-right header-component hover"></div>
    </div>
    <ol class="hide-candidates" >
        <li @click="candidateClick(idx, name)" class="candidate" v-for="(candidate, idx) in candidates"> {{ candidate }} </li>
    </ol>
</div>
    `,

    methods: {
        candidateClick: function (idx, name) {
            this.$emit('change-candidate', idx, name);
        },

        hi: function () {
            console.log('hi')
        }
    }
});