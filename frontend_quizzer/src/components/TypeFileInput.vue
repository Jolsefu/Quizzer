
- For file inputs
- Responsible for loading local files, or uploading files to database

<script setup>
  import { reactive, ref } from 'vue'
  import Status from './Status.vue'

  const props = defineProps(['modelValue'])
  const emit = defineEmits(['fileIsLoaded'])

  const error = reactive({
    'error': true,
    'message': '',
  })

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
  
        error.message = 'It must be a valid JSON File'

        return localFile.value.value = ''
      }
    }

    fReader.readAsText(localJsonFile)
  }
</script>

<template>
  <div> 
    <label for="localFile" class="form-label">
      Input Quiz File
      <Status 
        v-model="error"
        :two-status="false"
        :shake="true"
      />
    </label>
    <input ref="localFile" class="form-control" type="file" id="localFile" @input="loadLocalFile">
  </div>
</template>
