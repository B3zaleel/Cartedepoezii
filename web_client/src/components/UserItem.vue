<template>
  <div class="user-item">
    <div>
      <router-link to="/f">
        <img/>
        <AccountIcon/>
      </router-link>
    </div>
    <div>
      <router-link to="/f">
        {{ user.name }}
      </router-link>
    </div>
    <div>
      <button
        :class="{danger: actionText === 'Unfollow'}"
        @mouseenter="onMouseEnterAction"
        @mouseleave="onMouseLeaveAction"
      >
        {{ actionText }}
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { UserMin } from '@/assets/scripts/type_defs';
import AccountIcon from '@/assets/icons/Account.vue';

@Component({
  name: 'UserItemComponent',
  components: {
    AccountIcon,
  },
})
export default class UserItemComponent extends Vue {
  @Prop() user!: UserMin;

  actionText = '';

  hideAction = false;

  onMouseEnterAction(): void {
    if (!this.hideAction) {
      this.actionText = this.user.isFollowing ? 'Unfollow' : 'Follow';
    }
  }

  onMouseLeaveAction(): void {
    if (!this.hideAction) {
      this.actionText = this.user.isFollowing ? 'Following' : 'Follow';
    }
  }

  created(): void {
    this.hideAction = this.user.id === this.$store.state.user.id;
    this.onMouseLeaveAction();
  }
}
</script>

<style lang="scss">
.user-item {
  display: grid;
  padding: 5px;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  justify-content: center;
  column-gap: 5px;
  border-bottom: 2px solid gainsboro;

  &:first-child{
    border-top: none;
  }

  &:last-child{
    border-bottom: none;
  }

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
      border-radius: 15px;
      border: 1px solid gainsboro;
      cursor: pointer;
      transition-property: background;
      transition-duration: 300ms;
      transition-timing-function: cubic-bezier(0.39, 0.575, 0.565, 1);

      &:hover {
        background: rgb(204, 204, 204);
      }

      &.danger {
        background: #eb5757;
      }
    }
  }
}
</style>
