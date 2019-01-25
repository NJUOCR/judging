Vue.component('universal-album', {
    props: {
        cur: Number,
        links: Array,
    },
    template: `
<div class="universal-album">
    <img :src="links[cur]">
    <div class="universal-album-control">
        <button @click="goto(cur+1)">上一页</button>
        <button>下一页</button>
    </div>
</div>
    `,
    methods: {
        goto: function (idx) {
            if(idx < links.length() && idx >= 0){
                this.$emit('album-goto', idx)
            }
        }
    }
});