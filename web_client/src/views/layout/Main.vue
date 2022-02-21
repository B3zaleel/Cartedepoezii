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

    <div
      class="poem-post-dialog"
      id="top-dialog"
      v-show="isDialogOpen"
      @mousedown.self="closeDialog"
    >
      <div>
        <slot name="dialog" v-on:request-open-dialog="openDialog"></slot>
        <div v-show="isWritingPoem">
          <PoemEdit/>
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
    PoemEdit,
    CartedepoeziiLogo,
    PenIcon,
  },
})
export default class MainLayout extends Vue {
  isWritingPoem = false;

  isDialogOpen = false;

  adjustPanes = (): void => {
    const leftPane = document.getElementById('left-pane_main-layout');
    const rightPane = document.getElementById('right-pane_main-layout');
    const dialogPane = document.getElementById('top-dialog');

    if (leftPane) {
      const childHeight = leftPane.clientHeight;
      const child = leftPane.childNodes.item(0);

      leftPane.style.height = `${window.innerHeight}px`;
      if (child) {
        child.style.height = `${childHeight}px`;
      }
    }
    if (rightPane) {
      const childHeight = rightPane.clientHeight;
      const child = rightPane.childNodes.item(0);

      rightPane.style.height = `${window.innerHeight}px`;
      if (child) {
        child.style.height = `${childHeight}px`;
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
    this.openDialog();
  }

  openDialog(): void {
    this.isDialogOpen = true;
  }

  closeDialog(): void {
    this.isWritingPoem = false;
    this.isDialogOpen = false;
    this.$emit('dialog-closed');
  }
}
</script>

<style lang="scss">
.main-layout {
  display: grid;
  grid-template-areas: "left center right";
  grid-template-columns: clamp(30px, 30%, 150px) 1fr clamp(80px, 30%, 250px) 0;
  margin-left: clamp(2.5%, 25%, 80px);
  margin-right: clamp(2.5%, 25%, 80px);
  min-height: 100%;
  border-left: 2px solid gray;
  border-right: 2px solid gray;
  overscroll-behavior: contain;
  scroll-behavior: smooth;
  align-items: flex-start;

  > .left-pane {
    position: sticky;
    display: flex;
    top: 0;
    height: inherit;
    grid-area: left;
    overflow: auto;

    > div {
      height: 100%;
      width: 100%;

      > .logo-pane {
        display: flex;
        margin: 5px;
        padding: 10px;
        align-items: center;
        justify-content: center;
        border-radius: 5px;
        background: #d7dbdba1;
        cursor: pointer;

        > svg {
          width: 50px;
          height: 50px;
        }
      }
    }
  }

  > .center-pane {
    position: relative;
    min-height: 100%;
    border-left: 2px solid gray;
    border-right: 2px solid gray;

    > :first-child {
      position: sticky;
      top: 0;
      left: 0;
      border-bottom: 2px solid gray;
      height: calc(40px + 2px);

      > :first-child {
        position: absolute;
        display: grid;
        grid-auto-flow: row;
        align-items: center;
        justify-content: flex-start;
        padding: 5px;
        width: calc(100% - 2 * 5px);
        height: calc(100% - 2 * 5px);
        z-index: 5;
      }

      > :last-child {
        position: absolute;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: #ffffffb0;
        backdrop-filter: blur(2px);
      }
    }

    > :last-child {
      margin: 0;
    }
  }

  > .right-pane {
    position: sticky;
    display: flex;
    top: 0;
    height: inherit;
    grid-area: right;
    overflow: auto;

    > div {
      height: 100%;
      width: 100%;
    }
  }
}

.nav-btn {
  display: flex;
  width: calc(100% - 2 * 2.5px - 2 * 5px);
  margin: 2.5px;
  padding: 0 5px;
  align-items: center;
  justify-content: left;
  background: transparent;
  border: 1px solid transparent;
  text-decoration: none;
  cursor: pointer;

  > span {
    display: flex;
    width: fit-content;
    padding: 2.5px 5px;
    align-items: center;
    justify-content: center;
    color: #13bde7a1;
    fill: #13bde7a1;
    background: transparent;
    border-radius: 20px;
    border: 1px solid gray;
    text-decoration: none;
    cursor: pointer;

    > svg {
      width: 30px;
      height: 30px;
    }
  }

  &.selected {
    > span {
      background: #3fe0a2;
      color: white;
      fill: white;
    }
  }

  &:hover {
    > span {
      background: lighten($color: #13bde7a1, $amount: 30);
    }
  }
}

.cta-sect {
  display: flex;
  padding: 10px;
  justify-content: center;
  align-items: center;

  > button {
    display: flex;
    margin: 5px;
    padding: 10px 25px;
    align-items: center;
    justify-content: center;
    background: #13bde7a1;
    border-radius: 20px;
    border: none;
    box-shadow: 0 0 1.5px 1px gray;
    font-size: 1.1em;
    cursor: pointer;
    outline: none;
    filter: brightness(1.2);

    > svg {
      display: none;
    }
  }

  > button:hover {
    filter: brightness(0.98);
  }

  > button:active {
    transform: scaleX(0.95) scaleY(0.95);
  }
}

.header-pane {
  > div {
    display: grid;
    column-gap: 10px;
    grid-template-columns: auto 1fr;

    > :first-child {
      > button {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2.5px;
        border-radius: 50%;
        border: 1px solid gray;
        cursor: pointer;

        &:hover {
          background: #d6d6d6c5;
        }
      }
    }

    > :last-child {
      display: flex;
      flex-flow: column;
      align-items: flex-start;
      justify-content: flex-start;

      > h2 {
        margin: 0;
        font-size: 1.2em;
        cursor: context-menu;
      }

      > h3 {
        margin: 0;
        font-size: 1.2em;
        cursor: context-menu;
      }

      > h5 {
        margin: 0;
        font-size: 0.8em;
        font-weight: normal;
        cursor: context-menu;
      }
    }
  }
}

.poem-post-dialog {
  position: fixed;
  display: flex;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: center;
  background: #b7cec5bb;
  z-index: 50;
  overflow: auto;
  overscroll-behavior: none;
  scroll-behavior: smooth;

  > div {
    padding: 10px;
    border-radius: 15px;
    min-height: 150px;
    background: #fff;
  }
}

@media (max-width: 750px) {
  .main-layout {
    grid-template-areas: "left center";
    grid-template-columns: clamp(30px, 30%, 150px) 1fr 0;

    > .center-pane {
      border-right: none;
    }

    > .right-pane {
      display: none;
    }
  }
}

@media (max-width: 600px) {
  .main-layout {
    grid-template-areas: "left center";
    grid-template-columns: 50px 1fr;

    > .left-pane {
      > div {
        > .logo-pane {
          margin: 5px;
          padding: 5px;
          border-radius: 5px;

          > svg {
            width: 30px;
            height: 30px;
          }
        }
      }
    }

    > .center-pane {
      border-right: none;
    }
  }

  .nav-btn {
    > span {
      padding: 2.5px;
      border-radius: 20px;

      > svg {
        width: 30px;
        height: 30px;
      }
      > b {
        display: none;
      }
    }
  }

  .cta-sect {
    padding: 2px;

    > button {
      padding: 8px;

      > svg {
        display: inline-block;
        width: 25px;
        height: 25px;
      }

      > b {
        display: none;
      }
    }
  }
}

</style>
