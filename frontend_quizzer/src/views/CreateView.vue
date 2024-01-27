
- For creating or editing quiz files

<script setup>
  import { ref, reactive } from 'vue'

  import { useDownloadJSON } from '@/download'
  import { useIsAuthenticated, useGetToken } from '@/user'

  import TypeButton from '@/components/TypeButton.vue'
  import TypeBoolean from '@/components/TypeBoolean.vue'
  import TransitionUpFadeSlide from '@/components/TransitionUpFadeSlide.vue'
  import TypeFileInput from '@/components/TypeFileInput.vue'
  import FromDatabase from '@/components/FromDatabase.vue'
  import Status from '@/components/Status.vue'

  const errorPreFile = reactive({
    'error': true,
    'message': []
  })

  const preFileLoaded = ref(false)
  const editFile = ref(false)

  const downloadFileInput = ref(null)

  // For UI responsiveness
  const windowWidth = ref(window.innerWidth)
  window.onresize = () => windowWidth.value = window.innerWidth

  const types = ref({
    'single_input': 'Identification',
    'multiple_input': 'Enumeration',
    'multiple_choice': 'Multiple Choice',
    'true_or_false': 'True or False'
  })

  // Store Quiz JSON File on memory to be editable
  const preFile = reactive({
    'info': {
      name: '',
      caseSensitive: false,
      alwaysShuffle: false
    },
    'quiz': []
  })

  // The value of the input when adding a new choice
  const multipleChoiceInput = ref('')
  const chosenChoice = ref('')

  // Database file
  const databaseFileInfo = reactive({
    id: null
  })

  const fileFromDatabase = ref(false)

  function addQuizToPreFile() {
    preFile.quiz.push({
      'points': 0
    })
  }

  function removeQuizOfPreFile(index) {
    preFile.quiz.splice(index, 1)
  }

  function loadFile() {
    preFileLoaded.value = true
  }
  
  function databaseFile(id) {
    console.log('called')

    databaseFileInfo.id = id
    fileFromDatabase.value = true
  }

  function updateFile() {
    fetch('http://127.0.0.1:8000/quizzer/update_file', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${useGetToken()}`,
      },
      body: JSON.stringify(
        {
          'id': databaseFileInfo.id,
          'json': preFile
        }
      )
    })
    .then(response => response.json())
    .then(data => {

      console.log(data)

    })
    .catch(err => {
      console.log(err)
    })
  }

  function chooseType(quizDict, type) {
    quizDict.type = type

    quizDict.question ? quizDict.question = quizDict.question : quizDict.question = ''

    if (type === 'single_input') {
      quizDict.answer = ''
    } else if (type === 'multiple_input') {
      quizDict.answer = []
      quizDict.ordered = false
    } else if (type === 'multiple_choice') {
      quizDict.answer = null
      quizDict.choices = []
    } else if (type === 'true_or_false') {
      quizDict.answer = false
    }
  }

  function removeChoice(quizDict) {
    const index = quizDict.choices.indexOf(chosenChoice.value)

    if (quizDict.answer === chosenChoice.value) {
      quizDict.answer = null
    }

    if (index !== -1) {
      quizDict.choices.splice(index, 1)
    }

    chosenChoice.value = ''
  }

  function markChoiceAsAnswer(quizDict) {
    quizDict.answer = chosenChoice.value
  }

  function addInputToChoices(quizDict) {
    if (multipleChoiceInput.value.length > 0) {
      quizDict.choices.push(multipleChoiceInput.value)
    }
  }

  function downloadFile() {
    if (validateInput()) {
      useDownloadJSON(preFile)
    }
  }

  function validateInput() {
    // In case of past errors
    errorPreFile.message.splice(0)

    // Validates info of preFile
    if (preFile.info.name.length < 1) {
      errorPreFile.message.push('Must provide a name for the quiz.')
    }

    // Validates quiz array of preFile
    let isQuestionInvalid = false
    let isAnswerInvalid = false

    const quizChecker = () => preFile.quiz.forEach(quizEntry => {
      if (!quizEntry.question || quizEntry.question.length < 1) {
        isQuestionInvalid = true
      }

      if (!quizEntry.answer || quizEntry.answer.length < 1) {
        isAnswerInvalid = true
      }

      if (isQuestionInvalid || isAnswerInvalid) {
        return false
      }
    })

    if (!quizChecker()) {
      if (isQuestionInvalid) {
        errorPreFile.message.push('Must provide a question for each quiz entry.')
      }

      if (isAnswerInvalid) {
        errorPreFile.message.push('Must provide an answer for each quiz entry.')
      }
    }

    if (errorPreFile.message.length > 0) {    
      return false
    } else {
      return true
    }
  }
</script>

<template>
  <div class="main-content">
    <TransitionUpFadeSlide mode="out-in" appear>

      <!-- 
        
        Asks for input either from the user's database if they are authenticated
      
        or loads the file locally

      -->

      <template v-if="!preFileLoaded">
        <div>
          <TransitionUpFadeSlide mode="out-in" appear>
            <div v-if="editFile">
              <div id="edit-file" class="container-fluid text-center">
                <TypeButton 
                  @click="() => editFile = false" 
                  button-display="Back" 
                  class="me-1 mb-2"
                />

                <TypeFileInput v-model="preFile" @file-is-loaded="loadFile" />

                <template v-if="useIsAuthenticated()">
                  <FromDatabase 
                    v-model="preFile" 
                    :get-file-info="true" 
                    @file-is-loaded="loadFile"
                    @use-file-info="databaseFile"
                  />
                </template>
              </div>
            </div>
            <div v-else>
              <div class="container-fluid text-center">
                <TypeButton 
                  @click="() => editFile = true" 
                  button-display="Edit File" 
                  class="me-1" 
                />
                <TypeButton 
                  @click="() => preFileLoaded = true" 
                  button-display="Create New File" 
                  class="ms-1" 
                />
              </div>
            </div>
          </TransitionUpFadeSlide>
        </div>
      </template>
      <template v-if="preFileLoaded">
        <div>

          <!-- General quiz info -->

          <div id="info-container" class="container-fluid mb-3 text-center">
            <Status 
              v-model="errorPreFile" 
              :two-status="false"
              :shake="true"
            />

            <div class="container-fluid input-group mb-3">
              <span class="input-group-text">Quiz Name</span>
              <input 
                v-model="preFile.info.name"
                type="text"
                class="form-control"
                id="info-name"
              >
            </div>
            <div class="mb-2">
              Case Sensitivity: 
              <TypeBoolean 
                v-model="preFile.info.caseSensitive" 
                name="case-sensitivity"
                id="info-case-sensitive"
                class="is-invalid"
              />
            </div>
            <div class="mb-2">
              Always Shuffle: 
              <TypeBoolean 
                v-model="preFile.info.alwaysShuffle"
                name="always-shuffle"
                id="info-always-shuffle" 
              />
            </div>
            <div>
              <a
                ref="downloadFileInput"
                @click="downloadFile" 
                :class="{'disabled': preFile.quiz.length < 1}"
                class="btn btn-light me-1"
              >
                Download
              </a>
              <a
                v-if="fileFromDatabase"
                ref="downloadFileInput"
                @click="updateFile" 
                class="btn btn-light"
              >
                Save Changes
              </a>
              <TypeButton 
                @click="addQuizToPreFile" 
                button-display="Add Quiz"
                class="ms-1"
              />
            </div>
          </div>

          <!-- Quiz entries, question and answers -->

          <div id="quiz" class="container-fluid">
            <TransitionGroup tag="ul" name="quiz" id="quiz-entry-container" mode="out-in">
              <div 
                v-for="(quizDict, index) in preFile.quiz" 
                :key="quizDict"
                class="quiz-entry"
              >
                <div id="quiz-group-container" class="container-fluid mb-3 text-center">
                  <div class="input-group mb-2">
                    <span class="input-group-text">Question</span>
                    <input 
                      v-model="quizDict.question"
                      type="text"
                      class="form-control" 
                    >
                  </div>

                  <Transition name="quiz" mode="out-in">
                    <template v-if="quizDict.type === 'single_input'">
                      <div class="input-group my-2">
                        <span class="input-group-text">Answer</span>
                        <input 
                          v-model="quizDict.answer"
                          type="text"
                          class="form-control disabled" 
                        >
                      </div>
                    </template>

                    <template v-else-if="quizDict.type === 'multiple_input'">
                      <div>
                        <TransitionGroup 
                          tag="ul" 
                          name="quiz" 
                        >
                          <div 
                            v-for="(currentAnswer, index) in quizDict.answer" 
                            :key="index"
                          >
                            <div class="input-group my-2">
                              <span class="input-group-text">
                                Answer
                              </span>
                              <input 
                                v-model="quizDict.answer[index]"
                                type="text"
                                class="form-control"
                              >
                              <button
                                @click="quizDict.answer.splice(index, 1)" 
                                class="btn btn-outline-secondary" 
                                type="button" 
                              >
                                Remove
                              </button>
                            </div>
                          </div>
                        </TransitionGroup>

                        <div class="my-2">
                          <div>
                            <TypeButton 
                              @click="() => quizDict.answer.push('')" 
                              button-display="Add Answer" 
                            />
                          </div>
                          <div class="mt-2">
                            Ordered: 
                            <TypeBoolean 
                              v-model="quizDict.ordered" 
                              :name="`${index}-ordered-bool`" 
                            />
                          </div>
                        </div>
                      </div>
                    </template>

                    <template v-else-if="quizDict.type === 'true_or_false'">
                      <div class="my-2">
                        Answer: 
                        <TypeBoolean 
                          v-model="quizDict.answer" 
                          :name="`${index}-quiz`" 
                        />
                      </div>
                    </template>

                    <template v-else-if="quizDict.type === 'multiple_choice'">
                      <div class="my-2 mb-3">
                        <div 
                          :class="{
                            'btn-group': windowWidth > 655,
                            'btn-group-vertical': windowWidth <= 655
                          }"
                          class="my-2"
                        >
                          <button 
                            @click="markChoiceAsAnswer(quizDict)" 
                            :class="{'disabled': !chosenChoice}"
                            class="btn btn-success"
                          >
                            Mark As Answer
                          </button>
                          <button
                            @click="removeChoice(quizDict)"
                            :class="{'disabled': !chosenChoice}"
                            class="btn btn-danger"
                          >
                            Remove
                          </button>
                          <button 
                            :class="{
                              'disabled': quizDict.choices.length < 1,
                              'btn-success': quizDict.answer === chosenChoice,
                              'btn-light': quizDict.answer !== chosenChoice
                            }"
                            type="button" 
                            class="btn dropdown-toggle" 
                            data-bs-toggle="dropdown" 
                            aria-expanded="false"
                          >
                            {{ chosenChoice ? chosenChoice : 'Choose Choice' }}
                          </button>
                          <ul class="dropdown-menu">
                            <template v-for="(choice, index) in quizDict.choices">
                              <li>
                                <a 
                                  @click.prevent="() => chosenChoice = choice"
                                  :class="{'text-success': quizDict.answer === choice}"
                                  class="dropdown-item" 
                                  href="#"
                                >
                                  {{ choice }}
                                </a>
                              </li>
                            </template>
                          </ul>
                        </div>

                        <div class="input-group mt-2">
                          <button 
                            @click="addInputToChoices(quizDict)"
                            class="btn btn-outline-secondary" 
                            type="button" 
                          >
                            Add Choice
                          </button>
                          <input 
                            v-model="multipleChoiceInput"
                            type="text" 
                            class="form-control" 
                          >
                        </div>
                      </div>
                    </template>

                    <template v-else>
                      <div class="my-2">
                        Choose an answer type first to provide an answer.
                      </div>
                    </template>

                  </Transition>

                  <Transition name="quiz" mode="out-in">
                    <template v-if="quizDict.type">
                      <div id="points" class="input-group mb-3">
                        <span class="input-group-text">
                          Points
                        </span>
                        <button 
                          class="btn btn-outline-success" 
                          type="button"
                          @click="quizDict.points++"
                        >
                          +
                        </button>
                        <input
                          v-model="quizDict.points"
                          type="number" 
                          class="form-control"
                        >
                        <button
                          class="btn btn-outline-danger"
                          type="button" 
                          id="button-addon2"
                          @click="quizDict.points <= 0 ? null : quizDict.points--"
                        >
                          -
                        </button>
                      </div>
                    </template>
                  </Transition>

                  <div
                    :class="{
                      'btn-group': windowWidth > 655,
                      'btn-group-vertical': windowWidth <= 655
                    }"
                    id="quiz-buttons"
                    role="group"
                  >
                    <TypeButton 
                      v-if="index + 1 === preFile.quiz.length"
                      @click="addQuizToPreFile" 
                      button-display="Add Another" 
                    />
                    <TypeButton 
                      @click="removeQuizOfPreFile(index)" 
                      button-display="Remove"
                    />
                    <div class="btn-group" role="group">
                      <button 
                        type="button" 
                        class="btn btn-light dropdown-toggle" 
                        data-bs-toggle="dropdown" 
                        aria-expanded="false"
                      >
                        {{ quizDict.type ? types[quizDict.type] : 'Choose Type' }}
                      </button>
                      <ul class="dropdown-menu">
                        <template v-for="[type, typeDisplay] in Object.entries(types)">
                          <li>
                            <a 
                              @click.prevent="chooseType(quizDict, type)"
                              class="dropdown-item" 
                              href="#"
                            >
                              {{ typeDisplay }}
                            </a>
                          </li>
                        </template>
                      </ul>
                    </div>
                  </div>
                </div>

              </div>
            </TransitionGroup>
          </div>
        </div>
      </template>
    </TransitionUpFadeSlide>
  </div>
</template>

<style scoped>
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  .quiz-enter-active,
  .quiz-leave-active {
    transition: all 0.3s ease-in-out;
  }

  .quiz-enter-from,
  .quiz-leave-to {
    opacity: 0;
    transform: translate(30px, 0);
  }

  .quiz-entry {
    padding: 1.5rem;
    background-color: rgb(23, 23, 23);
    border: 1px solid rgb(69, 69, 69);
    margin-bottom: 2rem;
    border-radius: .5rem;
  }

  ul {
    padding: 0;
  }

  #points {
    width: 30%;
  }

  #error-prefile {
    width: fit-content;
    font-size: 13px;
    padding: .5rem;
    border-radius: .3rem;
  }

  #quiz-question-answer {
    width: 50%;
  }

  #quiz {
    width: 50%;
    padding: 3rem 0 0 0;
  }

  #info-container {
    width: 30%;
    padding: 0 2rem 1rem 2rem;
  }

  #edit-file {
    width: 50%;
  }

  @media only screen and (max-width: 1250px) {
    #points {
      width: 45%;
    }

    #info-container {
      width: 50%;
    }
  }

  @media only screen and (max-width: 970px) {
    #quiz {
      width: 70%;
    }

    #info-container {
      width: 70%;
    }
  }

  @media only screen and (max-width: 760px) {
    #points {
      width: 60%;
    }
  }

  @media only screen and (max-width: 655px) {
    .btn-group {
      position: relative;
      flex: 1 1 auto;
    }
  }

  @media only screen and (max-width: 630px) {
    #points {
      width: 70%;
    }
  }
 
  @media only screen and (max-width: 550px) {
    #info-container {
      width: 95%;
      padding: 0;
    }

    .main-content {
      padding: 10rem 1rem 1rem 1rem;
    }

    #quiz {
      width: 95%;
    }

    #edit-file {
      width: 95%;
    }
  }

  @media only screen and (max-width: 400px) {
    #points {
      width: 70%;
    }
  }

  @media only screen and (max-width: 370px) {
    #points {
      width: 90%;
    }
  }
</style>
