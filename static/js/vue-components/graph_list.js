Vue.component('graph-list', {
    props: ['graphList'],
    data: function () {
        return {
            isNewCase: false,
            currentIndex: "-1",
            inputList: [],
            searchGraph: ""
        }
    },
    computed: {
        graphs: function () {
            var result = Array();
            var length = this.searchGraph.length
            for (var i = 0; i < this.graphList.length; i++) {
                if(this.graphList[i].length >= length && this.graphList[i].substring(0,length)==this.searchGraph) {
                    result.push(this.graphList[i]);
                }
            }
            return result;
        }
    },
    template: `
        <div>
            <div class="search-box">
                <input id="search_input" class="search" type="text" v-model="searchGraph">
                <span class="search-icon glyphicon glyphicon-search"></span>
            </div>
            <hr class="separate-line"/>
            <div class="graph-list-box">
                <ul class="graph-list">
                    <li class="graph-item" v-for="(item, index) in this.graphs" :id="index" @click="changeCases(item)">
                        <div class="item-top">
                            <span class="item-text" >{{ item }}</span>
                            <div class="item-button-box">
                                <a class="item-button glyphicon glyphicon-plus" @click="newCase(index, 'true')"></a>
                                <a class="item-button glyphicon glyphicon-minus" @click="removeGraph(item)"></a>
                            </div>
                        </div>
                        <div class="item-bottom" :class="classes(index)">
                            <input class="case-input" type="text" v-model="inputList[index]">
                            <div class="item-button-box">
                                <a class="item-button glyphicon glyphicon-ok" @click="createCase(index, item)"></a>
                                <a class="item-button glyphicon glyphicon-remove" @click="newCase(index, 'false')"></a>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    `,

    methods: {
        changeCases: function (graph_name) {
            this.$emit('show-cases', graph_name)
        },
        newCase: function (index, isTrue) {
            this.currentIndex = index;
            if (isTrue === "true") {
                this.isNewCase = true;
            } else {
                this.isNewCase = false;
            }

        },
        createCase: function (index, item) {
            if (this.inputList[index] == undefined || this.inputList[index] == "" || this.inputList[index] == null) {
                alert("输入不可以为空！");
                return;
            }
            console.log(this.inputList[index]);
            document.cookie = "case-id=" + this.inputList[index];
            document.cookie = "graph-name=" + item;
            const url = "/config-graph";
            window.location.href = url
            //const url = "/config-graph?case_id="+this.inputList[index]+"&graph_name="+item

        },
        removeGraph: function (item) {
            this.$emit('remove-graph', item)
        },
        classes: function (index) {
            //[(index==currentIndex: 'currentGraph'),(isNewCase ? 'show-id-input' : 'hide-id-input')]
            let result_class = "";
            if (this.isNewCase && (index === this.currentIndex || this.currentIndex === "-1")) {
                result_class = " " + "show-input"
            } else {
                result_class = " " + "hide-input"
            }
            return result_class;
        }
    }
});