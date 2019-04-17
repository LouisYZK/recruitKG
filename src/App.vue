<template>
  <div id="app">
    <v-header :user="user"></v-header>
    <h1>Graduation Prject Template!</h1>
    <div id="nav">
     <router-link :to="{ name: 'home' }">Vue</router-link> |
     <router-link :to="{ name: 'messages' }">Django Rest</router-link>
    </div>
    <router-view/>
  </div>
</template>

<script>
import header from './components/header.vue';
export default {
  data(){
    return {
      user: {}
    }
  },
  components: {
    'v-header': header
  }
}
</script>


<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
#nap {
  color: red;
  font-size: 30px;
}
</style>
