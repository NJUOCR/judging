Vue.component('graph-list', {
    props: ['graphList'],
    data:function(){
        return{
            isNewCase: false
        }
    },
    template: `
        <div class="graph-list-box">
            <ul class="graph-list">
                <li class="graph-item" v-for="(item, index) in graphList">
                    <div class="item-top">
                        <span class="item-text">{{ item }}</span>
                        <div class="item-button-box">
                            <a class="item-button glyphicon glyphicon-plus" @click="newCase()"></a>
                            <a class="item-button glyphicon glyphicon-minus"></a>
                        </div>
                    </div>
                    <div class="item-bottom" :class="[ isNewCase ? 'show-input' : 'hide-input']">
                        <input id="case-id-input" class="case-input" type="text" ref="caseName">
                        <div class="item-button-box">
                            <a class="item-button glyphicon glyphicon-ok" @click="createCase()"></a>
                            <a class="item-button glyphicon glyphicon-remove" @click="newCase()"></a>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    `,

    methods: {
        move: function(graph_name){
            this.$emit('show-cases', graph_name)
        },
        newCase: function (event) {
            if(this.isNewCase){
                this.isNewCase = false;
            }else{
                this.isNewCase = true;
            }
        },
        createCase: function(event) {
            console.log(this.$refs.caseName.text)
        }
    }
});