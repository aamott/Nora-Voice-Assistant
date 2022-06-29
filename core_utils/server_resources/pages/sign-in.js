/***********************
 * Sign-up page
 */
import Auth from './auth.js';

let auth = new Auth();

function build_signin_form() {
    let container = document.getElementById("signin");
    let signin_form = document.createElement("form");

    let username_input = document.createElement("input");
    username_input.setAttribute("type", "text");
    username_input.setAttribute("name", "username");
    username_input.setAttribute("placeholder", "Username");
    signin_form.appendChild(username_input);

    let password_input = document.createElement("input");
    password_input.setAttribute("type", "password");
    password_input.setAttribute("name", "password");
    password_input.setAttribute("placeholder", "Password");
    signin_form.appendChild(password_input);

    let submit_button = document.createElement("input");
    submit_button.setAttribute("type", "submit");
    submit_button.setAttribute("value", "Sign in");
    signin_form.appendChild(submit_button);
    
    // When the submit button is clicked, run auth.login()
    submit_button.addEventListener("click", function(event) {
        event.preventDefault();
        console.log("Signing in...");
        auth.login(username_input.value, password_input.value, "/");
    }
    );

    // append the form to the container
    container.appendChild(signin_form);
}

window.addEventListener("load", build_signin_form);