<h1 align="center">Quizzer</h1>

## Introduction

Quizzer is a web app used for studying or reviewing. Users can create quizzes from the app or test themselves from already created quizzes. It is created to let users commonly use the app before an exam, quiz, and other forms of memory-related tasks.

## Specifications
Backend: Django with Django REST Framework

Frontend: VueJS

## How To Run

### Backend
- Open a terminal and navigate to the quizzer directory.
- In your terminal, run the command `python manage.py migrate`.
- After migration, run the command `python manage.py runserver` to run the server.

### Frontend
- After running the backend application, open a terminal and navigate towards the `frontend_quizzer` folder.
- Run the command `npm install`
- After installation, run the command `npm run dev` to run the development server of the frontend.

## Details

<h3 align="center">Backend</h3>

The backend is composed of two apps. Mainly: `backend_users` and `backend_quizzer`. Both are built as an API using a Django framework called `Django REST Framework`.

`backend_users` is a backend app used for the token-based user authentication system for the quizzer web app.

`backend_quizzer` is another backend app that handles operations of the saved quiz files from the database. It permits every user to upload, download, edit, and view a list of their saved files.

### Overview of `backend.users`
`/signup` - uses `views.signup` and method `POST`. Accepts a username and a password from the body and returns an authentication token of the user and their data. Let the users sign up for a new account/s.

`/login` - uses `views.login` and method `POST`. Accepts a username and a password from the body and returns an authentication token of the user and their data. Let the users log in on their account/s.

`/logout` - uses `views.logout` and method `POST`. Accepts a token, validates that token associated with the requesting user, and deletes the token from the database. Let the users log out of their accounts and delete the tokens from the database in the process.

`/delete` - uses `views.delete` and method `POST`. Accepts a token, and deletes the requesting user's account. Let the users delete their account/s.

### Overview of `backend.quizzer`

`upload_file` - uses `views.upload_file` and method `POST`. Accepts a token, and a JSON file data from the body. Let the users upload a file to their database.

`delete_file/<int:id>` - uses `views.delete_file` and method `PUT`. Accepts a token, and an id from the body. Uses the id to find the specified file and deletes it. Let the users deletes files they want to.

`update_file` - uses `views.update_file` and method `PUT`. Accepts a token, and a file id. Let the users update the current data of a quiz file.

`view_file/<int:id>` - uses `views.view_file` and method `GET`. Accepts a token and returns the quiz file as a json response. Let the users download or load the file.

`view_files` - uses `views.view_files` and method `GET`. Accepts a token and returns a list of all the files saved from the database of the requesting user. 

<h3 align="center">Frontend</h3>

The frontend is built using a Javascript framework called VueJS. It has a total of 8 Views of the web application. The frontend is responsible for letting the users create, save, or edit quizzes. They can also use the quizzes to test themselves either through flip cards or through a quiz.

#### Overview of the Frontend Components

`Auth.vue` - Responsible for making `LoginView.vue` and `SignUpView.vue` work. Both sign up and login user authentication logic goes here. Both has the same layout but with different descriptions and fetching methods. Compressed into one component for easy reusability.

`Card.vue` - Displays the flipping cards feature of the `QuizView.vue`.

`FromDatabase.vue` - Displays a list of quiz files the current user has in the database.

`Navbar.vue` - Displays the available options of the navigation bar at the top of the web application.

`Status.vue` - A component that is created for reusability. This component is responsible for displaying error, success, etc. badge messages of the web application.

`TransitionUpFadeSlide.vue` - Web application's default transition animation.

`TypeBoolean.vue` - Component that takes in a variable as a v-model. Displays a set of buttons; True, and False; that set's the variable's status as True or False.

`TypeButton.vue` - Component that takes in a variable as a v-model. Displays a placeholder of `buttonDisplay` if provided as prop. Changes the variable's value to the `buttonValue` provided as prop.

`TypeFileInput.vue` - Displays a file input that only takes a quiz JSON file. Loads that quiz JSON file to the variable passed down as v-model. 

`TypeInput.vue` - Displays a text input and the changes of the text input is applied to the variable using v-model.

`TypeRadio.vue` - Displays a buttons of choices passed down as a prop. Updates the value of the variable passed down as a v-model to the current selected button.

#### Overview of the Frontend Views

`AboutView.vue` - Additional description of the web application.

`CreateView.vue` - Created to let users create or edit their own quizzes. Users can either edit their quizzes locally or from their database if they are logged in.

`HomeView.vue` - Homepage of the web application.

`LoginView.vue` and `SignUpView.vue` - Both uses the component `Auth.vue`. Both views are responsible for user authentication system.

`QuizView.vue` - Can either load a quiz locally or from the database if the user is signed in. Loads the quiz files either as a quiz or flipping cards based on the user's preference.

`SavedView.vue` - If the user is signed in, it lets the user upload files. It shows a list of current uploaded files if there are any, displays two buttons to either delete or download the file.

`SettingsView.vue` - If the user is signed it, it lets the user log out of their accounts or delete them.
