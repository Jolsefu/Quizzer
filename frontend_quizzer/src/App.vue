<script setup>
  import { RouterLink, RouterView, useRouter } from 'vue-router'
  import { useIsAuthenticated, useGetToken } from './user';
  import Navbar from './components/Navbar.vue'

  const defaultClass = 'nav-link mx-3'

  const router = useRouter()

  function logOut() {
    fetch('http://127.0.0.1:8000/auth/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${useGetToken()}`
      }
    })
    .then(() => router.go(0))
  }
</script>

<template>
  <Navbar>
    <RouterLink :class="defaultClass" :to="{ name: 'home' }">Home</RouterLink>
    <RouterLink :class="defaultClass" :to="{ name: 'about' }">About</RouterLink>
    <RouterLink :class="defaultClass" :to="{ name: 'quiz' }">Quiz</RouterLink>
    <RouterLink :class="defaultClass" :to="{ name: 'create' }">Create</RouterLink>

    <RouterLink v-if="useIsAuthenticated()" :class="defaultClass" :to="{ name: 'saved' }">
      Saved Files
    </RouterLink>
    <a v-if="useIsAuthenticated()" @click.prevent="logOut" :class="defaultClass" href="#">Log Out</a>
    <RouterLink v-if="!useIsAuthenticated()" :class="defaultClass" :to="{ name: 'login' }">Login</RouterLink>
    <RouterLink v-if="!useIsAuthenticated()" :class="defaultClass" :to="{ name: 'signup' }">Sign Up</RouterLink>
  </Navbar>

  <RouterView />
</template>

<style>
  .shake {
    animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
    transform: translate3d(0, 0, 0);
  }

  @keyframes shake {
    10%,
    90% {
      transform: translate3d(-1px, 0, 0);
    }

    20%,
    80% {
      transform: translate3d(2px, 0, 0);
    }

    30%,
    50%,
    70% {
      transform: translate3d(-4px, 0, 0);
    }

    40%,
    60% {
      transform: translate3d(4px, 0, 0);
    }
  }

  body {
    background-color: #18191c !important;
  }

  input.light-border:focus {
    border-color: #c3c3c3 !important;
    box-shadow: 0px 0px 6px #c3c3c3 !important;
  }

  .main-content {
    padding: 10rem 3rem 3rem 3rem;    
  }
</style>

<style scoped>

</style>
