<template>
  <div class="poem" tabindex="0">
    <div :class="{sect: true, active: loadingPoem}">
      <LoadingIcon/>
    </div>

    <div :class="{sect: true, active: !loadingPoem && loadingFailed}">
      <h4>Failed to load poem</h4>
      <button class="btn-link" @click="loadPoem">
        <RefreshIcon/>
        <b>Retry</b>
      </button>
    </div>

    <div :class="{sect: true, active: !loadingPoem && !loadingFailed}">
      <div class="header">
        <div>
          <router-link to="/f">
            <img/>
            <AccountIcon/>
          </router-link>
        </div>
        <div>
          <router-link to="/f">
            {{ poem.user.name }}
          </router-link>
        </div>
        <div tabindex="1" @blur="closeMenu">
          <button @click.capture="openMenu">
            <DotsHorizontalIcon/>
          </button>
          <ContextMenuLayout
            :isMenuOpen="isMenuOpen"
            v-on:request-close="closeMenu"
          >
            <div>
              <button class="menu-item">
                Delete
              </button>
            </div>
          </ContextMenuLayout>
        </div>
      </div>

      <div class="main">
        <h4>{{ poem.title }}</h4>

        <div>
          <button
            :class="{'nav-btn': true, left: true, hidden: currentVerse <= 1}"
            @click="previousVerse"
          >
            <ChevronLeftIcon/>
          </button>
          <p>
            {{ poem.verses[currentVerse - 1] }}
          </p>
          <button
            :class="{'nav-btn': true, right: true, hidden: currentVerse >= poem.verses.length}"
            @click="nextVerse">
            <ChevronRightIcon/>
          </button>

          <span :class="{'page-info': true, hidden: poem.verses.length <= 1}">
            {{ currentVerse }} / {{ poem.verses.length }}
          </span>
        </div>
      </div>

      <div class="interactions">
        <button>
          <span>
            <CommentTextOutlineIcon/>
          </span>
          <b>{{ 6 }}</b>
        </button>
        <button>
          <span>
            <HeartOutlineIcon/>
          </span>
          <b>{{ 5 }}</b>
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { UserMin, Poem } from '@/assets/scripts/type_defs';
import AccountIcon from '@/assets/icons/Account.vue';
import ChevronLeftIcon from '@/assets/icons/ChevronLeft.vue';
import ChevronRightIcon from '@/assets/icons/ChevronRight.vue';
import CommentTextOutlineIcon from '@/assets/icons/CommentTextOutline.vue';
import LoadingIcon from '@/assets/icons/Loading.vue';
import HeartOutlineIcon from '@/assets/icons/HeartOutline.vue';
import RefreshIcon from '@/assets/icons/Refresh.vue';
import DotsHorizontalIcon from '@/assets/icons/DotsHorizontal.vue';
import ContextMenuLayout from '@/views/layout/ContextMenu.vue';

@Component({
  name: 'PoemComponent',
  components: {
    AccountIcon,
    LoadingIcon,
    RefreshIcon,
    ChevronLeftIcon,
    ChevronRightIcon,
    CommentTextOutlineIcon,
    HeartOutlineIcon,
    DotsHorizontalIcon,
    ContextMenuLayout,
  },
})
export default class PoemComponent extends Vue {
  @Prop() poemId!: string;

  poem!: Poem;

  currentVerse = 1;

  loadingPoem = false;

  loadingFailed = false;

  isMenuOpen = false;

  openMenu(): void {
    this.isMenuOpen = true;
  }

  closeMenu(): void {
    this.isMenuOpen = false;
  }

  loadPoem(): void {
    const BASE_URL = this.$store.state.API_URL;

    // this.loadingPoem = true;
    // fetch(`${BASE_URL}/poem/${this.poemId}`, {
    //   method: 'GET',
    //   mode: 'no-cors',
    //   headers: {
    //     'Content-Type': 'application/json',
    //   },
    // })
    //   .then((response) => response.json())
    //   .then((res) => {
    //     if (res.code === 200) {
    //       //
    //     } else {
    //       // show error info
    //       console.log(res.message);
    //     }
    //     this.loadingPoem = false;
    //   }).catch((err) => {
    //     if (err) {
    //       this.loadingPoem = false;
    //     }
    //   });
  }

  previousVerse(): void {
    if (this.currentVerse > 1) {
      this.currentVerse -= 1;
    }
  }

  nextVerse(): void {
    if (this.currentVerse !== this.poem.verses.length) {
      this.currentVerse += 1;
    }
  }

  deletePoem(): void {
    const BASE_URL = this.$store.state.API_URL;
  }

  updatePoem(): void {
    const BASE_URL = this.$store.state.API_URL;
  }

  openPoem(): void {
    this.$router.push(`/poem/${this.poemId}`);
  }

  created(): void {
    const author: UserMin = {
      id: 'lk-89iii',
      name: 'Beza',
      profilePhotoId: '',
      isFollowing: false,
    };
    this.poem = {
      id: this.poemId,
      publishedDate: new Date(),
      title: '',
      verses: [],
      user: author,
      isLiked: false,
      likesCount: 0,
      commentsCount: 5,
    };
    this.loadPoem();
  }
}
</script>

<style lang="scss">
@use '@/assets/styles/components/poem';
</style>
