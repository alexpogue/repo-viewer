<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Github Python projects</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Refresh database</button>
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
              v-for="(repository, index) in repositories"
              @click="navigateToDetails(repository)"
              :key="index"
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

export default {
  data() {
    return {
      repositories: [],
    };
  },
  methods: {
    getRepositories() {
      const path = 'http://localhost:5000/repo/';
      axios.get(path)
        .then((res) => {
          this.repositories = res.data.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    navigateToDetails(repository) {
      this.$router.push({
        name: 'RepoDetails',
        params: { id: repository.id, preloadedRepository: repository },
        // props: { repository },
      });
    },
  },
  created() {
    this.getRepositories();
  },
};
</script>
