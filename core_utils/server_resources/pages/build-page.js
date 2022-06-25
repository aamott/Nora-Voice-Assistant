/**
 * Takes all elements of the nav.htm file and 
 * adds them to the page
 */
function setup_page() {
    let filename = "/components/nav.htm";

    fetch( filename )
        .then( response => response.text() )
        .then( html => {
            let temp_container = document.createElement( 'div' );
            temp_container.innerHTML = html;

            // This will not work if there is anything (including comments) before the target element!
            let elements = temp_container.childNodes; 
            console.log(elements);

            // get the body's first child
            const body = document.querySelector( 'body' );
            const firstChild = body.firstChild;


            // append elements to the beginning of the body
            for (let element of elements) {
                console.log(element);
                body.insertBefore( element, firstChild );
            }
        } )
        .catch( error => console.log( error ) );
}

window.addEventListener( 'load', setup_page );