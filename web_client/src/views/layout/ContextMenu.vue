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
@use "@/assets/styles/globals";

.menu.visible {
  display: block;
}

.menu {
  display: none;
  padding: 5px 0;
  border-radius: 4px;
  border: 1px solid gray;
  background: ghostwhite;
  z-index: 700;
  box-shadow: 0 0 2px 1.5px #a3a3a3dc;

  > div {
    display: flex;
    flex-flow: column;

    .menu-item {
      display: flex;
      padding: 5px;
      color: black;
      background: none;
      border: none;
      white-space: nowrap;
      text-decoration: none;
      cursor: pointer;

      &:hover {
        color: white;
        background: globals.$primary-color-light;

        &.danger {
          background: globals.$danger-color-light;
        }
      }
    }
  }
}
</style>
