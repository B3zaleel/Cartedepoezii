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
