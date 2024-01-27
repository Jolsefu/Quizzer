<template>
  <nav class="navbar navbar-expand-lg fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand navbar-title">
        Quizzer
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <slot>
            <!-- Router Links -->
          </slot>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
  .navbar-title {
    font-size: 30px;
  }

  .navbar {
    background-color: black;
  }

  div .container-fluid {
    padding: 0 5rem 0 5rem
  }

  @media only screen and (max-width: 450px) {
    div .container-fluid {
      padding: 0 3rem 0 3rem;
    }
  }
</style>