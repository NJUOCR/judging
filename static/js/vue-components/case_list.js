Vue.component('case-list', {
    props: ['caseList'],
    data:function (){
            return{
                currentIndex:"-1",
                inputList:[],

                searchCase:""
            }
        },
    computed: {
        cases: function () {
            var match = new RegExp(this.searchCase, "i");
            return this.caseList.filter(c => c.search(match)!==-1);
        }
    },
    template: `
        <div>
            <div class="search-box">
                <input id="search_input" class="search" type="text" v-model="searchCase">
                <span class="search-icon glyphicon glyphicon-search"></span>
            </div>
            <hr class="separate-line"/>
            <div class="graph-list-box">
                <ul class="graph-list">
                    <li class="graph-item" v-for="(item, index) in this.cases" :id="index">
                        <div class="item-top ">
                            <span class="item-text" @click="changeCases(item)">{{ item }}</span>
                            <div class="item-button-box">
                                <a class="item-button glyphicon glyphicon-cog" @click="configCase(item)"></a>
                                <a class="item-button glyphicon glyphicon-minus" @click="removeCase(item)"></a>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    `,

    methods: {
        configCase: function(item) {
            document.cookie="case-id="+item;
            const url = "/config-graph";
            window.location.href = url
        },
        removeCase: function(item) {
            this.$emit('remove-case', item)
        },
    }
});