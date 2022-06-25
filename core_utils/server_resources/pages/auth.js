/******************
 * Auth Page
 */
class Auth {
    constructor() {
        this.token = null;
        this.token_url = "/token";

        // check if a token is already present in the session storage
        if ( sessionStorage.getItem( "token" ) !== null ) {
            this.token = sessionStorage.getItem( "token" );
        }
    }

    async fetch_token(username, password) {
        // fetch the access token from the server
        let data = new FormData();
        data.append("username", username);
        data.append("password", password);

        let response = await fetch(this.token_url, {
            method: "POST",
            body: data
        });
        if (response.ok) {
            let json = await response.json();
            // save the token in the session
            this.token = json.access_token;
            return this.token;
        }
        throw new Error(response.status);
    }


    async login(username, password, redirect_uri=null) {
        // get the token from the server
        await this.fetch_token(username, password);

        // save the token in the session storage
        // TODO: Security is currently between this and cookies. 
        sessionStorage.setItem("token", this.token);

        // redirect to the redirect_uri if specified
        if (redirect_uri) {
            window.location.href = redirect_uri;
        }
    }

    async logout(redirect_uri=null) {
        // Clear the session
        sessionStorage.clear();
        this.token = null;
    }


    async send_authorized_request(request_type, request_path, request_data=null) {
        // attach the token to the request
        let headers = new Headers();
        headers.append("Authorization", "Bearer " + this.token);

        // send the request
        let request = new Request(request_path, {
            method: request_type,
            headers: headers,
            body: request_data
        });

        // return the response
        let response = await fetch(request);
        if (response.ok) {
            return response;
        }
        throw new Error(response.status);
    }
}

export default Auth;