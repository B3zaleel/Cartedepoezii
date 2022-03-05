<template>
  <div class="auth sign-up">
    <div>
      <div class="heading">
        <button class="cdp-btn icon" @click="closeForm">
          <CloseIcon/>
        </button>

        <div></div>
      </div>
      <h2>Create your Account</h2>

      <form @submit.prevent="signUp">
        <div class="txb-label-over">
          <input
            name="name"
            id="form-name"
            type="text"
            v-model="name"
            :maxlength="nameLimit"
            @input="updateNameCount"
            @focus="inputFocus"
            @blur="inputBlur"
          />
          <label class="label" for="form-name">
            <div>
              <span>Name</span>

              <span class="status" v-show="nameCount > 0">{{ nameCount }} / {{ nameLimit }}</span>
            </div>
          </label>
        </div>

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
          <b>Aready have an account?</b>
          <router-link
            class="auth-link"
            to="/sign-in"
          >
            Sign In
          </router-link>
        </div>

        <div class="action right">
          <button class="cdp-btn text" :disabled="isSigningUp">
            <LoadingIcon v-show="isSigningUp"/>
            <b v-show="!isSigningUp">Create Account</b>
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
  name: 'SignUp',
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
export default class SignUp extends Vue {
  email = '';

  name = '';

  password = '';

  isSigningUp = false;

  nameCount = 0;

  isTypingName = false;

  nameLimit = 60;

  authAPIReq = new AuthAPIReq(this.$store.state.API_URL);

  updateNameCount(): void {
    this.nameCount = this.name.length;
  }

  closeForm(): void {
    this.$router.push('/');
  }

  signUp(): void {
    this.isSigningUp = true;
    this.authAPIReq.signUp(this.name, this.email, this.password)
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
        this.isSigningUp = false;
      }).catch(() => {
        this.isSigningUp = false;
      });
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/views/auth";
</style>
