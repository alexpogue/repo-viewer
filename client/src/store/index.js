import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store(
  {
    state: {
      repositories: {},
    },
    mutations: {
      setRepositories(state, newRepositories) {
        state.repositories = newRepositories;
      },
    },
  },
);