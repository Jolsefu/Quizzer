
- Makes quizzes as flashcards

<script setup>
  import { ref, onMounted } from 'vue';
  import TypeButton from './TypeButton.vue';

  const windowWidth = ref(window.innerWidth)
  window.onresize = () => windowWidth.value = window.innerWidth

  defineProps(['currNum'])

  defineEmits(['previousCard', 'nextCard'])

  onMounted(setSize)

  const front = ref(null)
  const back = ref(null)

  const inner = ref(null)
  const flipped = ref(false)

  const toggleAnimation = ref(true)

  // This function is necessary to set both sides of the card's size as one
  function setSize() {
    const pixels = front.value.clientHeight > back.value.clientHeight ? front.value.clientHeight : back.value.clientHeight

    back.value.style.height = `${pixels}px`
    front.value.style.height = `${pixels}px`
  }

  function flipCard() {  
    if (!flipped.value) {
      inner.value.style.transform = 'rotateY(180deg)'

      flipped.value = true
    } else if (flipped.value) {
      inner.value.style.removeProperty('transform')

      flipped.value = false
    }
  }

  function animateCard() {
    toggleAnimation.value = !toggleAnimation.value

    setTimeout(() => toggleAnimation.value = !toggleAnimation.value, 300)
  }
</script>

<template>
  <Transition @enter="setSize" mode="out-in">
    <div v-if="toggleAnimation" class="card">
      <div ref="inner" class="card-inner" @click="flipCard">
        <div ref="front" class="card-front">
          <div>
            <slot name="front">

            <!-- Front content -->

            </slot>
          </div>
          <div 
            :class="{
              'btn-group': windowWidth > 455,
              'btn-group-vertical': windowWidth < 455
            }"
          >
            <TypeButton
              :class="{'disabled': currNum <= 0}"
              @click.stop="() => {(animateCard(), $emit('previousCard'))}"
              button-display="Previous Card"
            />
            <TypeButton
              @click.stop="() => {(animateCard(), $emit('nextCard'))}" 
              button-display="Next Card"
            />
          </div>
        </div>
        <div ref="back" class="card-back">
          <div>
            <slot name="back">

            <!-- Back content -->

            </slot>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
  .v-enter-active,
  .v-leave-active {
    transition: all 0.3s ease-out;
  }

  .v-enter-from {
    transform: translateX(-50px);
    opacity: 0;
  }

  .v-leave-to {
    transform: translateX(50px);
    opacity: 0;
  }

  .card {
    background-color: transparent;
    border: 0;
    width: 300px;
    height: 200px;
  }

  .card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.8s;
    transform-style: preserve-3d;
    animation: fade-in 2s;
  }

  .card-front, .card-back {
    position: absolute;
    width: 100%;
    height: fit-content;
    padding: 1.5rem;
    background-color: rgb(40, 40, 40);
    border: 1px solid #fff;
    border-radius: 1rem;
    word-break: break-all;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
  }

  .card-back {
    transform: rotateY(180deg);
  }
</style>