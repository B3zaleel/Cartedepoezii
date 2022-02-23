<template>
  <MainLayout>
    <template v-slot:header>
      <div class="header-pane">
        <div>
          <div>
            <button>
              <ArrowLeftIcon/>
            </button>
          </div>
          <div>
            <h2>{{ user.name }}</h2>
            <h5 class="">{{ getSubTitle() }}</h5>
          </div>
        </div>
      </div>
    </template>

    <template v-slot:main>
      <div class="user-profile">
        <div class="profile-info">
          <div>
            <div class="profile-photo-sect">
              <button class="image-view-btn">
                <AccountIcon/>
                <img :src="getProfilePhotoURL()" @error="imageLoadError"/>
              </button>

              <button class="account-action-btn">
                {{ actionText }}
              </button>
            </div>

            <div class="name-sect">
              {{ user.name }}
            </div>

            <div class="join-sect">
              <CalendarMonthIcon/>
              <span>{{ getJoinDate() }}</span>
            </div>

            <div class="connections-sect">
              <button>
                <b>{{ MathUtils.formatNumber(user.followersCount) }}</b>
                <b>Followers</b>
              </button>
              <button>
                <b>{{ MathUtils.formatNumber(user.followingsCount) }}</b>
                <b>Followings</b>
              </button>
            </div>

            <div class="bio-sect">
              {{ user.bio }}
            </div>
          </div>
        </div>

        <TabsLayout
          :items="tabItems"
          v-bind:selectedId="selectedId"
          v-on:select-tab="args => changeSelectedTab(args)"
        >
          <div v-show="selectedId == 1">
            Poems go here
            <Poem/>
          </div>
          <div v-show="selectedId == 2">
            Comments go here
            <Comment/>
          </div>
          <div v-show="selectedId == 3">
            Likes go here
          </div>
        </TabsLayout>
      </div>
    </template>
  </MainLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { User } from '@/assets/scripts/type_defs';
import MathUtils from '@/assets/scripts/math_utils';
import MainLayout from '@/views/layout/Main.vue';
import TabsLayout from '@/views/layout/Tabs.vue';
import Poem from '@/components/Poem.vue';
import Comment from '@/components/Comment.vue';
import ArrowLeftIcon from '@/assets/icons/ArrowLeft.vue';
import AccountIcon from '@/assets/icons/Account.vue';
import CalendarMonthIcon from '@/assets/icons/CalendarMonth.vue';

@Component({
  name: 'ProfileView',
  components: {
    MainLayout,
    TabsLayout,
    Poem,
    Comment,
    ArrowLeftIcon,
    AccountIcon,
    CalendarMonthIcon,
  },
})
export default class ProfileView extends Vue {
  actionText = '';

  MathUtils = MathUtils;

  tabItems = [
    {
      id: 1,
      title: 'Poems',
    },
    {
      id: 2,
      title: 'Comments',
    },
    {
      id: 3,
      title: 'Likes',
    },
  ];

  selectedId = 1;

  user!: User;

  imageLoadFailed = false;

  changeSelectedTab(tabId: number): void {
    this.selectedId = tabId;
  }

  imageLoadError(): void {
    this.imageLoadFailed = true;
  }

  getProfilePhotoURL(): string {
    const BASE_URL = this.$store.state.API_URL;
    return this.imageLoadFailed ? '' : `${BASE_URL}/profile-photo?id=${this.user.id}`;
  }

  getJoinDate(): string {
    const joinDateStr = this.user.joinDate;
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
    return `Joined ${months[joinDateStr.getMonth()]} ${joinDateStr.getFullYear()}`;
  }

  checkAction() {
    const options = ['Edit Profile', 'Unfollow', 'Follow'];
    let idx = -1;

    if (this.user.id === this.$store.state.user.id) {
      idx = 0;
    } else if (this.user.isFollowing) {
      idx = 1;
    } else {
      idx = 2;
    }
    return { id: idx, value: options[idx] };
  }

  getSubTitle(): string {
    switch (this.selectedId) {
      case 1: {
        const n = MathUtils.formatNumber(this.user.poemsCount, true);
        return `${n} Poems`;
      }
      case 2: {
        const n = MathUtils.formatNumber(this.user.commentsCount, true);
        return `${n} Comments`;
      }
      case 3: {
        const n = MathUtils.formatNumber(this.user.likesCount, true);
        return `${n} Likes`;
      }
      default:
        return '';
    }
  }

  created(): void {
    this.user = {
      id: this.$route.params.id,
      joinDate: new Date(),
      name: 'Beza',
      bio: '',
      profilePhotoId: '',
      followersCount: 0,
      followingsCount: 0,
      isFollowing: false,
      poemsCount: 0,
      likesCount: 0,
      commentsCount: 5,
    };
    this.actionText = this.checkAction().value;
  }

  // loadUserInfo() {}
}
</script>

<style lang="scss">
@use '@/assets/styles/views/profile';
</style>
