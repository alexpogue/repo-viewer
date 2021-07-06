import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store(
  {
    state: {
      repositories: null,
    },
    mutations: {
      setRepositories(state, newRepositories) {
        state.repositories = {};
        newRepositories.forEach((repo) => { state.repositories[repo.id] = repo; });
      },
      setRepository(state, repository) {
        if (state.repositories == null) {
          state.repositories = {};
        }
        state.repositories[repository.id] = repository;
      },
    },
  },
);
