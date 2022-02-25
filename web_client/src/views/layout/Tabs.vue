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
@use "@/assets/styles/views/layout/tabs";
</style>
