import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    API_URL: 'http://localhost:5000/api/v1',
    user: {
      isAuthenticated: window.localStorage.getItem('user.isAuthenticated') === 'true',
      authToken: window.localStorage.getItem('user.authToken') || '',
      id: window.localStorage.getItem('user.id') || '',
    },
  },
  mutations: {
    signIn(state, info) {
      state.user.authToken = info.token;
      state.user.id = info.id;
      state.user.isAuthenticated = true;
      window.localStorage.setItem('user.authToken', info.token);
      window.localStorage.setItem('user.id', info.id);
      window.localStorage.setItem('user.isAuthenticated', 'true');
    },
    signOut(state) {
      state.user.authToken = '';
      state.user.id = '';
      state.user.isAuthenticated = false;
      window.localStorage.setItem('user.authToken', '');
      window.localStorage.setItem('user.id', '');
      window.localStorage.setItem('user.isAuthenticated', 'false');
    },
  },
  actions: {
  },
  modules: {
  },
});
