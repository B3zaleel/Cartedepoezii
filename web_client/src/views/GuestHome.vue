<template>
  <MainAltLayout>
    <div class="guest-home">
      <div class="main">
        <div>
          <img
            class="bg"
            loading="lazy"
            src="../assets/images/home_background.jpg"
          />
          <div class="bg">
            <Logo/>
          </div>
        </div>

        <div>
          <div>
            <h1>It's poetic</h1>
            <h2>Join Cartedepoezii today.</h2>
            <router-link class="cdp-btn text" to="/sign-up">Sign up with email</router-link>
            <div>
              <h4>
                By signing up, you agree to our
                <router-link to="/terms-of-service">Terms of service</router-link>
                and <router-link to="privacy-policy">Privacy Policy</router-link>.
              </h4>
            </div>
          </div>

          <div>
            <h3>Already have an account?</h3>
            <router-link class="cdp-btn text" to="/sign-in">Sign In</router-link>
          </div>
        </div>
      </div>
    </div>
  </MainAltLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import MainAltLayout from '@/views/layout/MainAlt.vue';
import Logo from '@/assets/icons/Logo.vue';

@Component({
  name: 'GuestHomeView',
  components: {
    MainAltLayout,
    Logo,
  },
})
export default class GuestHomeView extends Vue {}
</script>

<style lang="scss">
.guest-home {
  display: grid;
  grid-template-rows: 1fr auto;
  min-height: 100%;

  .main {
    display: grid;
    grid-template-columns: 50% 50%;

    div {
      position: relative;

      img {
        width: 100%;
        object-fit: cover;
      }
      .bg{
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        left: 0;
        bottom: 0;
      }
      .bg:last-child{
        z-index: 5;
        background: #b4f0dec4;
        backdrop-filter: blur(1.5px);

        > svg {
          width: clamp(30px, 80%, 720px);
          height: clamp(30px, 80%, 720px);
        }
      }
    }

    > div:nth-child(2) {
      padding: 20px;

      > div {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
      }
    }

    h1 {
      font-size: 2.5em;
    }

    h2 {
      font-size: clamp(18px, 2.0em, 25px);
    }

    h3 {
      font-size: clamp(12px, 1.2em, 18px);
    }

    h4 {
      font-size: 0.6em;
    }
  }
}

@media (max-width: 600px) {
  .guest-home {
    .main {
      display: flex;
      flex-flow: column-reverse;
      grid-template-columns: none;
      align-items: stretch;
      justify-content: stretch;

      > div:first-child {
        min-height: 150px;
        height: 40%;
      }

      > div:last-child {
        height: inherit;
        align-items: center;
        height: 60%;
        min-height: 250px;
      }
    }
  }
}
</style>
