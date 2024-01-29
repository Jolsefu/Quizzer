<script setup>
  import { onMounted, ref } from 'vue'
  import TransitionUpFadeSlide from '@/components/TransitionUpFadeSlide.vue';
  import { useGetUsername, useIsAuthenticated } from '@/user';

  const logoAnimation = ref(false)

  onMounted(() => setTimeout(() => logoAnimation.value = true, 2000))
</script>

<template>
  <TransitionUpFadeSlide appear>
    <div class="main-content">
      <TransitionUpFadeSlide appear>

        <template v-if="!logoAnimation">
          <div class="container-fluid text-center">
            <img src="../assets/logo.png" id="logo" />
          </div>
        </template>
          
        <template v-if="logoAnimation">
          <div>
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
        </template>

      </TransitionUpFadeSlide>
    </div>
  </TransitionUpFadeSlide>
</template>

<style scoped>
  #website-title {
    text-shadow : 1px 1px 10px #fff;
  }

  #logo {
    width: 25%;
  }

  @media only scren and (max-width: 450px) {
    #logo {
      width: 100%;
    }
  }
</style>
