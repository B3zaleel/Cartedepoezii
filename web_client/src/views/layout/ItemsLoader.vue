<template>
  <div class="items-loader">
    <div>
      <div v-for="group in itemGroups" :key="group.id">
        <div v-if="itemsName === 'users'">
          <UserItem
            v-for="item in getUsers(group.id)"
            :key="item.id"
            :user="item"
          />
        </div>
        <div v-if="itemsName === 'poems'">
          <Poem
            v-for="item in getPoems(group.id)"
            :key="item.id"
            :poem="item"
            :updateDisplay="updateItemView"
          />
        </div>
        <div v-if="itemsName === 'comments'">
          <Comment
            v-for="item in getComments(group.id)"
            :key="item.id"
            :comment="item"
          />
        </div>
      </div>
    </div>

    <div :class="{sect: true, hidden: !loadingItems}">
      <LoadingIcon/>
    </div>

    <div :class="{sect: true, hidden: !loadingFailed || loadingItems}">
      <h4>Failed to load {{ itemsName }}</h4>
      <button class="cdp-btn text" @click="loadItems">
        <RefreshIcon/>
        <b>Retry</b>
      </button>
    </div>

    <div :class="{
      sect: true,
      hidden: (itemGroups.length > 0) || loadingFailed || loadingItems
      }">
      <h3 v-show="!useCustom404">
        Nothing found
      </h3>
      <div v-show="useCustom404">
        <slot></slot>
      </div>
    </div>

    <div :class="{
      sect: true,
      hidden: endReached || loadingItems || loadingFailed
      }">
      <button class="cdp-btn text" @click="loadItems">
        <b>More</b>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Item, Page } from '@/assets/scripts/types/interfaces';
import LoadingIcon from '@/assets/icons/Loading.vue';
import RefreshIcon from '@/assets/icons/Refresh.vue';
import Poem from '@/components/Poem.vue';
import Comment from '@/components/Comment.vue';
import UserItem from '@/components/UserItem.vue';

@Component({
  name: 'ItemsLoaderLayout',
  components: {
    LoadingIcon,
    RefreshIcon,
    Poem,
    Comment,
    UserItem,
  },
})
export default class ItemsLoaderLayout extends Vue {
  @Prop() itemsName!: string;

  @Prop({ default: false }) reverse!: boolean;

  @Prop({ default: true }) updateItemView!: boolean;

  @Prop({ default: false }) useCustom404!: boolean;

  @Prop() itemsFetcher!: (page: Page) => Promise<{
    success: boolean,
    data?: Array<Item>,
    message?: string
  }>;

  itemGroups: Array<{id: number, group: Array<Item>}> = [];

  groupsLoaded = 0;

  lastItemId = '';

  loadingItems = false;

  loadingFailed = true;

  endReached = false;

  async loadItems(): Promise<void> {
    if (this.endReached) {
      return;
    }
    this.loadingItems = true;
    this.loadingFailed = false;
    const nextPage = {
      span: 12,
      after: this.reverse ? '' : this.lastItemId,
      before: this.reverse ? this.lastItemId : '',
    };
    const res = await this.itemsFetcher(nextPage);
    if (res.success) {
      if (res.data) {
        if (res.data.length > 0) {
          this.itemGroups.push({
            id: this.groupsLoaded,
            group: res.data,
          });
          this.groupsLoaded += 1;
        }
        this.lastItemId = res.data.length > 0 ? res.data[res.data.length - 1].id : '';
        this.endReached = res.data.length < nextPage.span;
        this.loadingItems = false;
        this.loadingFailed = false;
      }
    } else if (res.message) {
      console.error(res.message);
      this.loadingItems = false;
      this.loadingFailed = true;
    }
  }

  getPoems(groupId: number): Array<Item> {
    let items: Array<Item> = [];
    if (this.itemsName === 'poems') {
      items = this.itemGroups[groupId].group;
    }
    return items;
  }

  getComments(groupId: number): Array<Item> {
    let items: Array<Item> = [];
    if (this.itemsName === 'comments') {
      items = this.itemGroups[groupId].group;
    }
    return items;
  }

  getUsers(groupId: number): Array<Item> {
    let items: Array<Item> = [];
    if (this.itemsName === 'users') {
      items = this.itemGroups[groupId].group;
    }
    return items;
  }

  mounted(): void {
    this.loadItems();
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/views/layout/items_loader";
</style>
