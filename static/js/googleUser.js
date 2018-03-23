function onSignIn(googleUser) {
    // Useful data for your client-side scripts:
    var profile = googleUser.getBasicProfile();
    
    $("#title").text("Welcome to SpeechBuddy, " + profile.getGivenName() + ".");
    $("#sign-in").remove();
    $("#navCollapsed").append('<li id="signedin" class="nav-item"></li>');
    $("#signedin").append('<a id="email" href="/" style="width: 80px"></a>');
    $("#email").text(profile.getEmail());

    console.log("ID: " + profile.getId()); // Don't send this directly to your server!
    console.log('Full Name: ' + profile.getName());
    console.log('Given Name: ' + profile.getGivenName());
    console.log('Family Name: ' + profile.getFamilyName());
    console.log("Image URL: " + profile.getImageUrl());
    console.log("Email: " + profile.getEmail());

    // The ID token you need to pass to your backend:
    var id_token = googleUser.getAuthResponse().id_token;
    console.log("ID Token: " + id_token);
};
