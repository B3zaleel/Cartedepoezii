<template>
  <MainLayout>
    <template v-slot:header>
      <div class="header-pane">
        <h2>Home</h2>
      </div>
    </template>

    <template v-slot:main>
      <div class="user-home">
        <div>
          <div>
            <Poem/>
          </div>
        </div>
      </div>
    </template>
  </MainLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import MainLayout from '@/views/layout/Main.vue';
import Poem from '@/components/Poem.vue';

@Component({
  name: 'UserHomeView',
  components: {
    MainLayout,
    Poem,
  },
})
export default class UserHomeView extends Vue {}
</script>

<style lang="scss">
.header-pane {
  > h2 {
    margin: 0;
    font-size: 1.2em;
    cursor: context-menu;
  }
}
</style>
