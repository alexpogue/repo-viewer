<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Github Python projects</h1>
        <hr><br><br>
        <button
          type="button"
          class="btn btn-success btn-sm"
          @click="refreshDatabase()"
        >
          Refresh database
        </button>
        <span>{{ refreshStatusMessage }}</span>
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
  data() {
    return {
      refreshStatusMessage: '',
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
      const path = '/api/admin/refresh_repo_db';
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
  },
};
</script>
