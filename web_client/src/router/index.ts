import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    meta: {
      title: 'Home',
      requiresAuth: false,
      authLevel: 'any',
    },
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/sign-in',
    name: 'SignIn',
    meta: {
      title: 'Sign In',
      requiresAuth: false,
      disableOnSignedIn: true,
      authLevel: 'any',
    },
    component: () => import('../views/auth/SignIn.vue'),
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    meta: {
      title: 'Sign Up',
      requiresAuth: false,
      disableOnSignedIn: true,
    },
    component: () => import('../views/auth/SignUp.vue'),
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    meta: {
      title: 'Reset Password',
      requiresAuth: false,
    },
    component: () => import('../views/auth/ResetPassword.vue'),
  },
  {
    path: '/explore',
    name: 'Explore',
    meta: {
      title: 'Explore',
      requiresAuth: true,
    },
    component: () => import('../views/Explore.vue'),
  },
  {
    path: '/profile/:id',
    props: { id: String },
    name: 'Profile',
    meta: {
      title: 'Profile',
      requiresAuth: true,
    },
    component: () => import('../views/Profile.vue'),
  },
  {
    path: '/search/:q',
    props: { q: String },
    name: 'Search',
    meta: {
      title: 'Search',
      requiresAuth: true,
    },
    component: () => import('../views/Search.vue'),
  },
  {
    path: '/tos',
    name: 'TOS',
    meta: {
      title: 'Terms of Service',
      requiresAuth: false,
    },
    component: () => import('../views/info/TOS.vue'),
  },
  {
    path: '/privacy-policy',
    name: 'PrivacyPolicy',
    meta: {
      title: 'Privacy Policy',
      requiresAuth: false,
    },
    component: () => import('../views/info/PrivacyPolicy.vue'),
  },
  {
    path: '/about',
    name: 'About',
    meta: {
      title: 'About',
      requiresAuth: false,
    },
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: 'about' */ '../views/info/About.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
