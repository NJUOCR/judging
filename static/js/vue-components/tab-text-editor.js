Vue.component('tab-text-editor', {
    props: {
        // tabs: Array,
        // contents: Array,
        pointer: Number,
        nameAndContents: Array
    },
    template:
        `
<article class="tab-text-editor">
    <header>
        <ul>
            <li v-for="(nc,i) in nameAndContents" :class="{'selected-tab': i===pointer}" @click="select(i)">{{nc.name}}</li>
        </ul>
    </header>
        
    <div>
        <textarea v-if="pointer >= 0" v-model="pointer === -1 ? '' : nameAndContents[pointer].contents"></textarea>
    </div>
</article>
    `,
    methods: {
        select: function (i) {
            this.$emit('change-tab', i);
        }
    }
});