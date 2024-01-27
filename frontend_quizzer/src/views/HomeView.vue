<script setup>
  import TransitionUpFadeSlide from '@/components/TransitionUpFadeSlide.vue';
  import { useGetUsername, useIsAuthenticated } from '@/user';
</script>

<template>
  <TransitionUpFadeSlide appear>
    <div class="main-content">
      <div class="text-center">
        <h4 v-if="useIsAuthenticated()">Hello, {{ useGetUsername() }}</h4>
        <h4 v-else>Hello, Stranger</h4>

        <h1>Welcome to <span id="website-title">Quizzer!</span></h1>
      </div>

      <br>

      <div class="container-fluid d-flex flex-wrap justify-content-center text-center row-gap-2 column-gap-2">
        <button type="button" class="btn btn-light" @click="$router.push('quiz')">Start Reviewing</button>
        <button type="button" class="btn btn-light" @click="$router.push('create')">Create A Review</button>
      </div>
    </div>
  </TransitionUpFadeSlide>
</template>

<style scoped>
  #website-title {
    text-shadow : 1px 1px 10px #fff;
  }
</style>
