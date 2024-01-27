
- For the main reviewing sessions
- Two options: either quiz or as flashcards

<script setup>
  import { ref, reactive, watch } from 'vue'
  import { useRouter } from 'vue-router'

  import { useIsAuthenticated } from '@/user'

  import TypeBoolean from '../components/TypeBoolean.vue'
  import TypeInput from '../components/TypeInput.vue'
  import TypeRadio from '../components/TypeRadio.vue'
  import TypeButton from '../components/TypeButton.vue'
  import TypeFileInput from '@/components/TypeFileInput.vue'
  import Card from '@/components/Card.vue'
  import FromDatabase from '@/components/FromDatabase.vue'
  import TransitionUpFadeSlide from '@/components/TransitionUpFadeSlide.vue'
    
  // Input selector
  const selected = ref(false)

  // Pre Quiz
  const loaded = ref(false)
  const loadType = ref('')
  const localFile = ref(null)

  const router = useRouter()

  watch(loadType, (newLoadType) => {

    if (newLoadType === 'databaseFile' && !useIsAuthenticated()) {
      router.push({ path: '/signup' })
    }

  })

  // Quiz
  const quizActivated = ref(false)
  const cardActivated = ref(false)
  const types = ref({
    'single_input': 'Identification',
    'multiple_input': 'Enumeration',
    'multiple_choice': 'Multiple Choice',
    'true_or_false': 'True or False'
  })

  // JSON file variables
  const finalFormatted = reactive({})
  const info = ref({})
  const quiz = ref({})
  const currNum = ref(0)

  // Quiz JSON info variables
  const caseSensitive = ref(false)
  const alwaysShuffle = ref(false)

  // Main quiz variables
  const question = ref('')
  const answer = ref('')
  const answerArr = ref([])
  const choices = ref([])
  const answerType = ref('')
  const results = ref(false)
  const quizIsAnimating = ref(false)

  const checkCount = ref(0)
  const wrongCount = ref(0)
  const corrections = ref([])

  /**
   * 
   * Quiz application flow chart
   * 
   * Get load type: loadFile or loadDatabaseFile
   * 
   * Either way, get and load json file from both 
   * and parse it to quizJsonParser() or cardJsonParser()
   * 
   * First Case:
   * 
   * quizJsonParser()
   * - disableQuiz(): Disables the quiz by setting quizActivated variable to false using v-if
   * - get data of current quiz number and assign it to the appropriate variables
   * - activateQuiz(): Activates the quiz by setting quizActivated variable to true using v-if
   * 
   * checker()
   * - get the answer of the user and compare it to the
   * correct answer of the current quiz and append
   * the results to the results variable
   * - checks if it is the end of the quiz, if not, then
   * it increments the count of current quiz number and calls quizJsonParser()
   * 
   * Second Case:
   * 
   * cardJsonParser()
   * - disableCard(): Disables the card by setting cardActivated variable to false using v-if
   * - get data of current number and assign it to the appropriate variables
   * - activateCard(): Activates the card by setting cardActivated variable to true using v-if
   * 
   * nextCard()
   * - Proceed to next card by checking if it is the final card
   * - If not, then increment number value using cardJsonParser()
   * - If it is, show the user a prompt to try again or get another quiz json file
   * 
   */

  function loadFile() {
    info.value = finalFormatted.info
    quiz.value = finalFormatted.quiz
    caseSensitive.value = finalFormatted.info.caseSensitive
    alwaysShuffle.value = finalFormatted.info.alwaysShuffle

    if (alwaysShuffle.value) {
      shuffleQuizOnce()
    }

    loaded.value = true
  }

  function loadDatabaseFile() {
    // TODO
  }

  function quizJsonParser() {
    disableQuiz()

    // Disable activateQuiz selector
    selected.value = false

    const currQuiz = quiz.value[currNum.value]

    // Clear the answer variable
    answer.value = null

    // Set the displayed question
    question.value = currQuiz.question

    // Set what type of display of question and answer/s the quiz will be
    answerType.value = currQuiz.type

    if (currQuiz.type === 'multiple_choice') {

      // If the answer type is multiple choices, assign choices variable with the provided choices
      choices.value = currQuiz.choices

    } else if (currQuiz.type === 'multiple_input') {

      // If the answer type has multiple inputs, fill answerArr with how many answer strings are needed
      answerArr.value = []

      currQuiz.answer.forEach(() => {
        answerArr.value.push('')
      })

    }

    toggleAnimation()
  }

  function toggleAnimation() {

    quizIsAnimating.value = true

    // The timeout is necessary to fully trigger the animation
    // Otherwise, it would change the variable so fast it's undetectable
    setTimeout(() => {

      activateQuiz()

      quizIsAnimating.value = false

    }, 300)
  }

  function activateQuiz() {
    quizActivated.value = true
  }

  function disableQuiz() {
    quizActivated.value = false
  }

  function shuffleQuizOnce() {
    quiz.value = shuffle(quiz.value)
  }

  function shuffle(array) {
    let current_index = array.length, random_index;

    while (current_index > 0) {  
      random_index = Math.floor(Math.random() * current_index);
      current_index--;
  
      [array[current_index], array[random_index]] = [array[random_index], array[current_index]];
    }

    return array;
  }

  function checker() {
    /**
     * 
     * Gets the current variable model used for the current quiz and
     * checks if it matches the answer variable of the current quiz
     * 
     */

    let correctAnswers = quiz.value[currNum.value].answer
    correctAnswers = typeof(correctAnswers) !== 'object' ? [correctAnswers] : correctAnswers
    let providedAnswer = answerType.value !== 'multiple_input' ? [answer.value] :  answerArr.value
    const isOrdered = quiz.value[currNum.value].type === 'multiple_input' ? quiz.value[currNum.value].ordered : false
    const currPoints = quiz.value[currNum.value].points

    // If the quiz has case sensitivity enabled
    if (!caseSensitive.value) {
      correctAnswers = correctAnswers.map(element => {
        return typeof(element) === 'string' ? element.toLowerCase() : element
      })

      providedAnswer = providedAnswer.map(element => {
        return typeof(element) === 'string' ? element.toLowerCase() : element
      })
    }

    let currNumNeedsCorrection = false

    providedAnswer.forEach((answer, answerIndex) => {

      const index = correctAnswers.indexOf(answer)

      if (index >= 0) {

        if (isOrdered) {

          if (index === answerIndex) {
            checkCount.value += currPoints
          } else {
            wrongCount.value += currPoints

            currNumNeedsCorrection = true
          }

        } else if (!isOrdered) {
          checkCount.value += currPoints
        }

      } else if (index === -1) {
        wrongCount.value += currPoints

        currNumNeedsCorrection = true
      }
    })

    if (currNumNeedsCorrection) {
      corrections.value.push(currNum.value)
    }

    // Identifies whether if it is the end of the quiz or not
    currNum.value + 1 >= quiz.value.length ? showResults() : (currNum.value++, quizJsonParser())
  }

  function showResults() {
    // Show results template
    results.value = true
  }

  function answerParser(type, answer) {
    /**
     * 
     * Takes the type of the current quiz and its answer;
     * 
     * it then parses the answer variable and returns the
     * user-friendly string representation of it.
     * 
     */

    if (type === 'single_input'| type === 'multiple_choice') {
      return answer
    }

    if (type === 'true_or_false') {
      return answer ? 'True' : 'False'
    }

    if (type === 'multiple_input') {
      return answer.join(', ')
    }
  }

  function restart() {
    /**
     * 
     * Restarts the quiz
     * 
     */

    results.value = false
    currNum.value = 0

    if (alwaysShuffle.value) {
      shuffleQuizOnce()
    }

    if (quizActivated.value) {
      checkCount.value = 0
      wrongCount.value = 0
      corrections.value = []

      quizJsonParser()
    }

    if (cardActivated.value) {
      cardJsonParser()
    }
  }

  function cardJsonParser() {
    disableCard()

    question.value = quiz.value[currNum.value].question

    answer.value = quiz.value[currNum.value].answer
    
    answerType.value = quiz.value[currNum.value].type

    activateCard()
  }

  function activateCard() {
    cardActivated.value = true
  }

  function disableCard() {
    cardActivated.value = false
  }

  function nextCard() {
    currNum.value + 1 >= quiz.value.length ? showResults() : (currNum.value++, cardJsonParser())
  }

  function previousCard() {
    currNum.value <= 0 ? null : (currNum.value--, cardJsonParser())    
  }
</script>

<template>
  <div class="main-content">
    <!-- Quiz -->

    <TransitionUpFadeSlide mode="out-in">
      <template v-if="!results">

      <!-- Pre Quiz Choice -->
      <!-- The user can either load a quiz from local file or load it from its saved quizzes database -->

        <template v-if="!loaded || loaded && (!quizActivated && !cardActivated && !quizIsAnimating)">
          <template v-if="loadType === 'databaseFile' || loadType === 'localFile'">
            <div id="pre-quiz" class="container-fluid text-center">
              <div id="back">
                <TypeButton 
                  v-model="loadType" 
                  button-value="" 
                  button-display="Back" 
                />
              </div>

              <div id="vertical-line"></div>

              <div id="load-file">
                <template v-if="loadType === 'databaseFile'">
                  <FromDatabase 
                    v-model="finalFormatted"
                    @file-is-loaded="loadFile" 
                  />
                </template>

                <template v-if="loadType === 'localFile'">
                  <TypeFileInput 
                    v-model="finalFormatted" 
                    :ref-local-file="localFile" 
                    @file-is-loaded="loadFile" 
                  />
                </template>
              </div>

              <div id="vertical-line"></div>

              <div disabled class="btn-group-vertical d-flex" role="group" aria-label="Vertical radio toggle button group">
                <input
                  @input="quizJsonParser"
                  id="btnradio1"
                  type="radio"
                  class="btn-check"
                  name="btnradio"
                  autocomplete="off"
                />
                <label :class="{'disabled': !loaded}" class="btn btn-outline-light" for="btnradio1"> 
                  Quiz
                </label>
                <input
                  @input="cardJsonParser"
                  id="btnradio2"
                  type="radio"
                  class="btn-check"
                  name="btnradio"
                  autocomplete="off"
                />
                <label :class="{'disabled': !loaded}" class="btn btn-outline-light" for="btnradio2"> 
                  Cards
                </label>
              </div>

            </div>
          </template>

          <template v-else>
            <div id="quiz" class="container-fluid text-center">
              <h3 class="mb-3">Choose a quiz file type</h3>
              <div id="load-type" class="container-fluid">
                <TypeRadio
                  v-model="loadType"
                  :alt-choices="['From Database', 'Local File']"
                  :choices="['databaseFile', 'localFile']"
                />
              </div>
            </div>
          </template>

        </template>

        <!-- Main quiz application-->

        <template v-if="loaded">
          <template v-if="quizActivated">
            <TransitionUpFadeSlide mode="out-in" appear>
              <div id="quiz" class="container-fluid">
                <div class="text-center mb-4">
                  <h6>{{ types[answerType] }}</h6>
                  <h3>Question {{ currNum + 1 }}</h3>
                  <span 
                    v-if="answerType === 'multiple_input'" 
                    class="badge text-bg-info"
                  >
                    {{ quiz[currNum].ordered ? 'The answers must be ordered.' : 'The answers can be unordered.'  }}
                  </span>
                </div>

                <div id="question" class="text-center">
                  {{ question }}
                </div>

                <div id="answer" class="text-center">
                  <template v-if="answerType === 'single_input'">
                    <TypeInput v-model="answer" display="Answer" @keyup.enter="checker" />
                  </template>

                  <template v-if="answerType === 'multiple_input'">
                    <template v-for="(item, index) in answerArr" :key="index">
                      <TypeInput 
                        @keyup.enter="checker"
                        :id="index"
                        display="Answer"
                        v-model="answerArr[index]"
                      />    
                    </template>
                  </template>

                  <template v-if="answerType === 'true_or_false'">
                    <div>
                      <TypeBoolean v-model="answer" @keyup.enter="checker" />
                    </div>
                  </template>

                  <template v-if="answerType === 'multiple_choice'">
                    <div id="multiple-choice" class="container-fluid">
                      <TypeRadio 
                        v-model="answer" 
                        :choices="choices"
                        @keyup.enter="checker"
                      />
                    </div>
                  </template>

                  <TypeButton @click="checker" button-display="Answer" class="mt-3" />
                </div>
              </div>
            </TransitionUpFadeSlide>
          </template>

          <template v-if="cardActivated">
            <div class="container-fluid text-center d-flex justify-content-center">
              <Card
                @next-card="nextCard" 
                @previous-card="previousCard"
                :curr-num="currNum"
              >
                <template #front>
                  <div class="mb-1 fs-6">
                    Question {{ currNum + 1 }} <span class="badge text-bg-secondary">{{ types[answerType] }}</span>
                  </div>
                  <div class="mb-1 fs-5">
                    {{ question }}
                  </div>
                </template>
                <template #back>
                  <div class="mb-2 fs-5">
                    <span class="badge text-bg-success">
                      Answer
                    </span>
                  </div>
                  <div class="fs-5">
                    <span>{{ answerParser(answerType, answer) }}</span>
                  </div>
                </template>
              </Card>
            </div>
          </template>
        </template>
      </template>

      <!-- Results -->

      <template v-if="results">
        <div id="results" class="container-fluid">
          <div id="try-buttons" class="text-start mb-5 text-center">
            <button class="btn btn-light me-1" @click="restart">Try again</button>
            <button class="btn btn-light ms-1" @click="$router.go(0)">Reset</button>
          </div>

          <template v-if="quizActivated">
            <div id="main-results-info" class="text-center">
              <div>
                <h5>
                  Total: {{ checkCount + wrongCount }}
                </h5>
              </div>
              <div>
                <h5>
                  Checks: {{ checkCount }}
                </h5>
              </div>
              <div>
                <h5>
                  Wrongs: {{ wrongCount }}
                </h5>
              </div>
            </div>        
          </template>

          <template v-for="index in corrections" :key="corrections">
            <div class="container-fluid text-start results-corrections">
              <h5>Number {{ index + 1 }}</h5>
              <h5> Type: {{ types[quiz[index].type] }} </h5>
              <h5 class="text-info">Question: {{ quiz[index].question }}</h5>
              <h5 class="text-danger">Answer: {{ answerParser(quiz[index].type, quiz[index].answer) }}</h5>
              <h5 class="text-success">
                {{ quiz[index].type === 'multiple_input' ? 'Points per item' : 'Points' }}: {{ quiz[index].points  }}
              </h5>
            </div>
          </template>
        </div>
      </template>
    </TransitionUpFadeSlide>
  </div>
</template>

<style scoped>
  .results-corrections {
    word-break: break-all;
    padding: 1rem 3rem 1rem .5rem;
    border-bottom: 1px solid #fff;
  }

  #load-type {
    width: 50%;
  }

  #multiple-choice {
    width: 50%;
  }

  #pre-quiz {
    display: flex;
    justify-content: center;
    gap: 2rem;
  }

  #results {
    width: 50%;
  }

  #load-file {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  #back {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  #vertical-line {
    height: 5rem;
    border-right: 2px solid rgb(173, 173, 173);
  }

  #quiz {
    width: 50%;
  }

  #question {
    text-align: center;
    word-break: break-all;
    margin-bottom: 1.5rem;
  }

  h6 {
    word-break: break-all;
  }

  @media only screen and (max-width: 1024px) {
    #quiz {
      width: 70%;
    }
  }

  @media only screen and (max-width: 768px) {
    #quiz {
      width: 90%;
    }

    #question, #answer {
      font-size: 15px;
    }

    #question {
      text-align: justify;
    }
  }

  @media only screen and (max-width: 675px) {
    .main-content {
      padding: 10rem 1rem 1rem 1rem;
    }

    #pre-quiz {
      flex-direction: column;
    }

    #vertical-line {
      display: none;
    }
  }

  @media only screen and (max-width: 450px) {
    #multiple-choice {
      width: 80%;
    }

    #results {
      width: 90%;
    }

    #load-type {
      width: 70%;
    }
  }

  @media only screen and (max-width: 325px) {
    #try-buttons {
      display: flex;
      flex-direction: column;
    }

    #try-buttons button {
      margin: 0 0 1rem 0 !important;
    }
  }
</style>
