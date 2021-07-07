<template>
  <div class="container">
    <router-link to="/">Go back</router-link>
    <div v-if="!isLoading">
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
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';

export default {
  props: ['id'],
  data() {
    return {
      isLoading: true,
    };
  },
  computed: mapState({
    repository(state) {
      return (state.repositories) ? state.repositories[this.id] : null;
    },
  }),
  methods: {
    getRepository() {
      const path = `/api/repo/${this.id}`;
      axios.get(path)
        .then((res) => {
          this.$store.commit('setRepository', res.data.data);
          this.isLoading = false;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    if (this.repository == null) {
      this.getRepository();
    } else {
      this.isLoading = false;
    }
  },
};
</script>
