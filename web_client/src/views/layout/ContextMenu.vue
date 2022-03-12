<template>
  <div
    :class="{menu: true, visible: isMenuOpen,}"
    :style="positionStyle"
    @mousedown="mouseDownEvent"
  >
    <slot></slot>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Position } from '@/assets/scripts/types/interfaces';

@Component({
  name: 'ContextMenuLayout',
  computed: {
    positionStyle() {
      const style = {
        position: this.$props.position.type,
        left: this.$props.position.left || 'auto',
        top: this.$props.position.top || 'auto',
        right: this.$props.position.right || 'auto',
        bottom: this.$props.position.bottom || 'auto',
      };
      return style;
    },
  },
  methods: {
    mouseDownEvent(ev) {
      ev.preventDefault();
      ev.stopPropagation();
    },
  },
}) export default class ContextMenuLayout extends Vue {
  @Prop() isMenuOpen!: boolean;

  @Prop() position?: Position;

  created(): void {
    window.addEventListener('mousedown', () => {
      this.$emit('request-close');
    });
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/views/layout/context_menu";
</style>
