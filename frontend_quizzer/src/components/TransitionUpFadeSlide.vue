<template>
  <Transition mode="out-in" appear>
    <slot></slot>
  </Transition>
</template>

<style scoped>
  .v-enter-active,
  .v-leave-active {
    transition: all 0.25s ease-out;
  }

  .v-enter-from {
    transform: translateY(50px);
    opacity: 0;
  }

  .v-leave-to {
    transform: translateY(-50px);
    opacity: 0;
  }
</style>