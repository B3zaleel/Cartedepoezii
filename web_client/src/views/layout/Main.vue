<template>
  <main class="main-layout">
    <div class="left-pane" id="left-pane_main-layout">
      <div>
        <div class="logo-pane">
          <CartedepoeziiLogo/>
        </div>

        <div class="nav-pane">
          <router-link
            :class="{'nav-btn': true, selected: isSelectedBtn('home')}"
            to="/"
          >
            <span>
              <CollageIcon/>
              <b>Home</b>
            </span>
          </router-link>
          <router-link
            :class="{'nav-btn': true, selected: isSelectedBtn('explore')}"
            to="/explore"
          >
            <span>
              <CompassIcon/>
              <b>Explore</b>
            </span>
          </router-link>
          <a
            :class="{'nav-btn': true, selected: isSelectedBtn('profile')}"
            :href="`/profile/${$store.state.user.id}`"
          >
            <span>
              <AccountIcon/>
              <b>Profile</b>
            </span>
          </a>
          <div tabindex="1" @blur="closeMoreMenu">
            <button class="nav-btn" @click.stop="openMoreMenu">
              <span>
                <DotsHorizontalCircleOutlineIcon/>
                <b>More</b>
              </span>
            </button>
          </div>
        </div>

        <div class="cta-sect">
          <button @click="openPoemDialog">
            <PenIcon/>
            <b>Poetize</b>
          </button>
        </div>
      </div>
    </div>

    <div class="center-pane">
      <div>
        <slot name="header"></slot>
        <div></div>
      </div>

      <div>
        <ContextMenuLayout
          :position="moreMenuPos"
          :isMenuOpen="isMoreMenuOpen"
          v-on:request-close="closeMoreMenu"
        >
          <div>
            <div class="info-sect">
              <router-link class="menu-item" to="/terms-of-service">
                Terms of Service
              </router-link>
              <router-link class="menu-item" to="/privacy-policy">
                Privacy Policy
              </router-link>
              <router-link class="menu-item" to="/about">
                About
              </router-link>
            </div>
            <button class="menu-item" @click="signOut">
              Sign Out
            </button>
            <button class="menu-item danger" @click="deleteAccount">
              Delete Account
            </button>
          </div>
        </ContextMenuLayout>
        <slot name="main"></slot>
          <ModalLayout
            :modalOpen="isWritingPoem"
            :modalTitle="dialogTitle"
            :hasHeader="hasHeader"
            v-on:request-close="closeDialog"
          >
            <template v-slot:modal-body>
              <div>
                <PoemEdit
                  :poem="newPoem"
                  v-on:add-verse="args => addVerse(args)"
                  v-on:remove-verse="args => removeVerse(args)"
                />
              </div>
            </template>

            <template v-slot:modal-action-panel>
              <div>
                <div>
                  <button class="cdp-btn text" @click="createPoem">
                    Done
                  </button>
                </div>
              </div>
            </template>
          </ModalLayout>
      </div>
    </div>

    <div class="right-pane" id="right-pane_main-layout">
      <div>
        <div :class="{search: true, hidden: canHideSearchPanel()}">
          <input
            placeholder="Search Cartedepoezii"
            v-model="searchQuery"
            @keydown.enter="searchSite"
          />
          <button class="cdp-btn icon" @click="searchSite">
            <MagnifyIcon/>
          </button>
        </div>

        <div class="info">
          <router-link to="/terms-of-service">Terms of Service</router-link>
          <router-link to="/privacy-policy">Privacy Policy</router-link>
          <router-link to="/about">About</router-link>
          <span>
            &copy; {{ new Date().getFullYear() }} Cartedepoezii
          </span>
        </div>
      </div>
    </div>
  </main>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { EditPoemForm, Position, PointerClickEvent } from '@/assets/scripts/types/interfaces';
import UserAPIReq from '@/assets/scripts/api_requests/user';
import PoemAPIReq from '@/assets/scripts/api_requests/poem';
import PoemEdit from '@/components/PoemEdit.vue';
import CartedepoeziiLogo from '@/assets/icons/Logo.vue';
import CollageIcon from '@/assets/icons/Collage.vue';
import CompassIcon from '@/assets/icons/Compass.vue';
import AccountIcon from '@/assets/icons/Account.vue';
import DotsHorizontalCircleOutlineIcon from '@/assets/icons/DotsHorizontalCircleOutline.vue';
import PenIcon from '@/assets/icons/Pen.vue';
import MagnifyIcon from '@/assets/icons/Magnify.vue';
import ModalLayout from './Modal.vue';
import ContextMenuLayout from './ContextMenu.vue';

@Component({
  name: 'MainLayout',
  components: {
    ModalLayout,
    ContextMenuLayout,
    PoemEdit,
    CartedepoeziiLogo,
    CollageIcon,
    CompassIcon,
    AccountIcon,
    DotsHorizontalCircleOutlineIcon,
    PenIcon,
    MagnifyIcon,
  },
})
export default class MainLayout extends Vue {
  isMoreMenuOpen = false;

  moreMenuPos: Position = {
    type: 'fixed',
    left: '0',
    bottom: '0',
  };

  isWritingPoem = false;

  hasHeader = true;

  dialogTitle = 'Create Poem';

  searchQuery = '';

  newPoem: EditPoemForm = {
    poemId: '',
    title: '',
    verses: [''],
  };

  poemAPIReq = new PoemAPIReq(
    this.$store.state.API_URL,
    this.$store.state.user.authToken,
  );

  userAPIReq = new UserAPIReq(
    this.$store.state.API_URL,
    this.$store.state.user.authToken,
  );

  adjustPanes = (): void => {
    const leftPane = document.getElementById('left-pane_main-layout');
    const rightPane = document.getElementById('right-pane_main-layout');
    const dialogPane = document.getElementById('top-dialog');

    if (leftPane) {
      // const childHeight = leftPane.clientHeight;
      const child = leftPane.getElementsByTagName('div').item(0);

      // console.log(leftPane.scrollHeight, leftPane.clientHeight);
      leftPane.style.height = `${window.innerHeight}px`;
      if (child) {
        child.style.height = `${window.innerHeight}px`;
      }
    }
    if (rightPane) {
      // const childHeight = rightPane.clientHeight;
      const child = rightPane.getElementsByTagName('div').item(0);

      rightPane.style.height = `${window.innerHeight}px`;
      if (child) {
        child.style.height = `${window.innerHeight}px`;
      }
    }
    if (dialogPane) {
      dialogPane.style.height = `${window.innerHeight}px`;
    }
  };

  isSelectedBtn(name: string): boolean {
    const userId = this.$store.state.user.id;
    switch (name) {
      case 'home':
        return window.location.pathname === '/';
      case 'explore':
        return window.location.pathname.startsWith('/explore');
      case 'profile':
        return window.location.pathname === `/profile/${userId}`;
      default:
        break;
    }
    return false;
  }

  canHideSearchPanel(): boolean {
    if (this.$route.path.startsWith('/search')) {
      return true;
    }
    return this.$route.path.startsWith('/explore');
  }

  openMoreMenu(ev: PointerClickEvent): void {
    console.dir(ev.target);
    let button = null;
    const el = ev.target;
    let leftPos = ev.clientX;
    let bottomPos = ev.clientY;
    if (el.nodeName === 'SPAN') {
      button = el.parentElement;
    } else if (el.nodeName === 'svg' || el.nodeName === 'B') {
      button = el.parentElement?.parentElement;
    } else if (el.nodeName === 'path') {
      button = el.parentElement?.parentElement?.parentElement;
    } else {
      button = el;
    }
    if (button) {
      leftPos = button.clientWidth;
      bottomPos = window.innerHeight - button.offsetTop - 1.5 * button.clientHeight;
    }
    this.moreMenuPos.left = `${leftPos}px`;
    this.moreMenuPos.bottom = `${bottomPos}px`;
    this.isMoreMenuOpen = true;
  }

  closeMoreMenu(): void {
    this.isMoreMenuOpen = false;
  }

  openPoemDialog(): void {
    let isEditActive = false;

    if (this.newPoem.title.length > 0) {
      isEditActive = true;
    }
    if (this.newPoem.verses.some((obj) => obj.length > 0)) {
      isEditActive = true;
    }
    if (!isEditActive) {
      this.newPoem = {
        poemId: '',
        title: '',
        verses: [''],
      };
    }
    this.isWritingPoem = true;
  }

  closeDialog(): void {
    this.isWritingPoem = false;
  }

  searchSite(): void {
    this.$router.push(`/search/${this.searchQuery}`);
  }

  addVerse(versePos: number): void {
    const newVerses = [];
    for (let i = 0; i < this.newPoem.verses.length; i += 1) {
      newVerses.push(this.newPoem.verses[i]);
      if (i === versePos) {
        newVerses.push('');
      }
    }
    this.newPoem.verses = newVerses;
  }

  removeVerse(versePos: number): void {
    const newVerses = [];
    if (this.newPoem.verses.length === 1) {
      return;
    }
    for (let i = 0; i < this.newPoem.verses.length; i += 1) {
      if (i !== versePos) {
        newVerses.push(this.newPoem.verses[i]);
      }
    }
    this.newPoem.verses = newVerses;
  }

  createPoem(): void {
    const userId = this.$store.state.user.id;
    const { verses } = this.newPoem;
    this.poemAPIReq.createPoem(userId, this.newPoem.title, verses)
      .then((res) => {
        if (res.success) {
          //
        }
      });
  }

  signOut(): void {
    this.$store.commit('signOut');
    this.$router.push('/');
  }

  deleteAccount(): void {
    this.userAPIReq.deleteUser(this.$store.state.user.id)
      .then((res) => {
        if (res.success) {
          this.$router.push('/');
        }
      });
  }

  mounted(): void {
    this.adjustPanes();
    window.addEventListener('resize', () => {
      this.adjustPanes();
    });
    // disable scrolling of the main layout if the dialog is open
    const dialogPane = document.getElementById('top-dialog');
    if (dialogPane && dialogPane.parentElement) {
      dialogPane.parentElement.addEventListener('mousewheel', (ev) => {
        // console.log('scrolling');
        if (dialogPane.style.display !== 'none') {
          ev.preventDefault();
        }
      }, false);
    }
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/views/layout/main";
</style>
