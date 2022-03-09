<template>
  <div class="poem" tabindex="0">
    <div>
      <div class="header">
        <div>
          <router-link :to="`/profile/${poem.user.id}`">
            <img :src="imageSrc"/>
            <AccountIcon/>
          </router-link>
        </div>
        <div>
          <router-link :to="`/profile/${poem.user.id}`">
            {{ poem.user.name }}
          </router-link>
        </div>
        <div tabindex="1" @blur="closeMenu" v-show="canModifyPoem">
          <button class="cdp-btn icon" @click.capture="openMenu">
            <DotsHorizontalIcon/>
          </button>
          <ContextMenuLayout
            :isMenuOpen="isMenuOpen"
            v-on:request-close="closeMenu"
            :position="actionMenuPos"
          >
            <div>
              <button class="menu-item" @click="openUpdateDialog">
                Edit
              </button>
              <button class="menu-item danger" @click="openDeleteDialog">
                Delete
              </button>
            </div>
          </ContextMenuLayout>
        </div>
      </div>

      <div class="main" @mousedown.self="openPoem">
        <h4>{{ poem.title }}</h4>

        <div :style="{'height': versesPHeight }">
          <button
            :class="{'nav-btn': true, left: true, hidden: currentVerse <= 1}"
            @click="previousVerse"
          >
            <ChevronLeftIcon/>
          </button>
          <p
            v-for="verse, idx in poem.verses"
            :key="idx"
            :class="{'verses-p': true, hidden: idx !== currentVerse - 1}"
          >{{ verse.trim() }}</p>
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

      <div class="creation-time">
        {{ creationTime }}
      </div>
      <div class="interactions">
        <div class="action-box">
          <button @click="toggleComment">
            <span>
              <CommentIcon v-show="isCommentingOnPoem"/>
              <CommentTextIcon v-show="!isCommentingOnPoem"/>
            </span>
          </button>
          <b>{{ MathUtils.formatNumber(poem.commentsCount, true) }}</b>
        </div>
        <div class="action-box">
          <button @click="reactToPoem" :class="{'like-btn': true, liked: isPoemLiked}">
            <span>
              <HeartOutlineIcon class="not-liked-icon"/>
              <HeartIcon class="liked-icon"/>
            </span>
          </button>
          <b>{{ MathUtils.formatNumber(poemLikesCount, true) }}</b>
        </div>
        <ModalLayout
          :modalOpen="isDialogOpen"
          :modalTitle="dialogTitle"
          :hasHeader="hasHeader"
          v-on:request-close="closeDialog"
        >
          <template v-slot:modal-body>
            <div>
              <div v-show="dialogType === dialogTypes.Edit">
                <PoemEdit
                  :poem="editPoemForm"
                  v-on:add-verse="args => addVerse(args)"
                  v-on:remove-verse="args => removeVerse(args)"
                />
              </div>
              <div v-show="dialogType === dialogTypes.Delete">
                <p>
                  Are you sure you want to delete this poem?
                </p>
              </div>
            </div>
          </template>

          <template v-slot:modal-action-panel>
            <div class="pane-container">
              <div v-show="dialogType === dialogTypes.Delete">
                <button class="cdp-btn text danger" @click="deletePoem">
                  <LoadingIcon v-show="isDeletingPoem"/>
                  <b v-show="!isDeletingPoem">Yes</b>
                </button>
              </div>
              <div v-show="dialogType === dialogTypes.Edit">
                <button class="cdp-btn text" @click="editPoem">
                  <LoadingIcon v-show="isEditUploading"/>
                  <b v-show="!isEditUploading">Done</b>
                </button>
              </div>
            </div>
          </template>
        </ModalLayout>
      </div>

      <div class="new-comment" v-show="isCommentingOnPoem">
        <textarea class="cdp-txb" v-model="comment" :maxlength="commentLimit"/>
        <div>
          <DoughnutStatus
            :value="comment.length / commentLimit"
            :titleValue="doughnutTitle"
          />
          <button class="cdp-btn text" @click="commentOnPoem">
            <LoadingIcon v-show="isCommentUploading"/>
            <b v-show="!isCommentUploading">Post</b>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Prop,
  Watch,
  Vue,
} from 'vue-property-decorator';
import { Position, EditPoemForm } from '@/assets/scripts/types/interfaces';
import Poem from '@/assets/scripts/types/poem';
import MathUtils from '@/assets/scripts/math_utils';
import CommentAPIReq from '@/assets/scripts/api_requests/comment';
import PoemAPIReq from '@/assets/scripts/api_requests/poem';
import UserAPIReq from '@/assets/scripts/api_requests/user';
import AccountIcon from '@/assets/icons/Account.vue';
import ChevronLeftIcon from '@/assets/icons/ChevronLeft.vue';
import ChevronRightIcon from '@/assets/icons/ChevronRight.vue';
import CommentIcon from '@/assets/icons/Comment.vue';
import CommentTextIcon from '@/assets/icons/CommentText.vue';
import HeartOutlineIcon from '@/assets/icons/HeartOutline.vue';
import HeartIcon from '@/assets/icons/Heart.vue';
import DotsHorizontalIcon from '@/assets/icons/DotsHorizontal.vue';
import LoadingIcon from '@/assets/icons/Loading.vue';
import ContextMenuLayout from '@/views/layout/ContextMenu.vue';
import ModalLayout from '@/views/layout/Modal.vue';
import PoemEdit from '@/components/PoemEdit.vue';
import DoughnutStatus from '@/assets/icons/animated/DoughnutStatus.vue';

@Component({
  name: 'PoemComponent',
  computed: {
    creationTime() {
      const months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December',
      ];
      const date = new Date(this.$props.poem.publishedOn);
      const month = months[date.getUTCMonth()];
      const monthDay = date.getUTCDate().toString();
      const [a, b] = [
        monthDay[monthDay.length - 1],
        monthDay[monthDay.length - 2],
      ];
      let ordinal = 'th';

      if ((a === '1') && (b !== '1')) {
        ordinal = 'st';
      } else if ((a === '2') && (b !== '1')) {
        ordinal = 'nd';
      } else if ((a === '3') && (b !== '1')) {
        ordinal = 'rd';
      }
      return `Published on ${month} ${monthDay}${ordinal} ${date.getUTCFullYear()}`;
    },
    doughnutTitle() {
      return `${this.$data.comment.length} / ${this.$data.commentLimit}`;
    },
  },
  components: {
    AccountIcon,
    ChevronLeftIcon,
    ChevronRightIcon,
    CommentIcon,
    CommentTextIcon,
    HeartOutlineIcon,
    HeartIcon,
    DotsHorizontalIcon,
    LoadingIcon,
    ContextMenuLayout,
    ModalLayout,
    PoemEdit,
    DoughnutStatus,
  },
})
export default class PoemComponent extends Vue {
  @Prop() poem!: Poem;

  @Prop() updateDisplay!: boolean;

  MathUtils = MathUtils;

  actionMenuPos: Position = {
    type: 'absolute',
    right: '0',
    top: '0',
  };

  editPoemForm: EditPoemForm = {
    poemId: this.poem.id,
    title: this.poem.title,
    verses: this.poem.verses,
  };

  commentAPIReq = new CommentAPIReq(
    this.$store.state.API_URL,
    this.$store.state.user.authToken,
  );

  poemAPIReq = new PoemAPIReq(
    this.$store.state.API_URL,
    this.$store.state.user.authToken,
  );

  userAPIReq = new UserAPIReq(
    this.$store.state.API_URL,
    this.$store.state.user.authToken,
  );

  canModifyPoem = this.poem.user.id === this.$store.state.user.id;

  isPoemLiked = this.poem.isLiked;

  poemLikesCount = this.poem.likesCount;

  poemCommentsCount = this.poem.commentsCount;

  comment = '';

  commentLimit = 384;

  imageSrc = '';

  currentVerse = 1;

  loadingPoem = false;

  loadingFailed = false;

  isCommentingOnPoem = false;

  isCommentUploading = false;

  isEditUploading = false;

  isDeletingPoem = false;

  isMenuOpen = false;

  versesPHeight = 'fit-content';

  isDialogOpen = false;

  dialogType = 0;

  dialogTypes = {
    None: 0,
    Comment: 1,
    Delete: 2,
    Edit: 3,
  };

  hasHeader = true;

  dialogTitle = '';

  @Watch('updateDisplay')
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  updateElementSizing(_old: boolean, _newVal: boolean): void {
    this.computeVersesPHeight();
  }

  computeVersesPHeight(): void {
    let versesHeight = 'fit-content';
    const versesP = this.$el?.firstElementChild?.children.item(1)?.children.item(1);
    if (versesP) {
      let maxHeight = 0;
      for (let i = 0; i < versesP.childElementCount; i += 1) {
        if (versesP.children.item(i)?.classList.contains('verses-p')) {
          const height = versesP.children.item(i)?.clientHeight;
          if (height && (height > maxHeight)) {
            maxHeight = height;
          }
        }
      }
      versesHeight = `${maxHeight + 2 * 5}px`;
    }
    this.versesPHeight = versesHeight;
  }

  openMenu(): void {
    this.isMenuOpen = true;
  }

  closeMenu(): void {
    this.isMenuOpen = false;
  }

  previousVerse(): void {
    if (this.currentVerse > 1) {
      this.currentVerse -= 1;
    }
  }

  nextVerse(): void {
    if (this.currentVerse !== this.poem?.verses.length) {
      this.currentVerse += 1;
    }
  }

  toggleComment(): void {
    this.isCommentingOnPoem = !this.isCommentingOnPoem;
  }

  openDeleteDialog(): void {
    this.closeMenu();
    if (!this.isDeletingPoem) {
      this.dialogType = this.dialogTypes.Delete;
      this.dialogTitle = 'Delete Poem';
      this.isDialogOpen = true;
    }
  }

  openUpdateDialog(): void {
    this.closeMenu();
    if (!this.isEditUploading) {
      this.dialogType = this.dialogTypes.Edit;
      this.dialogTitle = 'Edit Poem';
      this.editPoemForm = {
        poemId: this.poem.id,
        title: this.poem.title,
        verses: this.poem.verses,
      };
      this.isDialogOpen = true;
    }
  }

  closeDialog(): void {
    this.isDialogOpen = false;
  }

  openDeletePoemDialog(): void {
    this.dialogType = this.dialogTypes.Comment;
    this.isDialogOpen = true;
  }

  addVerse(versePos: number): void {
    const newVerses = [];
    for (let i = 0; i < this.editPoemForm.verses.length; i += 1) {
      newVerses.push(this.editPoemForm.verses[i]);
      if (i === versePos) {
        newVerses.push('');
      }
    }
    this.editPoemForm.verses = newVerses;
  }

  removeVerse(versePos: number): void {
    const newVerses = [];
    if (this.editPoemForm.verses.length === 1) {
      return;
    }
    for (let i = 0; i < this.editPoemForm.verses.length; i += 1) {
      if (i !== versePos) {
        newVerses.push(this.editPoemForm.verses[i]);
      }
    }
    this.editPoemForm.verses = newVerses;
  }

  loadProfilePhoto(): void {
    this.userAPIReq.getProfilePhoto(this.poem.user.profilePhotoId)
      .then((res) => {
        if (res.success) {
          if (res.data) {
            this.imageSrc = `${res.data.url}?tr=w-38,h-38`;
          }
        }
      });
  }

  commentOnPoem(): void {
    const poemId = this.poem.id;
    const userId = this.$store.state.user.id;
    this.isCommentUploading = true;
    this.commentAPIReq.createComment(poemId, userId, this.comment)
      .then((res) => {
        if (res.success) {
          this.comment = '';
        }
        this.isCommentUploading = false;
      }).catch(() => {
        this.isCommentUploading = false;
      });
  }

  reactToPoem(): void {
    const userId = this.$store.state.user.id;
    this.poemAPIReq.reactToPoem(userId, this.poem.id)
      .then((res) => {
        if (res.success) {
          if (res.data) {
            this.isPoemLiked = res.data.status;
            this.poemLikesCount += (res.data.status ? 1 : -1);
          }
        }
      });
  }

  deletePoem(): void {
    const userId = this.$store.state.user.id;
    this.isDeletingPoem = true;
    this.poemAPIReq.deletePoem(userId, this.poem.id)
      .then((res) => {
        if (res.success) {
          window.location.reload();
        } else {
          console.error(res.message);
        }
        this.isDeletingPoem = false;
      }).catch(() => {
        this.isDeletingPoem = false;
      });
  }

  editPoem(): void {
    const userId = this.$store.state.user.id;
    this.isEditUploading = true;
    const { verses, title } = this.editPoemForm;
    const poemId = this.poem.id;
    this.poemAPIReq.updatePoem(userId, poemId, title, verses)
      .then((res) => {
        if (!res.success) {
          console.error(res.message);
        }
        this.isEditUploading = false;
        this.closeDialog();
      }).catch(() => {
        this.isEditUploading = false;
      });
  }

  openPoem(): void {
    const location = `/poem/${this.poem.id}`;
    if (!this.$route.path.startsWith(location)) {
      this.$router.push(`/poem/${this.poem.id}`);
    }
  }

  mounted(): void {
    this.isPoemLiked = this.poem.isLiked;
    this.poemLikesCount = this.poem.likesCount;
    this.poemCommentsCount = this.poem.commentsCount;
    this.loadProfilePhoto();
    this.computeVersesPHeight();
    window.addEventListener('resize', () => {
      this.computeVersesPHeight();
    });
  }
}
</script>

<style lang="scss">
@use '@/assets/styles/components/poem';
</style>
