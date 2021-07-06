import Vue from 'vue';
import VueRouter from 'vue-router';
import Ping from '../components/Ping.vue';
import Repos from '../components/Repos.vue';
import RepoDetails from '../components/RepoDetails.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/ping',
    name: 'Ping',
    component: Ping,
  },
  {
    path: '/',
    name: 'Repos',
    component: Repos,
  },
  {
    path: '/repo/:id',
    name: 'RepoDetails',
    component: RepoDetails,
    props: (route) => ({
      ...route.params,
    }),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
