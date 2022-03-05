<template>
  <div class="auth sign-in">
    <div>
      <div class="heading">
        <button class="cdp-btn icon" @click="closeForm">
          <CloseIcon/>
        </button>

        <div></div>
      </div>
      <h2>Access your Account</h2>

      <form @submit.prevent="signIn">
        <div class="txb-label-over">
          <input
            name="email"
            id="form-email"
            type="email"
            v-model="email"
            @focus="inputFocus"
            @blur="inputBlur"
          />
          <label class="label" for="form-email">Email</label>
        </div>

        <div class="txb-label-over">
          <input
            name="password"
            id="form-word"
            type="password"
            v-model="password"
            @focus="inputFocus"
            @blur="inputBlur"
          />
          <label class="label" for="form-word">Password</label>
        </div>

        <div>
          <b>Don't have an account?</b>
          <router-link
            class="auth-link"
            to="/sign-up"
          >
            Sign Up
          </router-link>
        </div>

        <div>
          <b>Forgot password?</b>
          <router-link
            class="auth-link"
            to="#reset"
            @click.prevent="forgotPassword"
            >
            Reset It
          </router-link>
        </div>

        <div class="action">
          <button class="cdp-btn text" :disabled="isSigningIn">
            <LoadingIcon v-show="isSigningIn"/>
            <b v-show="!isSigningIn">Sign In</b>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import AuthAPIReq from '@/assets/scripts/api_requests/authentication';
import CloseIcon from '@/assets/icons/Close.vue';
import LoadingIcon from '@/assets/icons/Loading.vue';

@Component({
  name: 'SignInView',
  methods: {
    inputFocus(ev) {
      const labels = ev.target.parentElement.getElementsByClassName('label');
      if (labels[0]) {
        if (!labels[0].classList.contains('roll-up')) {
          labels[0].classList.add('roll-up');
        }
      }
    },
    inputBlur(ev) {
      const labels = ev.target.parentElement.getElementsByClassName('label');
      if (ev.target.value.length > 0) {
        return;
      }
      if (labels[0]) {
        if (labels[0].classList.contains('roll-up')) {
          labels[0].classList.remove('roll-up');
        }
      }
    },
  },
  components: {
    CloseIcon,
    LoadingIcon,
  },
})
export default class SignInView extends Vue {
  email = '';

  password = '';

  isSigningIn = false;

  authAPIReq = new AuthAPIReq(this.$store.state.API_URL);

  closeForm(): void {
    this.$router.push('/');
  }

  forgotPassword(): void {
    this.authAPIReq.requestResetPassword(this.email)
      .then((res) => {
        if (res.success) {
          console.info('Please check your email for the next steps.');
        }
      });
  }

  signIn(): void {
    this.isSigningIn = true;
    this.authAPIReq.signIn(this.email, this.password)
      .then((res) => {
        if (res.success) {
          if (res.data) {
            this.$store.commit('signIn', {
              token: res.data.authToken,
              id: res.data.userId,
            });
            this.$router.push('/');
          }
        } else {
          console.error(res.message);
        }
        this.isSigningIn = false;
      }).catch(() => {
        this.isSigningIn = false;
      });
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/views/auth";
</style>
