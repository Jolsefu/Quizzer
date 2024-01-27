
- This component is used for user authentication
- Responsible for handling the Login and Sign Up page

<script setup>
  import { ref, reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import { useSetUser } from '@/user'
  import TransitionUpFadeSlide from './TransitionUpFadeSlide.vue'
  import Status from './Status.vue'

  const props = defineProps({
    formTitle: String,
  })

  const router = useRouter()

  const username = ref('')
  const password = ref('')
  const errors = reactive({
    'error': true,
    'message': []
  })

  function handleSubmit() {
    let method = props.formTitle === 'Login' ? 'login' : props.formTitle === 'Sign Up' ? 'signup' : ''

    fetch(`http://127.0.0.1:8000/auth/${method}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(
        {
          username: username.value,
          password: password.value
        }
      )
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        doError(data.error)
      }

      if (data.success) {
        const tokenResponse = useSetUser(data)

        if (tokenResponse.error) {
          return doError([tokenResponse.error])
        } else {
          router.push({ path: '/' })
        }
      }
    })
    .catch(error => {
      console.log(error)
    })
  }

  function doError(errorMessage) {
    errors.message = errorMessage
  }
</script>

<template>
  <div class="main-content" @keyup.enter="handleSubmit">
    <TransitionUpFadeSlide appear>
      <div id="auth-container" class="container-fluid d-flex justify-content-evenly flex-wrap">
        <div id="auth-info" class="text-center d-flex">
          <div>
            <h3 id="auth-title">{{ formTitle }}</h3>

            <br>

            <template v-if="formTitle === 'Login'">
              <h6>Don't have an account?</h6>
              <h6>Sign Up <RouterLink :to="{ name: 'signup' }">Here!</RouterLink></h6>
            </template>

            <template v-if="formTitle === 'Sign Up'">
              <h6>Already have an account?</h6>
              <h6>Log in <RouterLink :to="{ name: 'login' }">Here!</RouterLink></h6>
            </template>
          </div>
        </div>

        <div id="vertical-line" class="line">
        </div>

        <div id="horizontal-line" class="line">
        </div>

        <div id="auth-input">
          <div class="text-center">
            <Status 
              v-model="errors"
              :two-status="false"
              :shake="true"
            />
          </div>

          <form>
            <div class="input-container">
              <label class="form-label">Username</label>
              <input 
                v-model="username" 
                type="username" 
                class="form-control" 
                placeholder="thealphabetandnumbers" 
                autocomplete
              >
            </div>

            <div class="input-container">
              <label class="form-label">Password</label>
              <input 
                v-model="password" 
                type="password" 
                class="form-control" 
                placeholder="abcdefg321" 
                autocomplete
              >
            </div>

            <div class="text-center">
              <button @click="handleSubmit" type="button" class="btn btn-secondary my-3">Submit</button>
            </div>
          </form>
        </div>
      </div>
    </TransitionUpFadeSlide>
  </div>
</template>

<style scoped>
  a {
    text-decoration: none;
  }

  .input-container {
    margin-top: 1rem;
  }

  label {
    margin-left: 5px;
  }

  #auth-title {
    margin: 0.5rem 0 0.5rem 0;
  }

  #auth-container {
    width: 35%;
    background-color: #151515;
    border: 1px solid rgb(69, 69, 69);
    padding: 2rem;
    border-radius: 3px;
    gap: 3rem;
  }

  #vertical-line {
    height: 15rem;
    border-right: 2px solid rgb(173, 173, 173);
  }

  #horizontal-line {
    width: 90%;
    border-bottom: 2px solid rgb(173, 173, 173);
    margin: auto;
    display: none;
  }

  #auth-info {
    align-items: center;
  }

  #auth-input {
    width: 100%;
  }

  @media only screen and (max-width: 1650px) {
    #auth-container {
      width: 30%;
      gap: 1.5rem;
      flex-direction: column;
    }

    #horizontal-line {
      display: block;
    }

    #vertical-line {
      display: none;
    }

    #auth-info {
      flex: 1 0 100%;
      justify-content: center;
    }

    #auth-input {
      flex: 1 0 auto;
    }
  }

  @media only screen and (max-width: 1024px) {
    #auth-container {
      width: 45%;
    }
  }

  @media only screen and (max-width: 768px) {
    .input-container {
      margin-top: 0.5rem;
    }

    #auth-container {
      padding: 1.5rem;
    }
  }

  @media only screen and (max-width: 700px) {
    #auth-container {
      width: 60%;
    }
  }

  @media only screen and (max-width: 520px) {
    .main-content {
      padding: 10rem .5rem .5rem .5rem;
    }

    #auth-container {
      width: 80%;
    }
  }

  @media only screen and (max-width: 375px) {
    #auth-container {
      width: 95%;
    }

    #auth-info * {
      font-size: 15px;
    }

    #auth-input * {
      font-size: 15px;
    }
  }

  @media only screen and (max-width: 325px) {
    #auth-title {
      font-size: 25px;
    }
  }
</style>