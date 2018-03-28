
function onSignIn(googleUser) {
    // Useful data for your client-side scripts:
    var profile = googleUser.getBasicProfile();

    //Update home page with user data
    $("#title").text("Welcome to SpeechBuddy, " + profile.getGivenName() + ".");
    $("#sign-in").remove();
    $("#navCollapsed").append('<li id="signedin" class="nav-item"></li>');
    $("#signedin").append('<a id="email" href="" style="width: 80px"></a>');
    $("#email").text(profile.getEmail());

    // console.log("Image URL: " + profile.getImageUrl());
    // console.log("Email: " + profile.getEmail());

    // The ID token you need to pass to your backend:
    var id_token = googleUser.getAuthResponse().id_token;

    //send token to backend
    $.ajax({
        type: 'POST',
        url: '/api/googleOAuth/',
        data: {user_token:id_token},
        success: function(){
            console.log("OAuth post success!")
        }, 
        error: function(){
            alert('error saving token');
        }
    });
};
