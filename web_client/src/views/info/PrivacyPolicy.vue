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
              <h3>Privacy Policy</h3>
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
import MainContent from './_PrivacyPolicy.vue';

@Component({
  name: 'PrivacyPolicyView',
  components: {
    MainLayout,
    MainAltLayout,
    ArrowLeftIcon,
    MainContent,
  },
})
export default class PrivacyPolicyView extends Vue {
  isAuthenticated(): boolean {
    return this.$store.state.user.isAuthenticated;
  }

  goBack(): void {
    this.$router.go(-1);
  }
}
</script>

<style lang="scss">
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
      align-items: center;
      justify-content: center;

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
</style>
