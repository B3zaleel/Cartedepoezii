<template>
  <MainLayout>
    <template v-slot:header>
      <div class="header-pane">
        <div class="search-pane">
          <input
            placeholder="Search Cartedepoezii"
            v-model="searchQuery"
          />
          <button class="cdp-btn icon">
            <MagnifyIcon/>
          </button>
        </div>
      </div>
    </template>

    <template v-slot:main>
      <div class="user-search">
        <div>
          <TabsLayout
            :items="tabItems"
            v-bind:selectedId="selectedId"
            v-on:select-tab="args => changeSelectedTab(args)"
          >
            <div>
              <div class="" v-show="selectedId === 1">
                No Poems found
              </div>
              <div class="" v-show="selectedId === 2">
                No Users found
              </div>
            </div>
          </TabsLayout>
        </div>
      </div>
    </template>
  </MainLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Poem as PoemT, UserMin } from '@/assets/scripts/type_defs';
import MainLayout from '@/views/layout/Main.vue';
import TabsLayout from '@/views/layout/Tabs.vue';
import Poem from '@/components/Poem.vue';
import UserItem from '@/components/UserItem.vue';
import MagnifyIcon from '@/assets/icons/Magnify.vue';

@Component({
  name: 'SearchView',
  components: {
    MainLayout,
    TabsLayout,
    Poem,
    UserItem,
    MagnifyIcon,
  },
})
export default class SearchView extends Vue {
  selectedId = 1;

  tabItems = [
    {
      id: 1,
      title: 'Poems',
    },
    {
      id: 2,
      title: 'Users',
    },
  ];

  searchQuery = '';

  changeSelectedTab(tabId: number): void {
    this.selectedId = tabId;
  }

  created(): void {
    this.searchQuery = this.$route.params.q;
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/views/search";
</style>
