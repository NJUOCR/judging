Vue.component('switch-btn', {
    props: ['on'],
    template: `
    <button class="switch-btn" type="button" @click="emitSwitch">
        <div :class="['switch-slider', on?'on':'off']">
            <span :class="['switch-circle', on?'on':'off']"></span>
        </div>
    </button>
    `,
    methods: {
        emitSwitch: function () {
            this.$emit('switch');
        }
    }
});