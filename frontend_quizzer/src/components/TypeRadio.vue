
- For radio button inputs
- A radio button group of choices when a choice is clicked, it updates the model of the choice's value

<script setup>
  defineProps(['modelValue', 'choices', 'altChoices'])
  defineEmits(['update:modelValue'])
</script>

<template>
  <div class="btn-group-vertical d-flex" role="group" aria-label="Vertical radio toggle button group">
    <template v-for="(choice, index) in choices" :key="index">
      <input 
        :value="choice" 
        :id="`btnradio${index}`" 
        @input="$emit(`update:modelValue`, $event.target.value)" 
        type="radio" 
        class="btn-check" 
        name="btnradio" 
        autocomplete="off" 
      />
      <label class="btn btn-outline-light" :for="`btnradio${index}`"> 
        {{ altChoices && altChoices.length === choices.length? altChoices[index] : choice }}
      </label>
    </template>
  </div>
</template>

<style scoped>
  label {
    word-break: break-all;
  }

  .btn-outline-light:hover {
    color: #000;
    background-color: #f8f9fa;
    border-color: #f8f9fa;
    text-shadow: inset 0 3px 5px rgba(0, 0, 0, 0.125);
  }
</style>
