/*www.almasweb.org*/

function showLogin() {
    $(".login-link").addClass("active");
    $(".signup-link").removeClass("active");
    document.getElementById("trade_type").value = "buy";
    $(".confirm-password-row").hide()
    $(".forgot-password-row").show();
}

function showSignup() {
    $(".login-link").removeClass("active");
    $(".signup-link").addClass("active");
    document.getElementById("trade_type").value = "sell";
    $(".confirm-password-row").show()
    $(".forgot-password-row").hide();
}

function checkPasswordStrength() {
    if (!$("#password").val() || $(".login-link").hasClass("active")) return;

    const emoji = {
        0: "\u{1F628}", // Fearful
        1: "\u{1F616}", // Confounded
        2: "\u{1F61E}", // Disappointed
        3: "\u{1F615}", // Confused
        4: "\u{1F603}" // Grinning
    };
    const result = zxcvbn($("#password").val());
    const warning = result.feedback.warning || "";
    const suggestion = result.feedback.suggestions.join(", ").replace(/,/g, "") || "";

    $("#password-strength").html(emoji[result.score]);
    $(".help-text").text(`سعی کنید پسوردتان بهتر شود !`);
}

function init() {
    $(".login-link").on("click", showLogin);
    $(".signup-link").on("click", showSignup);
    $("#password")
        .on("input focus", checkPasswordStrength)
        .on("blur", () => $("#password-strength, .help-text").empty());
}

$(init);
/*www.almasweb.org*/