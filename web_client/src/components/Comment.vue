<template>
  <div class="comment">
    <div class="heading">
      <div>
        <router-link to="/f">
          <img/>
          <AccountIcon/>
        </router-link>
      </div>
      <div>
        <router-link to="/f">
          {{ comment.user.name }}
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

    <div class="body">
      <p class="main">
        {{ comment.text }}
      </p>

      <div :class="{footer: true, visible: comment.repliesTo && showReplies}">
        <div>
          <button>
            <CommentIcon/>
          </button>
        </div>

        <div>
          <span>
            {{ comment.repliesCount > 1 ? `${comment.repliesCount} Replies` : '1 Reply' }}
          </span>
          <span>
            &nbsp;-&nbsp;{{ comment.createdDate.getFullYear() }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { UserMin, Comment } from '@/assets/scripts/type_defs';
import AccountIcon from '@/assets/icons/Account.vue';
import CommentIcon from '@/assets/icons/Comment.vue';
import DotsHorizontalIcon from '@/assets/icons/DotsHorizontal.vue';
import ContextMenuLayout from '@/views/layout/ContextMenu.vue';

@Component({
  name: 'CommentComponent',
  components: {
    AccountIcon,
    CommentIcon,
    DotsHorizontalIcon,
    ContextMenuLayout,
  },
})
export default class CommentComponent extends Vue {
  @Prop() commentId!: string;

  @Prop() showReplies!: boolean;

  comment!: Comment;

  isMenuOpen = false;

  openMenu(): void {
    this.isMenuOpen = true;
  }

  closeMenu(): void {
    this.isMenuOpen = false;
  }

  created(): void {
    const author : UserMin = {
      id: '4566-332',
      name: 'Marianna',
      profilePhotoId: '',
      isFollowing: false,
    };
    this.comment = {
      id: 'e45',
      user: author,
      poemId: '',
      text: 'This poem was awesome',
      createdDate: new Date(),
      repliesTo: '',
      repliesCount: 2,
    };
  }
}
</script>

<style lang="scss">
.comment {
  padding: 5px;
  border-top: 1px solid gainsboro;
  border-bottom: 1px solid gainsboro;

  > .heading {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    justify-content: center;
    column-gap: 5px;

    > div:nth-child(1) {
      > a {
        display: flex;
        align-items: center;
        justify-content: center;
        // width: 25px;
        padding: 2px;
        border: 2px solid greenyellow;
        border-radius: 50%;

        > svg {
          width: 30px;
          height: 30px;
        }
      }
    }

    > div:nth-child(2) {
      > a {
        text-decoration: none;
        white-space: nowrap;
        overflow: auto;
        text-overflow: ellipsis;
      }
    }

    > div:nth-child(3) {
      position: relative;

      > button {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 5px;
        background: none;
        border-radius: 50%;
        border: 1px solid transparent;
        cursor: pointer;
        transition-property: background;
        transition-duration: 300ms;
        transition-timing-function: cubic-bezier(0.39, 0.575, 0.565, 1);

        &:hover {
          border-color: gainsboro;
          background: rgb(172, 172, 172);
        }
      }
    }
  }

  > .body {
    margin: 0 40px;

    > .main {
      margin: 10px 0;
    }

    > .footer {
      display: none;
    }

    > .footer.visible {
      display: grid;
      grid-template-columns: auto 1fr;
      padding: 5px 5px 0 5px;
      justify-content: flex-start;
      align-items: center;
      border-top: 1px solid black;

      // > div:nth-child(1) {
      //   > button {
      //     display: none;
      //   }
      // }

      > div:nth-child(1) {
        > button {
          display: flex;
          padding: 5px;
          align-items: center;
          justify-content: center;
          background: none;
          border: 1px solid transparent;
          border-radius: 50%;
          cursor: pointer;
          outline: none;

          &:hover {
            border: 1px solid gainsboro;
          }
        }
      }

      > div:nth-child(2) {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        align-content: center;

        > span {
          padding: 0;
          margin: 0;
          background: none;
          border: none;
        }

        > span:nth-child(1) {
          cursor: pointer;

          &:hover {
            text-decoration: underline;
          }
        }
      }
    }
  }
}
</style>
