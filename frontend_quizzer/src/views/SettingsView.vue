<script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useGetToken, useSetLoggedOut, useIsAuthenticated } from '@/user'
  import TransitionUpFadeSlide from '@/components/TransitionUpFadeSlide.vue'

  onMounted(() => {

    if (!useIsAuthenticated()) {
      router.push('/')
    }

  })

  const router = useRouter()

  const confirmDeletion = ref(false)

  function logOut() {
    fetch('http://127.0.0.1:8000/auth/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${useGetToken()}`
      }
    })
    .then(() => {
      useSetLoggedOut()

      router.push('/')
    })
  }

  function deleteAccount() {
    fetch('http://127.0.0.1:8000/auth/delete', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${useGetToken()}`
      }
    })
    .then(() => {
      useSetLoggedOut()

      router.push('/')
    })
  }
</script>

<template>
  <TransitionUpFadeSlide appear>
    <div class="main-content">
      <div class="container-fluid text-center">
        <div class="mb-5 fs-5">
          Account Settings:
        </div>

        <TransitionUpFadeSlide>
        <template v-if="!confirmDeletion">
          <div>
            <div class="mb-3">
              <button class="btn btn-warning" @click="logOut">Log Out</button>
            </div>
            <div>
              <button class="btn btn-danger" @click="confirmDeletion = true">Delete Account</button>
            </div>
          </div>
        </template>
        <template v-if="confirmDeletion">
          <div>
            <div class="mb-3">
              This will permanently delete your quizzer user account. Are you sure you want to delete the account?
            </div>
            <div>
              <button class="btn btn-danger" @click="deleteAccount">Confirm Deletion</button>
            </div>
          </div>
        </template>
        </TransitionUpFadeSlide>
      </div>
    </div>
  </TransitionUpFadeSlide>
</template>
