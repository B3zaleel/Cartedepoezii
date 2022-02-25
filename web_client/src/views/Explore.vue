<template>
  <MainLayout>
    <template v-slot:header>
      <div class="header-pane">
        <div class="search-pane">
          <input
            placeholder="Search Cartedepoezii"
            v-model="searchQuery"
          />
          <button class="cdp-btn icon">
            <MagnifyIcon/>
          </button>
        </div>
      </div>
    </template>

    <template v-slot:main>
      <div class="app-explore">
        <div>
          <div>
            <!-- <Poem/> -->
          </div>
        </div>
      </div>
    </template>
  </MainLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Poem as PoemT } from '@/assets/scripts/type_defs';
import MainLayout from '@/views/layout/Main.vue';
import Poem from '@/components/Poem.vue';
import MagnifyIcon from '@/assets/icons/Magnify.vue';

@Component({
  name: 'ExploreView',
  components: {
    MainLayout,
    Poem,
    MagnifyIcon,
  },
})
export default class ExploreView extends Vue {
  searchQuery = '';
}
</script>

<style lang="scss">
@use "@/assets/styles/views/search";
</style>
