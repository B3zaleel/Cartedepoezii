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
@use "@/assets/styles/views/layout/main_alt";
</style>
