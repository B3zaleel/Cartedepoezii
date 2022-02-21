<template>
  <div class="tabs-layout">
    <div class="tab-header">
      <button
        v-for="item in items"
        :key="item.id"
        class="tab-btn"
        @click="selectTab(item.id)"
      >
        {{ item.title }}
        <span :class="{'selected-notif': item.id === selectedId}"></span>
      </button>
    </div>

    <div class="tab-content">
      <slot></slot>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

interface TabItem {
  id: number;
  title: string;
}

@Component({
  name: 'TabsLayout',
})
export default class TabsLayout extends Vue {
  @Prop() items!: Array<TabItem>;

  @Prop() selectedId!: number;

  selectTab(id: number): void {
    this.$emit('select-tab', id);
  }
}
</script>

<style lang="scss">
.tabs-layout {
  > .tab-header {
    display: flex;
    flex-flow: row;
    justify-content: space-evenly;
    height: 40px;

    > .tab-btn {
      position: relative;
      width: calc(100%);
      height: 100%;
      border: none;
      border-radius: 0;
      background: none;
      cursor: pointer;
      transition-property: background;
      transition-duration: 300ms;

      > .selected-notif {
        position: absolute;
        display: inline-block;
        height: 5px;
        width: 80%;
        bottom: 0;
        left: 10%;
        border-radius: 5px;
        background: #6bd39f;
      }

      &:hover {
        background: rgb(199, 199, 199);
      }
    }
  }
  > .tab-content {
    border-top: 2px solid gray;
  }
}
</style>
