import Vue from 'vue';
import VueRouter, { Route, RouteConfig } from 'vue-router';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    meta: {
      title: 'Home',
      requiresAuth: false,
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
      disableOnSignedIn: true,
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
    path: '/poem/:id',
    props: { id: String },
    name: 'Poem',
    meta: {
      title: 'Poem',
      requiresAuth: true,
    },
    component: () => import('../views/Poem.vue'),
  },
  {
    path: '/comment/:id',
    props: { id: String },
    name: 'Comment',
    meta: {
      title: 'Comment',
      requiresAuth: true,
    },
    component: () => import('../views/Comment.vue'),
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
    path: '/terms-of-service',
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
  {
    path: '*',
    name: 'Error404',
    meta: {
      title: 'Error 404',
      requiresAuth: false,
    },
    component: () => import('../views/Error404.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to: Route, from: Route, next) => {
  const isAuthenticated = window.localStorage.getItem('user.isAuthenticated') === 'true';
  if (!isAuthenticated && to.meta?.requiresAuth) {
    next('/sign-in');
  } else if (isAuthenticated && to.meta?.disableOnSignedIn) {
    next('/');
  } else {
    next();
  }
});

router.afterEach((to) => {
  document.title = to.meta?.title
    ? `${to.meta.title} - Cartedepoezii`
    : 'Cartedepoezii';
});

export default router;
