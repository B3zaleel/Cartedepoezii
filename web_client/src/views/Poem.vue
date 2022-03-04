<template>
  <MainLayout>
    <template v-slot:header>
      <div class="header-pane">
        <div>
          <div>
            <button class="cdp-btn icon">
              <ArrowLeftIcon/>
            </button>
          </div>
          <div>
            <h1>Poem</h1>
          </div>
        </div>
      </div>
    </template>

    <template v-slot:main>
      <div class="user-poem">
        <div>
          <div v-show="!poemLoaded" class="loading-pane">
            <LoadingIcon/>
          </div>
          <div v-show="poemLoaded">
            <Poem :poem="poem"/>
          </div>
          <div v-show="poemLoaded">
            <ItemsLoaderLayout
              :itemsName="'comments'"
              :itemsFetcher="commentsFetcher"
            />
          </div>
        </div>
      </div>
    </template>
  </MainLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Page, Item } from '@/assets/scripts/types/interfaces';
import CommentAPIReq from '@/assets/scripts/api_requests/comment';
import PoemAPIReq from '@/assets/scripts/api_requests/poem';
import PoemT from '@/assets/scripts/types/poem';
import ArrowLeftIcon from '@/assets/icons/ArrowLeft.vue';
import LoadingIcon from '@/assets/icons/Loading.vue';
import MainLayout from '@/views/layout/Main.vue';
import ItemsLoaderLayout from '@/views/layout/ItemsLoader.vue';
import Poem from '@/components/Poem.vue';

@Component({
  name: 'PoemView',
  components: {
    ArrowLeftIcon,
    LoadingIcon,
    MainLayout,
    ItemsLoaderLayout,
    Poem,
  },
})
export default class PoemView extends Vue {
  poem: PoemT = new PoemT();

  poemLoaded = false;

  commentsSrc = '';

  commentsQueryParams = '';

  commentAPIReq = new CommentAPIReq(
    this.$store.state.API_URL,
    this.$store.state.user.authToken,
  );

  poemAPIReq = new PoemAPIReq(
    this.$store.state.API_URL,
    this.$store.state.user.authToken,
  );

  commentsFetcher(page: Page): Promise<{
      success: boolean,
      data?: Array<Item>,
      message?: string
    }> {
    return this.commentAPIReq.getPoemComments(this.$route.params.id, page);
  }

  loadPoem(): void {
    this.poemLoaded = false;
    this.poemAPIReq.getPoem(this.$route.params.id)
      .then((res) => {
        if (res.success) {
          if (res.data) {
            this.poem = res.data;
            document.title = `${this.poem.user.name}: ${this.poem.title} - Cartedepoezii`;
            this.poemLoaded = true;
          }
        }
      });
  }

  mounted(): void {
    this.loadPoem();
  }
}
</script>

<style lang="scss">
@use '@/assets/styles/views/poem';
</style>
