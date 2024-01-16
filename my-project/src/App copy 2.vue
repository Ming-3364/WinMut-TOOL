<template>
  <div id="app">
    <h1>File Content Viewer</h1>
    <p>{{ fileContent }}</p>
  </div>
</template>

<script>
// import axios from 'axios';
export default {
  data() {
    return {
      fileContent: ''
    };
  },
  mounted() {
    this.getFileContent();
  },
  methods: {
    async getFileContent() {
      try {
        // const response = await this.$axios.get('/api/get_file_content');
        // this.fileContent = response.data.content;
        
        await this.$axios
          .get('/api/get_file_content')
          .then(response => (this.fileContent = response.data.content))
          .catch(function (error) { // 请求失败处理
            console.log(error);
          });

      } catch (error) {
        console.error('Error fetching file content:', error);
      }
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1 {
  font-size: 2em;
  margin-bottom: 20px;
}

p {
  font-size: 1.2em;
}
</style>
