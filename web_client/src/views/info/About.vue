<template>
  <div class="content-container">
    <MainLayout v-if="isAuthenticated()">
      <template v-slot:header>
        <div class="header-pane">
          <div class="page-nav-bar">
            <div>
              <button class="cdp-btn icon" @click="goBack">
                <ArrowLeftIcon/>
              </button>
            </div>
            <div>
              <h1>About Cartedepoezii</h1>
            </div>
          </div>
        </div>
      </template>

      <template v-slot:main>
        <MainContent/>
      </template>
    </MainLayout>
    <MainAltLayout v-if="!isAuthenticated()">
      <MainContent/>
    </MainAltLayout>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import MainLayout from '@/views/layout/Main.vue';
import MainAltLayout from '@/views/layout/MainAlt.vue';
import ArrowLeftIcon from '@/assets/icons/ArrowLeft.vue';
import MainContent from './_About.vue';

@Component({
  name: 'AboutView',
  components: {
    MainLayout,
    MainAltLayout,
    ArrowLeftIcon,
    MainContent,
  },
})
export default class AboutView extends Vue {
  userId! : string

  isAuthenticated(): boolean {
    return this.$store.state.user.isAuthenticated;
  }

  goBack(): void {
    this.$router.go(-1);
  }

  created(): void {
    this.userId = this.$route.params.id;
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/views/info";
</style>
