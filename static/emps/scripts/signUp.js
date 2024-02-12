$(document).ready(function() {
    // image slider
    // welcome text
    const welcomeText = $('#welcome');
    const welcome = welcomeText.text();
    welcomeText.text('');


    const scriptText = $('.script');
    const script = scriptText.text();
    scriptText.text('');

    function typeWelcomeText(text, i) {
        if (i < text.length) {
            welcomeText.text(welcomeText.text() + text.charAt(i));
            i++;
            setTimeout(function() {
                typeWelcomeText(text, i);
                // welcomeText.css('color', 'whitesmoke')
            }, 50); // Adjust typing speed here (milliseconds)
        } else {
            // Once welcome text is fully typed, start typing the script text

            typeScriptText(script, 0);
        }
    }

    function typeScriptText(text, i) {
        if (i < text.length) {
            scriptText.text(scriptText.text() + text.charAt(i));
            i++;
            setTimeout(function() {
                typeScriptText(text, i);
                // scriptText.css('color', 'whitesmoke')
            }, 30); // Adjust typing speed here (milliseconds)
        }
    }

    typeWelcomeText(welcome, 0);
});
