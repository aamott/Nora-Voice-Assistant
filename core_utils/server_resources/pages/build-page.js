/**
 * Takes all elements of the nav.htm file and 
 * adds them to the page
 */
import Auth from "/auth.js";

let auth = new Auth();

async function setup_page() {
    let filename = "/components/nav.htm";

    fetch( filename )
        .then( response => response.text() )
        .then( async html => {
            let temp_container = document.createElement( 'div' );
            temp_container.innerHTML = html;
            
            let top_bar_el = await build_top_bar();

            let elements = temp_container.childNodes; 

            // get the body's first child
            const body = document.querySelector( 'body' );
            const firstChild = body.firstChild;


            // append elements to the beginning of the body
            // start with the top bar
            body.insertBefore( top_bar_el, firstChild );
            for (let element of elements) {
                body.insertBefore( element, firstChild );
            }
            
        } )
        .catch( error => console.log( error ) );
}

async function build_top_bar() {
    let top_bar_el = document.createElement( 'div' );
    top_bar_el.id = "top-bar";
    top_bar_el.appendChild(document.createElement('p'));

    let logged_in = await auth.logged_in();

    // add a sign in button that only shows when the user is not logged in
    let signin_btn = document.createElement( 'button' );
    signin_btn.type = 'button';
    signin_btn.id = 'signin-btn';
    signin_btn.innerHTML = 'Sign In';
    signin_btn.hidden = logged_in;
    signin_btn.onclick = function() {
        window.location.href = 'sign-in.htm';
    }
    top_bar_el.appendChild( signin_btn );

    // hide the logout button until the user is logged in
    let logout_btn = document.createElement( 'button' );
    logout_btn.type = 'button';
    logout_btn.id = 'logout-btn';
    logout_btn.innerHTML = 'Logout';
    logout_btn.hidden = ! logged_in;
    logout_btn.onclick = function() {
        auth.logout();
    }
    top_bar_el.appendChild( logout_btn );

    return top_bar_el;
}

window.addEventListener( 'load', () => {
    setup_page();
} );