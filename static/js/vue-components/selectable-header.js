function list(elem) {
    let root = elem.parentElement.parentElement.parentElement;
    root.attributes['data-show-candidates'] =
        root.attributes['data-show-candidates'] === 'true' ? 'false' : 'true';
    let showList = root.attributes['data-show-candidates'] === 'true';
    elem.className = `glyphicon glyphicon-triangle-${showList ? 'top' : 'bottom'}`;
    let list = root.querySelector('ol');
    list.className = showList ? '' : 'hide-candidates';
}

function unlist(elem) {
    let root = elem.parentElement.parentElement.parentElement;
    root.attributes['data-show-candidates'] = 'false';

    let btn = root.querySelector('.glyphicon-triangle-top');
    if (btn)    btn.className = 'glyphicon glyphicon-triangle-bottom';

    let ol = root.querySelector('ol');
    ol.className = 'hide-candidates';
}

function headerFocus(elem) {
    // let text = elem.parentElement.querySelector('span[onblur]');
    elem.focus();
}

Vue.component('selectable-header', {
    props: {
        candidates: Array,
        selected: Number,
        name: String,
        plain: Boolean
    },
    template:
        `
<div class="selecting" data-show-candidates="false">
    <div class="header-container">
        <div class="glyphicon glyphicon-menu-left header-component" 
            :class="[plain? 'hide-control':'hover']" @click="step('left', name)"></div>
        <div class="header-component header-text" :class="[plain? 'floor':'hover']"> 
            <span onclick="headerFocus(this);list(this);" onblur="unlist(this)" tabindex="10" class="glyphicon glyphicon-triangle-bottom header-control" :class="[plain? 'hide-control':'']"></span>
            <span>
                {{ selected >= 0 ? candidates[selected] : '' }}
            </span>
        </div>
        <div class="glyphicon glyphicon-menu-right header-component header-control" 
            :class="[plain? 'hide-control':'hover']" @click="step('right', name)"></div>
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

        step: function (direction, name) {
            this.$emit('step', direction, name)
        }
    }
});