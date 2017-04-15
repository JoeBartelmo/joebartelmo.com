
var firstToggle = true;

function fadeInElem(elem) {
    $('.fader').fadeOut();
    $('.fader').promise().then(function(){
        $(elem).fadeIn();
        if(!firstToggle) {
            $('#about').click();
        }
        else {
            firstToggle = false;
        }
    });
}

$(document).ready(function() {
    //for toggling fade in/out on each summary item
    $('#toggle-experience').on('click', function() {
        fadeInElem('#experience');
    });
    $('#toggle-languages').on('click', function() {
        fadeInElem('#languages');
    });
    $('#toggle-projects').on('click', function() {
        fadeInElem('#projects');
    });
    $('#toggle-hobbies').on('click', function() {
        fadeInElem('#hobbies');
    });

    $('.toggle-default').click();

});

