<template>
  <article class="app-privacy-policy">
    <p>
      Lorem ipsum dolor sit, amet consectetur adipisicing elit.
      Optio quibusdam soluta id molestias nam ipsa ipsam assumenda
      quis voluptates totam tenetur cupiditate repellendus doloribus,
      incidunt harum cum commodi ex impedit!
    </p>
  </article>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component({
  name: 'PrivacyPolicyContent',
})
export default class PrivacyPolicyContent extends Vue {}
</script>

<style lang="scss">
p {
  padding: 10px;
}
</style>
