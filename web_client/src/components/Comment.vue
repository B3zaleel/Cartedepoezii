<template>
  <div class="comment">
    <div class="heading">
      <div>
        <router-link :to="`/profile/${comment.user.id}`">
          <img :src="imageSrc"/>
          <AccountIcon/>
        </router-link>
      </div>
      <div>
        <router-link :to="`/profile/${comment.user.id}`">
          {{ comment.user.name }}
        </router-link>
      </div>
      <div tabindex="1" @blur="closeMenu" v-show="canModifyComment">
        <button class="cdp-btn icon" @click.capture="openMenu">
          <DotsHorizontalIcon/>
        </button>
        <ContextMenuLayout
          :isMenuOpen="isMenuOpen"
          v-on:request-close="closeMenu"
          :position="actionMenuPos"
        >
          <div>
            <button class="menu-item danger" @click="openDeleteDialog">
              Delete
            </button>
          </div>
        </ContextMenuLayout>
      </div>
    </div>

    <div class="body">
      <p class="main">
        {{ comment.text }}
      </p>

      <div class="creation-time">
        {{ creationTime }}
      </div>
      <div :class="{footer: true, hidden: !canReply }">
        <div>
          <button class="cdp-btn icon reply-tgl-btn" @click="toggleReplyToComment">
            <CommentIcon v-show="isReplyingToComment"/>
            <CommentTextIcon v-show="!isReplyingToComment"/>
          </button>
        </div>

        <div>
          <router-link
            :to="`/comment/${comment.id}`"
            class="see-replies"
            v-show="canSeeReplies"
          >
            {{ repliesText }}
          </router-link>
        </div>
      </div>

      <div class="reply" v-show="isReplyingToComment">
        <textarea class="cdp-txb" v-model="reply"/>
        <div>
          <button class="cdp-btn text" @click="replyToComment">
            <LoadingIcon v-show="isReplyUploading"/>
            <b v-show="!isReplyUploading">Reply</b>
          </button>
        </div>
      </div>

      <ModalLayout
        :modalOpen="isDialogOpen"
        :modalTitle="dialogTitle"
        :hasHeader="true"
        v-on:request-close="closeDialog"
      >
        <template v-slot:modal-body>
          <div>
            <div v-show="dialogType === dialogTypes.Delete">
              <p>Are you sure you want to delete this comment?</p>
              <p v-show="comment.repliesCount > 0">
                This would delete {{ comment.repliesCount }} other comment(s) as well.
              </p>
            </div>
          </div>
        </template>

        <template v-slot:modal-action-panel>
          <div class="pane-container">
            <div v-show="dialogType === dialogTypes.Delete">
              <button class="cdp-btn text danger" @click="deleteComment">
                <LoadingIcon v-show="isDeletingComment"/>
                <b v-show="!isDeletingComment">Yes</b>
              </button>
            </div>
          </div>
        </template>
      </ModalLayout>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Position } from '@/assets/scripts/types/interfaces';
import Comment from '@/assets/scripts/types/comment';
import CommentAPIReq from '@/assets/scripts/api_requests/comment';
import UserAPIReq from '@/assets/scripts/api_requests/user';
import AccountIcon from '@/assets/icons/Account.vue';
import CommentIcon from '@/assets/icons/Comment.vue';
import CommentTextIcon from '@/assets/icons/CommentText.vue';
import DotsHorizontalIcon from '@/assets/icons/DotsHorizontal.vue';
import LoadingIcon from '@/assets/icons/Loading.vue';
import ContextMenuLayout from '@/views/layout/ContextMenu.vue';
import ItemsLoaderLayout from '@/views/layout/ItemsLoader.vue';
import ModalLayout from '@/views/layout/Modal.vue';
import DoughnutStatus from '@/components/DoughnutStatus.vue';

@Component({
  name: 'CommentComponent',
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
      const date = new Date(this.$props.comment.createdOn);
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
      const commentLocation = `/comment/${this.$props.comment.id}`;
      if (this.$route.path.startsWith(commentLocation)) {
        return `Created on ${month} ${monthDay}${ordinal} ${date.getUTCFullYear()}`;
      }
      return `Replied on ${month} ${monthDay}${ordinal} ${date.getUTCFullYear()}`;
    },
    repliesText() {
      if (this.$props.comment.repliesCount === 1) {
        return 'See 1 Reply';
      }
      if (this.$props.comment.repliesCount > 1) {
        return `See ${this.$props.comment.repliesCount} Replies`;
      }
      return '';
    },
    canSeeReplies() {
      const location = `/comment/${this.$props.comment.id}`;
      return this.$props.comment.repliesCount > 0 && !this.$route.path.startsWith(location);
    },
    canReply() {
      return this.$props.comment.replyTo.length === 0;
    },
  },
  components: {
    AccountIcon,
    CommentIcon,
    CommentTextIcon,
    DotsHorizontalIcon,
    LoadingIcon,
    ContextMenuLayout,
    ItemsLoaderLayout,
    ModalLayout,
    DoughnutStatus,
  },
})
export default class CommentComponent extends Vue {
  @Prop() comment!: Comment;

  actionMenuPos: Position = {
    type: 'absolute',
    right: '0',
    top: '0',
  };

  canModifyComment = this.comment.user.id === this.$store.state.user.id;

  isMenuOpen = false;

  poemRepliesCount = this.comment.repliesCount;

  reply = '';

  imageSrc = '';

  isReplyingToComment = false;

  isReplyUploading = false;

  isDeletingComment = false;

  isDialogOpen = false;

  dialogType = 0;

  dialogTypes = {
    None: 0,
    Delete: 2,
  };

  hasHeader = true;

  dialogTitle = '';

  commentAPIReq = new CommentAPIReq(
    this.$store.state.API_URL,
    this.$store.state.user.authToken,
  );

  userAPIReq = new UserAPIReq(
    this.$store.state.API_URL,
    this.$store.state.user.authToken,
  );

  openMenu(): void {
    this.isMenuOpen = true;
  }

  openDeleteDialog(): void {
    this.closeMenu();
    if (!this.isDeletingComment) {
      this.dialogType = this.dialogTypes.Delete;
      this.dialogTitle = 'Delete Comment';
      this.isDialogOpen = true;
    }
  }

  toggleReplyToComment(): void {
    this.isReplyingToComment = !this.isReplyingToComment;
  }

  closeMenu(): void {
    this.isMenuOpen = false;
  }

  closeDialog(): void {
    this.isDialogOpen = false;
  }

  loadProfilePhoto(): void {
    this.userAPIReq.getProfilePhoto(this.comment.user.profilePhotoId)
      .then((res) => {
        if (res.success) {
          if (res.data) {
            this.imageSrc = `${res.data.url}?tr=w-38,h-38`;
          }
        }
      });
  }

  replyToComment(): void {
    const userId = this.$store.state.user.id;
    const { poemId } = this.comment;
    const commentId = this.comment.id;
    this.isReplyUploading = true;
    this.commentAPIReq.createComment(poemId, userId, this.reply, commentId)
      .then((res) => {
        if (res.success) {
          this.reply = '';
        }
        this.isReplyUploading = false;
      }).catch(() => {
        this.isReplyUploading = false;
      });
  }

  deleteComment(): void {
    const userId = this.$store.state.user.id;
    const commentId = this.comment.id;
    this.isDeletingComment = true;
    this.commentAPIReq.deleteComment(userId, commentId)
      .then((res) => {
        if (res.success) {
          window.location.reload();
        } else {
          console.error(res.message);
        }
        this.isDeletingComment = false;
      }).catch(() => {
        this.isDeletingComment = false;
      });
  }

  mounted(): void {
    this.loadProfilePhoto();
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/components/comment";
</style>
