
- Displays the list of files of the current user logged in
- Provides the button to load it in via Create or Quiz

<script setup>
  import { ref, onMounted } from 'vue'

  import { useDateParser } from '@/dateParser'
  import { useGetToken } from '@/user'

  import TypeButton from './TypeButton.vue'
  
  const props = defineProps(['modelValue', 'getFileInfo', 'small'])
  const emit = defineEmits(['fileIsLoaded', 'useFileInfo'])

  onMounted(setSavedFiles)

  const files = ref([])

  function setSavedFiles() {
    fetch('http://127.0.0.1:8000/quizzer/view_files', {
      method: 'GET',
      headers: {
        'Authorization': `Token ${useGetToken()}`
      }
    })
    .then(response => response.json())
    .then(data => {
      files.value = data.files
    })
  }

  function loadFile(id) {
    fetch(`http://127.0.0.1:8000/quizzer/view_file/${id}`, {
      method: 'GET',
      headers: {
        'Authorization': `Token ${useGetToken()}`
      }
    })
    .then(response => response.json())
    .then(data => {
      Object.assign(props.modelValue, data)

      emit('fileIsLoaded')

      if (props.getFileInfo) {
        emit('useFileInfo', id)
      }

    })
  }
</script>

<template>
  <div v-if="files.length > 0" id="files" class="container-fluid text-center" :class="{'mt-5': !small}">
    <div class="fs-5">
      From Your Database
    </div>
    <div v-for="file in files" class="my-2">
      <TypeButton @click="loadFile(file.id)" :button-display="`Load ${file.name}`" />
    </div>
  </div>
</template>

<style scoped>
  #files {
    width: 80%;
  }

  @media only screen and (max-width: 450px) {
    #files {
      width: 90%;
    }
  }
</style>
