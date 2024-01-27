
- For boolean inputs
- Additional note: 
* Apparently, if there are two of this component in the same webpage
* it confuses the second, third, and vice versa renders of its self as the first one
* making the other components' input the same as the first component's v-model update
* 
* So, a name prop must be passed down if TypeBoolean component is used
* twice in a page

<script setup>
  defineProps(['modelValue', 'name'])
  defineEmits(['update:modelValue'])
</script>

<template>
  <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
    <input 
      :checked="modelValue"
      @input="$emit('update:modelValue', true)" 
      :name="name ? name : 'btnradio'" 
      :id="name ? name + '-1' : 'btnradio1'"
      type="radio" 
      class="btn-check" 
      autocomplete="off" 
    />
    <label class="btn btn-outline-light" :for="name ? name + '-1' : 'btnradio1'">True</label>

    <input 
      :checked="!modelValue"
      @input="$emit('update:modelValue', false)" 
      :name="name ? name : 'btnradio'" 
      :id="name ? name + '-2' : 'btnradio2'"
      type="radio" 
      class="btn-check" 
      autocomplete="off" 
    />
    <label class="btn btn-outline-light" :for="name ? name + '-2' : 'btnradio2'">False</label>
  </div>
</template>
