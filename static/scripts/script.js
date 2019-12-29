$(document).ready(function () { 

    // Based on windows size, set canvas width and height
    let mediaQuerysize = window.matchMedia("(max-width: 575.98px)");

    function cardElementDimension(e) {
        if (e.matches) {
            $(".card").removeClass("w-50");
        }
        else {
            $(".card").addClass("w-50");
        }
    }

    // Call the function at run time in order to resize the canvas element dimension
    cardElementDimension(mediaQuerysize);

    // attach listener to respond on state changes
    mediaQuerysize.addListener(cardElementDimension);
})