<template>
  <MainLayout>
    <template v-slot:header>
      <div class="header-pane">
        <h2>Home</h2>
      </div>
    </template>

    <template v-slot:main>
      <div class="user-home">
        <div>
          <ItemsLoaderLayout
            :itemsName="'poems'"
            :itemsFetcher="poemsFetcher"
          />
        </div>
      </div>
    </template>
  </MainLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Page, Item } from '@/assets/scripts/types/interfaces';
import PoemAPIReq from '@/assets/scripts/api_requests/poem';
import MainLayout from '@/views/layout/Main.vue';
import ItemsLoaderLayout from '@/views/layout/ItemsLoader.vue';

@Component({
  name: 'UserHomeView',
  components: {
    MainLayout,
    ItemsLoaderLayout,
  },
})
export default class UserHomeView extends Vue {
  poemAPIReq = new PoemAPIReq(
    this.$store.state.API_URL,
    this.$store.state.user.authToken,
  );

  poemsFetcher(page: Page): Promise<{
      success: boolean,
      data?: Array<Item>,
      message?: string
    }> {
    return this.poemAPIReq.getPoemsForUser(page);
  }
}
</script>

<style lang="scss">
.header-pane {
  > h2 {
    margin: 0;
    font-size: 1.2em;
    cursor: context-menu;
  }
}
</style>
