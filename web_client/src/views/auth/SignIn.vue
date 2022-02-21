<template>
  <div class="auth sign-in">
    <div>
      <div class="heading">
        <button class="close-btn" @click="closeForm">
          <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="mdi-close" width="24" height="24" viewBox="0 0 24 24"><path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" /></svg>
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

        <div class="action">
          <button class="btn-link" v-bind:disabled="isSigningIn">
            Sign In
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

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
  },
})
export default class SignInView extends Vue {
  email!: string

  password!: string;

  isSigningIn = false;

  validForm(): boolean {
    // TODO: Validate form
    let isValid = true;

    if (this.password.length === 0) {
      isValid = false;
    }
    return isValid;
  }

  closeForm(): void {
    this.$router.push('/');
  }

  signIn(): void {
    if (this.validForm()) {
      const BASE_URL = this.$store.state.API_URL;
      const signInData = {
        email: this.email,
        password: this.password,
      };

      this.isSigningIn = true;
      fetch(`${BASE_URL}/sign-up`, {
        method: 'POST',
        mode: 'no-cors',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(signInData),
      })
        .then((response) => response.json())
        .then((res) => {
          if (res.code === 200) {
            this.$store.commit('signIn', {
              token: res.data.authToken,
            });
            this.$router.push('/');
          } else {
            // show error info
            console.log(res.message);
          }
          this.isSigningIn = false;
        }).catch((err) => {
          this.isSigningIn = false;
        });
    }
  }
}
</script>

<style lang="scss">
@use "../../assets/styles/auth.scss";
</style>
