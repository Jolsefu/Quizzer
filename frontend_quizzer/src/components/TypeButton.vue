
- For button displays

<script setup>
  const props = defineProps(['modelValue', 'buttonValue', 'buttonDisplay'])
  defineEmits(['update:modelValue'])
</script>

<template>
  <button :value="buttonValue" @click="$emit('update:modelValue', $event.target.value)" class="btn btn-light">{{ buttonDisplay }}</button>
</template>
