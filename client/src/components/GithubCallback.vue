<template>
  <div class="container">
    <router-link to="/">Go back</router-link>
    <p>Getting Github access token... Will start repo refresh when complete</p>
    <p>{{ loggedInUserToken }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';

export default {
  computed: mapState(['loggedInUserToken']),
  methods: {
    getLoggedInUserToken() {
      const { code } = this.$route.query;
      const path = `/api/user/token?code=${code}`;
      axios.get(path)
        .then((res) => {
          // for some reason, this commit doesn't seem to work
          this.$store.commit('setLoggedInUserToken', res.data.data);
          this.$router.push({ name: 'Repos', params: { loggedInUserToken: res.data.data } });
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    if (this.loggedInUserToken == null) {
      this.getLoggedInUserToken();
    } else {
      this.isLoading = false;
    }
  },
};
</script>
