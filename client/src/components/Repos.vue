<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Github Python projects</h1>
        <hr><br><br>
        <div v-if="loggedInUserToken">
          <div>Token found: {{ loggedInUserToken }}</div>
          <button
            type="button"
            class="btn btn-success btn-sm"
            @click="refreshDatabase()"
          >
            Refresh database
          </button>
        </div>
        <div v-else>
          <a
            :href="'https://github.com/login/oauth/authorize?client_id=' + githubClientId"
            class="btn btn-success btn-sm"
          >
            Authenticate to Github to refresh the list
          </a>
        </div>
        <div v-if="refreshStatusMessage">Refresh status: {{ refreshStatusMessage }}</div>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Stars</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(repository, id) in repositories"
              @click="navigateToDetails(repository)"
              :key="id"
            >
              <td>{{ repository.name }}</td>
              <td>{{ repository.num_stars }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';

export default {
  props: ['loggedInUserToken'],
  data() {
    return {
      refreshStatusMessage: '',
      githubClientId: '',
    };
  },
  computed: mapState(['repositories']),
  methods: {
    getRepositories() {
      const path = '/api/repo/';
      axios.get(path)
        .then((res) => {
          this.$store.commit('setRepositories', res.data.data);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    refreshDatabase() {
      const pathRoot = '/api/admin/refresh_repo_db';
      const tokenQuery = (this.loggedInUserToken) ? `?token=${this.loggedInUserToken}` : '';
      const path = `${pathRoot}${tokenQuery}`;

      this.refreshStatusMessage = 'Working...';
      axios.post(path, {})
        .then((res) => {
          this.refreshStatusMessage = res.data.data;
          this.getRepositories();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getGithubClientId() {
      const path = '/api/admin/github_client_id';
      axios.get(path)
        .then((res) => {
          this.githubClientId = res.data.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    navigateToDetails(repository) {
      this.$router.push({
        name: 'RepoDetails',
        params: { id: repository.id },
      });
    },
  },
  created() {
    if (!this.repositories || Object.keys(this.repositories).length < 30) {
      this.getRepositories();
    }
    this.getGithubClientId();
  },

};
</script>
