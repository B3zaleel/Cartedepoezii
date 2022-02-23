<template>
  <div
    :class="{menu: true, visible: isMenuOpen,}"
    @mousedown="mouseDownEvent"
  >
    <slot></slot>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

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

  created(): void {
    window.addEventListener('mousedown', () => {
      this.$emit('request-close');
    });
  }
}
</script>

<style lang="scss">
.menu.visible {
  display: block;
}

.menu {
  position: absolute;
  display: none;
  right: 0;
  top: 0;
  padding: 5px 0;
  border-radius: 4px;
  border: 1px solid gray;
  background: ghostwhite;
  z-index: 5;
  box-shadow: 0 0 2px 1.5px #a3a3a3dc;

  > div {
    display: flex;
    flex-flow: column;

    .menu-item {
      padding: 5px;
      background: none;
      border: none;
      cursor: pointer;

      &:not(:first-child) {
        border-top: 1px solid gainsboro;
      }

      &:hover {
        background: gainsboro;
      }
    }
  }
}
</style>
