$(document).ready(function() {
    // image slider
    setInterval(function() {
        let $active = $('.image-slider img.active');
        let $next = $active.next().length ? $active.next() : $('.image-slider img:first');
        $active.removeClass('active');
        $next.addClass('active');
    }, 5000);

    // FAQ accordion
    $('.question').click(function() {
        $(this).toggleClass('active');
        $(this).find('i').toggleClass('fa-chevron-down fa-chevron-up');
        $(this).next('.answer').slideToggle();
        });

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
            }, 30); // Adjust typing speed here (milliseconds)
            $('.script i').addClass('letter-space')
        }
    }

    typeWelcomeText(welcome, 0);
});
