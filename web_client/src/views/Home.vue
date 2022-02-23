<template>
  <div class="home">
    <UserHome v-show="isAuthenticated()"/>
    <GuestHome v-show="!isAuthenticated()"/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import UserHome from './UserHome.vue';
import GuestHome from './GuestHome.vue';

@Component({
  components: {
    UserHome,
    GuestHome,
  },
  methods: {
    isAuthenticated() {
      return this.$store.state.user.isAuthenticated;
    },
  },
})
export default class HomeView extends Vue {}
</script>

<style lang="scss">
.home {
  display: contents;
  min-height: 100%;
}
</style>
