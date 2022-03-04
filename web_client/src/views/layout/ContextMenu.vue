<template>
  <div
    :class="{menu: true, visible: isMenuOpen,}"
    :style="getPositionStyle()"
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
  methods: {
    mouseDownEvent(ev) {
      ev.preventDefault();
      ev.stopPropagation();
    },
  },
}) export default class ContextMenuLayout extends Vue {
  @Prop() isMenuOpen!: boolean;

  @Prop() position: Position = {
    type: 'absolute',
    right: '0',
    top: '0',
  };

  getPositionStyle(): Record<string, string> {
    const style = {
      position: this.position.type,
      left: this.position.left || 'auto',
      top: this.position.top || 'auto',
      right: this.position.right || 'auto',
      bottom: this.position.bottom || 'auto',
    };
    return style;
  }

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
