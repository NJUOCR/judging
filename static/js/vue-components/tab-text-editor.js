Vue.component('tab-text-editor', {
    props: {
        tabs: Array,
        contents: Array,
        pointer: Number
    },
    template:
        `
<article class="tab-text-editor">
    <header>
        <ul>
            <li v-for="(tab,i) in tabs" :class="{'selected-tab': i===pointer}" @click="select(i)">{{tab}}</li>
        </ul>
    </header>
        
    <div>
        <textarea v-model="contents[pointer]"></textarea>
    </div>
</article>
    `,
    methods: {
        select: function (i) {
            this.$emit('change-tab', i);
        }
    }
});