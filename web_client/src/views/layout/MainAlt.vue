<template>
  <div class="main-alt-layout">
    <div class="header-pane">
      <router-link to="/" class="app-home-link">
        <Logo/>
      </router-link>
    </div>

    <div class="main-pane">
      <slot></slot>
    </div>

    <footer>
      <div class="legal">
        <router-link to="/terms-of-service">Terms of Service</router-link>
        <router-link to="/privacy-policy">Privacy Policy</router-link>
        <router-link to="/about">About</router-link>
      </div>
      <div>
        &copy; {{ new Date().getFullYear() }} Cartedepoezii
      </div>
    </footer>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Logo from '@/assets/icons/Logo.vue';

@Component({
  name: 'MainAltLayout',
  components: {
    Logo,
  },
})
export default class MainAltLayout extends Vue {}
</script>

<style lang="scss">
.main-alt-layout {
  position: relative;
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100%;

  > .header-pane {
    display: flex;
    position: sticky;
    top: 0;
    padding: clamp(5px, 5%, 10px) clamp(10px, 10%, 30px);
    border-bottom: 1px solid gray;
    background: white;
    box-shadow: 0 0 2px 2px rgba(192, 192, 192, 0.747);
    z-index: 50;

    > .app-home-link {
      padding: 5px;
      border-radius: 5px;
      background: rgb(207, 207, 207);
      text-decoration: none;
    }
  }

  > .main-pane {
    min-height: 100%;
    display: contents;

    article {
      margin: 0px clamp(20px, 10%, 200px);
    }
  }

  > footer {
    padding: 10px;

    .legal {
      a {
        text-decoration: none;
        padding: 0 5px;
      }

      a:hover {
        text-decoration: 1px solid underline;
      }

      a:not(:last-child) {
        border-right: 2px solid grey;
      }
    }

    div {
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
}
</style>
