
- For text input

<script setup>
  defineProps(['modelValue', 'id', 'display'])
  defineEmits(['update:modelValue'])
</script>

<template>
  <div class="form-floating mb-3">
    <input 
      :value="modelValue" 
      @input="$emit('update:modelValue', $event.target.value)" 
      type="text" class="form-control" 
      id="floatingInput"
      placeholder="Answer"
    />
    <label for="floatingInput">{{ display }}</label>
  </div>
</template>
