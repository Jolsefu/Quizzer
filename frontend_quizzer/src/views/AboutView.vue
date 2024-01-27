<script setup>
  import TransitionUpFadeSlide from '@/components/TransitionUpFadeSlide.vue';
</script>

<template>
  <div class="main-content">
    <TransitionUpFadeSlide appear>
      <div id="about-container" class="container-fluid">
        <div class="text-center">
          <h5>About</h5>

          <h1>A Brief Introduction</h1>
        </div>

        <div id="about-info">
          <p>This website was created because a student was so lazy of asking other students to question them as a means to review the upcoming quizzes, exams, etc. that he decided to create it as an application.</p>

          <div id="credit" class="position-relative">
            Written by Jules Leo Reserva
            <span class="position-absolute top-0 start-100 translate-middle badge bg-light text-dark">
              Creator
            </span>
          </div>
        </div>

        <div class="text-center">
          <button type="button" class="btn btn-light" @click="$router.push('/')">Home</button>
        </div>
      </div>
    </TransitionUpFadeSlide>
  </div>

</template>

<style scoped>
  #credit {
    background-color: black;
    width: fit-content;
    padding: 0.5rem;
  }

  #about-info {
    margin-top: 2rem;
    margin-bottom: 2rem;
    padding: 0 15rem 0 15rem;
    text-align: justify;
  }

  @media only screen and (max-width: 880px) {
    #about-info {
      padding: 0 5rem 0 5rem;
    }
  }

  @media only screen and (max-width: 550px) {
    #about-info {
      padding: 0;
    }
  }

  @media only screen and (max-width: 450px) {
    .main-content {
      padding: 7rem 1rem 1rem 1rem;
    }
  }
</style>