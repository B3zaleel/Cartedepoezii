<template>
  <div class="content-container">
    <MainLayout v-if="isAuthenticated()">
      <template v-slot:header>
        <div class="header-pane">
          <div>
            <div>
              <button class="cdp-btn icon" @click="goBack">
                <ArrowLeftIcon/>
              </button>
            </div>
            <div>
              <h1>Error 404</h1>
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
import MainContent from './_Error404.vue';

@Component({
  name: 'Error404View',
  components: {
    MainLayout,
    MainAltLayout,
    MainContent,
    ArrowLeftIcon,
  },
})
export default class Error404View extends Vue {
  isAuthenticated(): boolean {
    return this.$store.state.user.isAuthenticated;
  }

  goBack(): void {
    this.$router.go(-1);
  }
}
</script>
