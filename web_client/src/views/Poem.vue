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
          <div>
            <Poem :poem="poem"/>
          </div>
          <div class="{loading: true}">
            <LoadingIcon/>
          </div>
        </div>
        <div>
          <div>
          </div>
        </div>
      </div>
    </template>
  </MainLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { UserMin, Poem as PoemT } from '@/assets/scripts/type_defs';
import ArrowLeftIcon from '@/assets/icons/ArrowLeft.vue';
import LoadingIcon from '@/assets/icons/Loading.vue';
import MainLayout from '@/views/layout/Main.vue';
import Poem from '@/components/Poem.vue';
import Comment from '@/components/Comment.vue';

@Component({
  name: 'PoemView',
  components: {
    ArrowLeftIcon,
    LoadingIcon,
    MainLayout,
    Poem,
    Comment,
  },
})
export default class PoemView extends Vue {
  poem = {
    id: 'ffjddfjf',
    publishedDate: new Date(),
    title: '',
    verses: ['T\xa0h\nis\nis\na d\nem\no wo\nrk', '4553\n\xa0\n\xa0\n\xa0\n\xa0\n\xa0\n\xa0...'],
    user: {
      id: 'lk-89iii',
      name: 'Beza',
      profilePhotoId: '',
      isFollowing: false,
    },
    isLiked: false,
    likesCount: 15,
    commentsCount: 5,
  };
}
</script>

<style lang="scss">
// @use '@/assets/styles/views/profile';
</style>
