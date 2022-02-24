<template>
  <main class="main-layout">
    <div class="left-pane" id="left-pane_main-layout">
      <div>
        <div class="logo-pane">
          <CartedepoeziiLogo/>
        </div>

        <div>
          <router-link
            :class="{'nav-btn': true, selected: isSelectedBtn('home')}"
            to="/"
          >
            <span>
              <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="mdi-collage" width="24" height="24" viewBox="0 0 24 24"><path d="M5,3C3.89,3 3,3.89 3,5V19C3,20.11 3.89,21 5,21H11V3M13,3V11H21V5C21,3.89 20.11,3 19,3M13,13V21H19C20.11,21 21,20.11 21,19V13" /></svg>
              <b>Home</b>
            </span>
          </router-link>
          <router-link
            :class="{'nav-btn': true, selected: isSelectedBtn('explore')}"
            to="/explore"
          >
            <span>
              <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="mdi-compass" width="24" height="24" viewBox="0 0 24 24"><path d="M14.19,14.19L6,18L9.81,9.81L18,6M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,10.9A1.1,1.1 0 0,0 10.9,12A1.1,1.1 0 0,0 12,13.1A1.1,1.1 0 0,0 13.1,12A1.1,1.1 0 0,0 12,10.9Z" /></svg>
              <b>Explore</b>
            </span>
          </router-link>
          <router-link
            :class="{'nav-btn': true, selected: isSelectedBtn('profile')}"
            :to="`/profile/${$store.state.user.id}`"
          >
            <span>
              <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="mdi-account" width="24" height="24" viewBox="0 0 24 24"><path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" /></svg>
              <b>Profile</b>
            </span>
          </router-link>
          <button class="nav-btn">
            <span>
              <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="mdi-dots-horizontal-circle-outline" width="24" height="24" viewBox="0 0 24 24"><path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,10.5A1.5,1.5 0 0,1 13.5,12A1.5,1.5 0 0,1 12,13.5A1.5,1.5 0 0,1 10.5,12A1.5,1.5 0 0,1 12,10.5M7.5,10.5A1.5,1.5 0 0,1 9,12A1.5,1.5 0 0,1 7.5,13.5A1.5,1.5 0 0,1 6,12A1.5,1.5 0 0,1 7.5,10.5M16.5,10.5A1.5,1.5 0 0,1 18,12A1.5,1.5 0 0,1 16.5,13.5A1.5,1.5 0 0,1 15,12A1.5,1.5 0 0,1 16.5,10.5Z" /></svg>
              <b>More</b>
            </span>
          </button>
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
        <slot name="main"></slot>
          <ModalLayout
            :modalOpen="isWritingPoem"
            :modalTitle="dialogTitle"
            :hasHeader="hasHeader"
            v-on:request-close="closeDialog"
          >
            <template v-slot:modal-body>
              <div>
                <PoemEdit/>
              </div>
            </template>

            <template v-slot:modal-action-panel>
              <div>
                <div>
                  <button>
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
        <div></div>

        <div>
          This is the right pane
        </div>
      </div>
    </div>
  </main>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import PoemEdit from '@/components/PoemEdit.vue';
import CartedepoeziiLogo from '@/assets/icons/Logo.vue';
import PenIcon from '@/assets/icons/Pen.vue';
import ModalLayout from './Modal.vue';

@Component({
  name: 'MainLayout',
  methods: {
    isSelectedBtn(name) {
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
    },
  },
  // watch: {},
  components: {
    ModalLayout,
    PoemEdit,
    CartedepoeziiLogo,
    PenIcon,
  },
})
export default class MainLayout extends Vue {
  isWritingPoem = false;

  hasHeader = true;

  dialogTitle = 'Create Poem';

  adjustPanes = (): void => {
    const leftPane = document.getElementById('left-pane_main-layout');
    const rightPane = document.getElementById('right-pane_main-layout');
    const dialogPane = document.getElementById('top-dialog');

    if (leftPane) {
      const childHeight = leftPane.clientHeight;
      const child = leftPane.getElementsByTagName('div').item(0);

      // console.log(leftPane.scrollHeight, leftPane.clientHeight);
      leftPane.style.height = `${window.innerHeight}px`;
      if (child) {
        child.style.height = `${window.innerHeight}px`;
      }
    }
    if (rightPane) {
      const childHeight = rightPane.clientHeight;
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

  openPoemDialog(): void {
    this.isWritingPoem = true;
  }

  closeDialog(): void {
    this.isWritingPoem = false;
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/views/layout/main";
</style>
