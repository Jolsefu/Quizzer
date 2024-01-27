
- Handles the user's saved quiz files
- Shows a list of the user's saved quiz files
- Uploads local quiz files to the user's database

<script setup>
  import { ref, onMounted, reactive } from 'vue'
  import { useRouter } from 'vue-router'

  import { useGetToken, useIsAuthenticated } from '@/user'
  import { useDownloadJSON } from '@/download'
  import { useDateParser } from '@/dateParser'

  import TypeFileInput from '@/components/TypeFileInput.vue'
  import TypeButton from '@/components/TypeButton.vue'
  import TransitionUpFadeSlide from '@/components/TransitionUpFadeSlide.vue'
  import Status from '@/components/Status.vue'

  const router = useRouter()

  const files = ref([])

  const dataStatus = reactive({
    'message': ''
  })

  const defaultStatus = reactive({
    'warning': true,
    'message': 'Upload a file to input to save it to your database.'
  })

  onMounted(() => {
    if (useIsAuthenticated()) {
      setSavedFiles()
    } else {
      router.push({ path: '/signup' })
    }
  })

  // Responsible for letting the user view their current saved files
  function setSavedFiles() {
    fetch('http://127.0.0.1:8000/quizzer/view_files', {
      method: 'GET',
      headers: {
        'Authorization': `Token ${useGetToken()}`
      }
    })
    .then(response => response.json())
    .then(data => {
      files.value = data.files ? data.files : []
    })
  }

  function downloadFile(id) {
    fetch(`http://127.0.0.1:8000/quizzer/view_file/${id}`, {
      method: 'GET',
      headers: {
        'Authorization': `Token ${useGetToken()}`
      }
    })
    .then(response => response.json())
    .then(data => {
      const file = data

      useDownloadJSON(file)
    })
  }

  function deleteFile(id) {
    fetch(`http://127.0.0.1:8000/quizzer/delete_file/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Token ${useGetToken()}`
      }
    })
    .then(response => response.json())
    .then(data => {
      setSavedFiles()

      animateSuccess(data.success)
    })
  }

  function uploadFile() {
    const input = document.querySelector('#localFile')
    const data = new FormData()
    data.append('file', input.files[0])

    fetch('http://127.0.0.1:8000/quizzer/upload_file', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${useGetToken()}`,
      },
      body: data
    })
    .then(response => response.json())
    .then(data => {
      setSavedFiles()

      animateSuccess(data.success)

      input.value = ''
    })
    .catch(err => {
      console.log(err)
    })
  }

  function animateSuccess(message) {
    dataStatus.success = true
    dataStatus.message = message
  }
</script>

<template>
  <TransitionUpFadeSlide appear>
    <div class="main-content">
      <div id="status" class="text-center">
        <Status 
          v-model="dataStatus" 
          :two-status="true" 
          :default-status="defaultStatus" 
          :delay-time="1500"
        />
      </div>
      <div id="upload" class="container-fluid text-center">
        <TypeFileInput @file-is-loaded="uploadFile" />
      </div>
      <div v-if="files.length > 0" id="files" class="container-fluid text-center mt-5">
        <div v-for="file in files" class="my-2">
          Quiz '{{ file.name }}',
          Uploaded at {{ useDateParser(file.dt) }}
          <div class="btn-group">
            <TypeButton @click="downloadFile(file.id)" button-display="Download File" />
            <TypeButton @click="deleteFile(file.id)" button-display="Delete File" />
          </div>
        </div>
      </div>
    </div>
  </TransitionUpFadeSlide>
</template>

<style scoped>
  #upload {
    width: 50%;
  }

  #files {
    width: 80%;
  }

  @media only screen and (max-width: 800px) {
    #upload {
      width: 65%;
    }
  }

  @media only screen and (max-width: 450px) {
    .main-content {
      padding: 10rem .5rem .5rem .5rem;
    }

    #upload {
      width: 95%;
    }

    #files {
      width: 90%;
    }
  }
</style>
