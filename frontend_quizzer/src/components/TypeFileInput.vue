
- For file inputs
- Responsible for loading local files, or uploading files to database

<script setup>
  import { ref } from 'vue'

  const props = defineProps(['modelValue'])
  const emit = defineEmits(['fileIsLoaded'])

  const error = ref('')

  const localFile = ref(null)

  function loadLocalFile(event) {
    const localJsonFile =  event.target.files[0]

    const fReader = new FileReader()

    fReader.onload = (event) => {

      try {

        const finalFormatted = JSON.parse(event.target.result)

        if (props.modelValue) {
          Object.assign(props.modelValue, finalFormatted)
        }

        emit('fileIsLoaded')

      } catch(err) {

        console.log(err)
  
        error.value = 'It must be a valid JSON File'

        return localFile.value.value = ''
      }
    }

    fReader.readAsText(localJsonFile)
  }
</script>

<template>
  <div> 
    <label for="localFile" class="form-label">
      Input Quiz File <span v-if="error.length > 1" class="badge text-bg-warning">!! {{ error }} !!</span> 
    </label>
    <input ref="localFile" class="form-control" type="file" id="localFile" @input="loadLocalFile">
  </div>
</template>
