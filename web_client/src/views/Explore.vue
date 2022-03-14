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
      <div class="app-explore">
        <div>
          <ItemsLoaderLayout
            :itemsName="'poems'"
            :itemsFetcher="poemsFetcher"
            :reverse="true"
            :updateItemView="true"
          />
        </div>
      </div>
    </template>
  </MainLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {
  Page,
  Item,
} from '@/assets/scripts/types/interfaces';
import PoemAPIReq from '@/assets/scripts/api_requests/poem';
import MainLayout from '@/views/layout/Main.vue';
import ItemsLoaderLayout from '@/views/layout/ItemsLoader.vue';
import MagnifyIcon from '@/assets/icons/Magnify.vue';

@Component({
  name: 'ExploreView',
  components: {
    MainLayout,
    ItemsLoaderLayout,
    MagnifyIcon,
  },
})
export default class ExploreView extends Vue {
  searchQuery = '';

  poemAPIReq = new PoemAPIReq(
    this.$store.state.API_URL,
    this.$store.state.user.authToken,
  );

  search(): void {
    if (this.$route.params.q !== this.searchQuery) {
      this.$router.push(`/search/${this.searchQuery}`);
    }
  }

  poemsFetcher(page: Page): Promise<{
      success: boolean,
      data?: Array<Item>,
      message?: string
    }> {
    return this.poemAPIReq.getExploratoryPoems(page);
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/views/search";
</style>
