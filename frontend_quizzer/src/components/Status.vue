
- Reactive badges
- Responsible for displaying success, error, warning, and info messages of the application

<script setup>
  import { ref, watch } from 'vue'
  import TransitionUpFadeSlide from './TransitionUpFadeSlide.vue'
  
  const props = defineProps(['modelValue', 'shake', 'twoStatus', 'defaultStatus', 'delayTime'])

  const toggleShake = ref(false)

  watch(props.modelValue, (newModelValue) => {
    if (newModelValue.message.length > 1 && props.twoStatus) {
      animateMessage()
    } else if (props.shake) {
      animateShake()
    }
  })

  function animateMessage() {
    if (props.twoStatus) {
      setTimeout(() => props.modelValue.message = '', props.delayTime)
    }
  }

  function animateShake() {
    toggleShake.value = !toggleShake.value

    setTimeout(() => toggleShake.value = !toggleShake.value, 1000)
  }
</script>

<template>
  <TransitionUpFadeSlide mode="out-in">
    <template v-if="modelValue.message.length > 0">
      <div
        v-if="Array.isArray(modelValue.message)"
        :class="{
          'text-bg-success': modelValue.success,
          'text-bg-danger': modelValue.error,
          'text-bg-warning': modelValue.warning,
          'text-bg-info': modelValue.info,
          'shake': toggleShake
        }"
        class="badge fs-6 mb-3 text-wrap"
      >
        <div v-for="message in modelValue.message">
          {{ `${message}` }}
        </div>
      </div>

      <span 
        v-else
        :class="{
          'text-bg-success': modelValue.success,
          'text-bg-danger': modelValue.error,
          'text-bg-warning': modelValue.warning,
          'text-bg-info': modelValue.info,
          'shake': toggleShake
        }" 
        class="badge fs-6 mb-3 text-wrap"
      >
        {{ modelValue.message }}
      </span>
    </template>

    <span
      v-if="twoStatus && !modelValue.message.length > 0 && defaultStatus"
      :class="{
        'text-bg-success': defaultStatus.success,
        'text-bg-danger': defaultStatus.error,
        'text-bg-warning': defaultStatus.warning,
        'text-bg-info': defaultStatus.info
      }" 
      class="badge fs-6 mb-3 text-wrap"
    >
      {{ defaultStatus.message }}
    </span>
  </TransitionUpFadeSlide>
</template>
