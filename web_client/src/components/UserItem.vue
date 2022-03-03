<template>
  <div class="user-item">
    <div>
      <a :href="`/profile/${user.id}`">
        <img :src="imageSrc" v-show="imageSrc.length > 0"/>
        <AccountIcon v-show="imageSrc.length === 0"/>
      </a>
    </div>
    <div>
      <a :href="`/profile/${user.id}`">
        {{ user.name }}
      </a>
    </div>
    <div>
      <button
        :class="{
          'cdp-btn': true,
          'text': true,
          danger: actionText === 'Unfollow',
          light: actionText === 'Follow',
          hidden: hideAction
        }"
        @click="toggleConnection"
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
import UserMin from '@/assets/scripts/types/user_min';
import ConnectionAPIReq from '@/assets/scripts/api_requests/connection';
import UserAPIReq from '@/assets/scripts/api_requests/user';
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

  imageSrc = '';

  hideAction = false;

  isFollowing = this.user.isFollowing;

  connection!: ConnectionAPIReq;

  userAPIReq!: UserAPIReq;

  loadProfilePhoto(): void {
    this.userAPIReq.getProfilePhoto(this.user.profilePhotoId)
      .then((res) => {
        if (res.success) {
          if (res.data) {
            this.imageSrc = `${res.data.url}?tr=w-38,h-38`;
          }
        }
      });
  }

  toggleConnection(): void {
    const userId = this.$store.state.user.id;
    const followId = this.user.id;
    this.connection.follow(userId, followId)
      .then((res) => {
        if (res.success) {
          if (res.data) {
            this.isFollowing = res.data.status;
            this.onMouseEnterAction();
          }
        } else if (res.message) {
          console.error(res.message);
        }
      });
  }

  onMouseEnterAction(): void {
    if (!this.hideAction) {
      this.actionText = this.user.isFollowing && this.isFollowing ? 'Unfollow' : 'Follow';
    }
  }

  onMouseLeaveAction(): void {
    if (!this.hideAction) {
      this.actionText = this.user.isFollowing && this.isFollowing ? 'Following' : 'Follow';
    }
  }

  mounted(): void {
    this.hideAction = this.user.id === this.$store.state.user.id;
    this.onMouseLeaveAction();
    this.connection = new ConnectionAPIReq(
      this.$store.state.API_URL,
      this.$store.state.user.authToken,
    );
    this.userAPIReq = new UserAPIReq(
      this.$store.state.API_URL,
      this.$store.state.user.authToken,
    );
    this.loadProfilePhoto();
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/components/user_item";
</style>
