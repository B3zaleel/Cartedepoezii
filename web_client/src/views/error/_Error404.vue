<template>
  <div class="error-pane">
    <h1>Oh No!</h1>
    <p>
      We searched far and wide into the mist,<br/>
      But nothing came from within.<br/>
      We waited until the clear skies turned grey.<br/>
      After so long, back <router-link class="cdp-btn text" to="/">home</router-link> we went.
    </p>
  </div>
</template>

<script lang='ts'>
import { Component, Vue } from 'vue-property-decorator';

@Component({
  name: 'Error404Content',
})
export default class Error404Content extends Vue {}
</script>

<style lang="scss">
@use "@/assets/styles/globals";

.error-pane {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 10px;

  h1 {
    color: globals.$primary-color-lighter;
    font-size: 25px;
  }

  a {
    display: inline-flex;
  }
}
</style>
