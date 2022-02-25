<template>
  <MainLayout>
    <template v-slot:header>
      <div class="header-pane">
        <div class="search-pane">
          <input
            placeholder="Search Cartedepoezii"
            v-model="searchQuery"
          />
          <button>
            <MagnifyIcon/>
          </button>
        </div>
      </div>
    </template>

    <template v-slot:main>
      <div class="user-home">
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
.header-pane {
  > .search-pane {
    position: absolute;
    display: grid;
    align-items: center;
    width: calc(100% - 2 * 5px);
    left: 5px;
    grid-template-columns: 1fr auto;

    > input {
      padding: 5px 10px;
      border-radius: 15px;
      border: 2px solid rgb(59, 230, 144);
    }
  }
}
</style>
