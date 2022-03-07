<template>
  <MainLayout>
    <template v-slot:header>
      <div class="header-pane">
        <div class="search-pane">
          <input
            placeholder="Search Cartedepoezii"
            v-model="searchQuery"
            @keydown.enter="search"
          />
          <button @click="search">
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
                <ItemsLoaderLayout
                  :itemsName="'poems'"
                  :itemsFetcher="poemsFetcher"
                  :reverse="true"
                />
              </div>
              <div class="" v-show="selectedId === 2">
                <ItemsLoaderLayout
                  :itemsName="'users'"
                  :itemsFetcher="peopleFetcher"
                  :reverse="true"
                />
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
import { Page, Item } from '@/assets/scripts/types/interfaces';
import SearchAPIReq from '@/assets/scripts/api_requests/search';
import MainLayout from '@/views/layout/Main.vue';
import TabsLayout from '@/views/layout/Tabs.vue';
import ItemsLoaderLayout from '@/views/layout/ItemsLoader.vue';
import Poem from '@/components/Poem.vue';
import UserItem from '@/components/UserItem.vue';
import MagnifyIcon from '@/assets/icons/Magnify.vue';

@Component({
  name: 'SearchView',
  components: {
    MainLayout,
    TabsLayout,
    ItemsLoaderLayout,
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

  searchQueryAPIReq: SearchAPIReq = new SearchAPIReq(
    this.$store.state.API_URL,
    this.$store.state.user.authToken,
  );

  changeSelectedTab(tabId: number): void {
    this.selectedId = tabId;
  }

  getQueryParams(tabId: number):string {
    if (tabId === 1 || tabId === 2) {
      return [
        'q=',
        this.searchQuery,
        '&token=',
        this.$store.state.user.authToken,
      ].join('');
    }
    return '';
  }

  search(): void {
    if (this.$route.params.q !== this.searchQuery) {
      this.$router.push(`/search/${this.searchQuery}`);
      window.location.reload();
    }
  }

  poemsFetcher(page: Page): Promise<{
      success: boolean,
      data?: Array<Item>,
      message?: string
    }> {
    return this.searchQueryAPIReq.findPoems(this.$route.params.q, page);
  }

  peopleFetcher(page: Page): Promise<{
      success: boolean,
      data?: Array<Item>,
      message?: string
    }> {
    return this.searchQueryAPIReq.findPeople(this.$route.params.q, page);
  }

  mounted(): void {
    this.searchQuery = this.$route.params.q;
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/views/search";
</style>
