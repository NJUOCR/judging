Vue.component('bool-list-editor', {
    props: ['list'],
    template: `
<ul class="bool-list-editor">
    <li v-for="(item, idx) in list" :class="[item.contents==='是'? 'yes':'no']">
        <span class="bool-item-btn" @click="changeBool(idx);" :class="['glyphicon', item.contents==='是'? 'glyphicon-ok':'glyphicon-remove']"></span>
        <span class="bool-item-name">{{item.name}}</span>
    </li>    
</ul>
    `,
    methods: {
        changeBool: function (idx) {
            this.$emit('change-bool', idx);
        }
    }
});