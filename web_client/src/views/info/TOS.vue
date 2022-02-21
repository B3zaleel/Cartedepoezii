<template>
  <div class="content-container">
    <MainLayout v-if="isAuthenticated()">
      <template v-slot:header>
        <div class="header-pane">
          <div>
            <div>
              <button @click="goBack">
                <ArrowLeftIcon/>
              </button>
            </div>
            <div>
              <h3>Terms of Service</h3>
            </div>
          </div>
        </div>
      </template>

      <template v-slot:main>
        <MainContent/>
      </template>
    </MainLayout>
    <MainAltLayout v-if="!isAuthenticated">
      <MainContent/>
    </MainAltLayout>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import MainLayout from '@/views/layout/Main.vue';
import GuestLayout from '@/views/layout/MainAlt.vue';
import ArrowLeftIcon from '@/assets/icons/ArrowLeft.vue';
import MainContent from './_TOS.vue';

@Component({
  name: 'TOSView',
  components: {
    MainLayout,
    GuestLayout,
    ArrowLeftIcon,
    MainContent,
  },
})
export default class TOSView extends Vue {
  isAuthenticated(): boolean {
    return this.$store.state.user.isAuthenticated;
  }

  goBack(): void {
    this.$router.go(-1);
  }
}
</script>

<style lang="scss"></style>
