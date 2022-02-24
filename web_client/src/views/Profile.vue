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

              <button class="account-action-btn" @click="execAction">
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
              <button @click="viewFollowers">
                <b>{{ MathUtils.formatNumber(user.followersCount) }}</b>
                <b>Followers</b>
              </button>
              <button @click="viewFollowings">
                <b>{{ MathUtils.formatNumber(user.followingsCount) }}</b>
                <b>Followings</b>
              </button>
            </div>

            <div class="bio-sect" v-show="user.bio.length > 0">
              {{ user.bio }}
            </div>
          </div>
        </div>

        <ModalLayout
          :modalOpen="openDialog"
          :modalTitle="dialogTitle"
          :hasHeader="hasHeader"
          v-on:request-close="closeDialog"
        >
          <template v-slot:modal-body>
            <div>
              <div class="followers" v-show="dialogState === DialogStates.Followers">
                <UserItem :user="userTest"/>
              </div>
              <div class="followings" v-show="dialogState === DialogStates.Followings">
                <UserItem :user="userTest"/>
              </div>
              <div class="edit-profile" v-show="dialogState === DialogStates.EditProfile">
                <EditProfileView :user="user"/>
              </div>
              <!-- <div class="followings" v-show="dialogState === DialogStates.ProfilePhoto">
                <UserItem :user="userTest"/>
              </div> -->
            </div>
          </template>

          <template v-slot:modal-action-panel>
            <div v-show="dialogState === DialogStates.EditProfile">
              <div>
                <button>
                  Save
                </button>
              </div>
            </div>
          </template>
        </ModalLayout>

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
import { User, UserMin } from '@/assets/scripts/type_defs';
import MathUtils from '@/assets/scripts/math_utils';
import MainLayout from '@/views/layout/Main.vue';
import TabsLayout from '@/views/layout/Tabs.vue';
import ModalLayout from '@/views/layout/Modal.vue';
import Poem from '@/components/Poem.vue';
import Comment from '@/components/Comment.vue';
import UserItem from '@/components/UserItem.vue';
import ArrowLeftIcon from '@/assets/icons/ArrowLeft.vue';
import AccountIcon from '@/assets/icons/Account.vue';
import CalendarMonthIcon from '@/assets/icons/CalendarMonth.vue';
import EditProfileView from './settings/EditProfile.vue';

@Component({
  name: 'ProfileView',
  components: {
    MainLayout,
    TabsLayout,
    ModalLayout,
    EditProfileView,
    Poem,
    Comment,
    UserItem,
    ArrowLeftIcon,
    AccountIcon,
    CalendarMonthIcon,
  },
})
export default class ProfileView extends Vue {
  actionText = '';

  hasHeader = true;

  hasFooter = true;

  dialogTitle = '';

  openDialog = false;

  dialogState!: number;

  DialogStates = {
    None: 0,
    Followers: 1,
    Followings: 2,
    EditProfile: 3,
    ProfilePhoto: 4,
  }

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

  userTest!: UserMin;

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

  onMouseEnterAction(): void {
    if (this.user.id === this.$store.state.user.id) {
      this.actionText = 'Edit Profile';
    } else if (this.user.isFollowing) {
      this.actionText = 'Unfollow';
    } else {
      this.actionText = 'Follow';
    }
  }

  onMouseLeaveAction(): void {
    if (this.user.id === this.$store.state.user.id) {
      this.actionText = 'Edit Profile';
    } else if (this.user.isFollowing) {
      this.actionText = 'Following';
    } else {
      this.actionText = 'Follow';
    }
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

  execAction(): void {
    let actionId = -1;
    if (this.user.id === this.$store.state.user.id) {
      actionId = 0;
    } else if (this.user.isFollowing) {
      actionId = 1;
    } else {
      actionId = 2;
    }
    switch (actionId) {
      case 0: {
        this.viewEditProfile();
        break;
      }
      default:
        break;
    }
  }

  viewFollowers(): void {
    this.openDialog = true;
    this.dialogTitle = 'Followed by';
    this.hasHeader = true;
    this.hasFooter = false;
    this.dialogState = this.DialogStates.Followers;
  }

  viewFollowings(): void {
    this.openDialog = true;
    this.dialogTitle = 'Following';
    this.hasHeader = true;
    this.hasFooter = false;
    this.dialogState = this.DialogStates.Followings;
  }

  viewEditProfile(): void {
    this.openDialog = true;
    this.dialogTitle = 'Edit Profile';
    this.hasHeader = true;
    this.hasFooter = true;
    this.dialogState = this.DialogStates.EditProfile;
  }

  closeDialog(): void {
    this.openDialog = false;
  }

  created(): void {
    this.user = {
      id: this.$route.params.id,
      joinDate: new Date(),
      name: 'Beza',
      email: 'Beza',
      bio: '',
      profilePhotoId: '',
      followersCount: 0,
      followingsCount: 0,
      isFollowing: false,
      poemsCount: 0,
      likesCount: 0,
      commentsCount: 5,
    };
    this.userTest = {
      id: 'fggiish-',
      name: 'John',
      profilePhotoId: '455',
      isFollowing: false,
    };
    if (this.user.id === this.$store.state.user.id) {
      this.actionText = 'Edit Profile';
    } else if (this.user.isFollowing) {
      this.actionText = 'Following';
    } else {
      this.actionText = 'Follow';
    }
    this.dialogState = this.DialogStates.None;
  }

  // loadUserInfo() {}
}
</script>

<style lang="scss">
@use '@/assets/styles/views/profile';
</style>
