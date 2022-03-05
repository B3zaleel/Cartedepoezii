<template>
  <div class="auth sign-in">
    <div>
      <div class="heading">
        <button class="close-btn" @click="closeForm">
          <CloseIcon/>
        </button>

        <div></div>
      </div>
      <h2>Change your Password</h2>

      <form @submit.prevent="resetPassword">
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
          <label class="label" for="form-word">New Password</label>
        </div>

        <div class="action">
          <button class="btn-link" v-bind:disabled="isChangingPassword">
            <LoadingIcon v-show="isChangingPassword"/>
            <b v-show="!isChangingPassword">Change Password</b>
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
  name: 'ResetPasswordView',
  data() {
    return {
      info: {
        email: '',
        password: '',
      },
      isChangingPassword: false,
    };
  },
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
export default class ResetPasswordView extends Vue {
  email!: string;

  password!: string;

  isChangingPassword = false;

  authAPIReq = new AuthAPIReq(this.$store.state.API_URL);

  closeForm(): void {
    this.$router.push('/');
  }

  resetPassword(): void {
    this.isChangingPassword = true;
    const userId = this.$route.query.id[0] || '';
    const resetToken = this.$route.query.token[0] || '';
    this.authAPIReq.resetPassword(userId, this.email, this.password, resetToken)
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
        this.isChangingPassword = false;
      }).catch(() => {
        this.isChangingPassword = false;
      });
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/views/auth";
</style>
