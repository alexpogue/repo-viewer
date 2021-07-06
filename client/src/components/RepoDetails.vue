<template>
  <div class="container">
    <a href="#" @click="$router.go(-1)">Go back</a>
    <h1>{{ repository.name }}</h1>
    <ul>
      <li>Repository id: {{ repository.github_id }}</li>
      <li>URL: {{ repository.url }}</li>
      <li>Created date: {{ repository.created_date }}</li>
      <li>Last push date: {{ repository.last_push_date }}</li>
      <li>Description: {{ repository.description }}</li>
      <li>Number of stars: {{ repository.num_stars }}</li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['id', 'preloadedRepository'],
  data() {
    return {
      repository: {},
    };
  },
  methods: {
    getRepository() {
      const path = `http://localhost:5000/repo/${this.id}`;
      axios.get(path)
        .then((res) => {
          this.repository = res.data.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    if (!this.preloadedRepository) {
      // If user loads details page directly, we don't receive a repository
      // prop and we need to look it up the repo via AJAX
      this.getRepository();
    } else {
      // Otherwise we got repository prop from the previous page - just use that
      this.repository = this.preloadedRepository;
    }
  },
};
</script>
