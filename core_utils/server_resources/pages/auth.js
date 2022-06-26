/******************
 * Auth Page
 */
class Auth {
    static LOGOUT_WARNING_TIME = 5; // minutes
    static WARNING_INTERVAL = 3;

    constructor() {
        this.token = null;
        this.token_expiration = null;
        this.token_url = "/login";

        // Check if token_expiration is in the session
        let expiration = sessionStorage.getItem("token_expiration");
        if (expiration) {
            this.token_expiration = new Date(expiration);
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
            return json;
        }
        throw new Error(response.status);
    }

    async check_token() {
        // check if the token is expired
        if (this.token_expiration && this.token_expiration < new Date()) {
            // token is expired
            this.token = null;
            // redirect to login page
            window.location.href = "/sign-in.htm";
        }

        // check if token is less than 3 minutes from expiring
        if (this.token_expiration && this.token_expiration - new Date() < Auth.LOGOUT_WARNING_TIME * 60 * 1000 &&
             ( ! this.last_warning_time || this.last_warning_time < new Date() - Auth.WARNING_INTERVAL * 1000 * 60)) {
            let message = "Your session will expire in " + this.token_expiration.toLocaleTimeString() + " minutes.";
            // show warning
            alert(message);

            // save the warning time 
            this.last_warning_time = new Date();
        }
    }


    async login(username, password, redirect_uri=null) {
        // get the token from the server
        let token_data = await this.fetch_token(username, password);
        this.token = token_data.access_token;

        let now = new Date();
        let seconds = now.getSeconds() + token_data.expires_in;
        this.token_expiration = new Date(now.setSeconds(seconds));

        // save the token expiration in the session
        sessionStorage.setItem("token_expiration", this.token_expiration.toISOString());
    
        // redirect to the redirect_uri if specified
        if (redirect_uri) {
            window.location.href = redirect_uri;
        }
    }

    async logged_in() {
        // check if the token is expired
        if ( ! this.token_expiration || this.token_expiration < new Date()) {
            return false;
        } else {
            return true;
        }
    }

    async logout(redirect_uri=null) {
        // Clear the session
        sessionStorage.clear();
        this.token = null;

        // send a request to the server to logout
        let response = await fetch("/logout", {
            method: "POST"
        }).then(response => {
            if (response.ok) {
                if (redirect_uri) {
                    window.location.href = redirect_uri;
                } else {
                    window.location.href = "/sign-in.htm";
                }
                return true; 
            }
            throw new Error(response.status);
        }).catch(error => {
            console.log(error);
            // store a warning message in the session
            sessionStorage.setItem("logout_error", error.message);
            alert("Error logging out. Please try again.");
            return false;
        });
    }


    async send_authorized_request(request_type, request_path, request_data=null) {
        // check if the token is expired
        if ( ! this.token_expiration || this.token_expiration < new Date()) {
            // get a new token
            // TODO: implement refresh token
            window.location.href = "/sign-in.htm";
        }

        // send the request
        let request = new Request(request_path, {
            method: request_type,
            body: request_data
        });

        // return the response
        let response = await fetch(request);
        // if the user is not authenticated, redirect to the login page
        if (response.status == 401) {
            // set the token to null and expiration to null
            this.token = null;
            this.token_expiration = new Date();
            // clear the session
            sessionStorage.clear();
            window.location.href = "/sign-in.htm";
        }
        if (response.ok) {
            return response;
        }
        throw new Error(response.status);
    }
}

export default Auth;