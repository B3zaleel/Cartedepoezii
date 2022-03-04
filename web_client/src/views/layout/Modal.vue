<template>
  <div
    :class="{'modal-view': true, hidden: !modalOpen}"
    @mousedown.self="closeDialog"
    @mousedown="cancelBubble"
  >
    <div>
      <div class="header">
        <div>
          <h3>{{ modalTitle }}</h3>
        </div>
        <div>
          <button @click="closeDialog" class="cdp-btn icon danger">
            <CloseIcon />
          </button>
        </div>
      </div>

      <div class="content">
        <slot name="modal-body"></slot>
      </div>

      <div class="footer">
        <slot name="modal-action-panel"></slot>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import CloseIcon from '@/assets/icons/Close.vue';

@Component({
  methods: {
    cancelBubble(ev: MouseEvent): void {
      ev.preventDefault();
      ev.stopPropagation();
      ev.stopImmediatePropagation();
    },
  },
  components: {
    CloseIcon,
  },
}) export default class MainLayout extends Vue {
  @Prop() modalOpen!: boolean;

  @Prop() modalTitle!: string;

  @Prop() hasHeader!: boolean;

  @Prop() hasFooter!: boolean;

  closeDialog(ev: Event): void {
    this.$emit('request-close');
    ev.preventDefault();
    ev.stopPropagation();
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/views/layout/modal";
</style>
