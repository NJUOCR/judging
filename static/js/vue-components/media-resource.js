Vue.component('media-resource', {
    props: ['type', 'name', 'description'],
    template:
    `
<div class="media-container">
    <div class="media-icon" :class="icon(type)"></div>
    <div class="media-name"> {{ name }} </div>
    <!--<div class="media-remove glyphicon glyphicon-remove"></div>-->
</div>
    `,
    methods: {
        icon: function (type) {
            switch (type){
                case 'audio': return 'glyphicon glyphicon-headphones';
                case 'video': return 'glyphicon glyphicon-facetime-video';
                case 'image': return 'glyphicon glyphicon-picture';
                case 'create': return 'glyphicon glyphicon-plus';
                default: return 'glyphicon glyphicon-file'
            }
        }
    }
});