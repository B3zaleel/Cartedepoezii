<template>
  <MainLayout>
    <template v-slot:header>
      <div class="header-pane">
        <div class="page-nav-bar">
          <div>
            <button class="cdp-btn icon" @click="goBack">
              <ArrowLeftIcon/>
            </button>
          </div>
          <div>
            <h1>Comment</h1>
          </div>
        </div>
      </div>
    </template>

    <template v-slot:main>
      <div class="user-comment">
        <div>
          <div v-show="isLoadingComment" class="loading-pane">
            <LoadingIcon/>
          </div>

          <div v-show="commentLoadingFailed">
            <Error404View/>
          </div>

          <div v-show="commentLoaded">
            <Comment :comment="comment" v-for="comment in comments" :key="comment.id"/>
          </div>
          <div
            class="comment-replies-sect-divider"
            v-show="commentLoaded"
          ></div>
          <div v-show="commentLoaded">
            <ItemsLoaderLayout
              :itemsName="'comments'"
              :itemsFetcher="repliesFetcher"
              :reverse="true"
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
import CommentT from '@/assets/scripts/types/comment';
import ArrowLeftIcon from '@/assets/icons/ArrowLeft.vue';
import LoadingIcon from '@/assets/icons/Loading.vue';
import MainLayout from '@/views/layout/Main.vue';
import ItemsLoaderLayout from '@/views/layout/ItemsLoader.vue';
import Error404View from '@/views/error/_Error404.vue';
import Comment from '@/components/Comment.vue';

@Component({
  name: 'CommentView',
  components: {
    ArrowLeftIcon,
    LoadingIcon,
    MainLayout,
    ItemsLoaderLayout,
    Error404View,
    Comment,
  },
})
export default class CommentView extends Vue {
  comments: Array<CommentT> = [];

  isLoadingComment = true;

  commentLoaded = false;

  commentLoadingFailed = false;

  commentAPIReq = new CommentAPIReq(
    this.$store.state.API_URL,
    this.$store.state.user.authToken,
  );

  goBack(): void {
    if (this.comments[0].replyTo) {
      this.$router.push(`/comment/${this.comments[0].replyTo}`);
    } else {
      this.$router.push(`/poem/${this.comments[0].poemId}`);
    }
  }

  repliesFetcher(page: Page): Promise<{
      success: boolean,
      data?: Array<Item>,
      message?: string
    }> {
    const commentId = this.$route.params.id;
    return this.commentAPIReq.getCommentReplies(commentId, page);
  }

  loadComment(): void {
    this.isLoadingComment = true;
    this.commentLoaded = false;
    this.commentLoadingFailed = false;
    this.commentAPIReq.getComment(this.$route.params.id)
      .then((res) => {
        if (res.success) {
          if (res.data) {
            const n = this.comments.length;
            for (let i = 0; i < n; i += 1) {
              this.comments.pop();
            }
            this.comments.push(res.data);
            document.title = `Comment by ${res.data.user.name} - Cartedepoezii`;
            this.commentLoaded = true;
          }
        } else {
          document.title = 'Comment Not Found - Cartedepoezii';
          this.commentLoadingFailed = true;
        }
        this.isLoadingComment = false;
      });
  }

  created(): void {
    this.loadComment();
  }
}
</script>

<style lang="scss">
@use '@/assets/styles/views/comment';
</style>
