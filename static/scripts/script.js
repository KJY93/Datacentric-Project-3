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

    // if manufacturer is selected
    $("#manufacturer").click(function () {

        if (document.getElementById("manufacturer").hasAttribute("checked") === false) {

            $("#manufacturer").attr("checked", "checked");
            // commit this
            $("#cereal_type").removeAttr("checked");
            $("#cereal_name").removeAttr("checked");
            $("#selectOptionSearchField").empty();

            $("#selectOptionSearchField").append(`<select class="custom-select" id="manufacturer_selection" name="manufacturer_selection" required></select>`);
            $("#manufacturer_selection").append('<option value="" selected disabled hidden>Choose...</option>');
            let manufacturer_list = ["American Home Food Products", "General Mills", "Kelloggs", "Nabisco", "Post", "Quacker Oats", "Ralston Purina"];
            for (let i = 0; i < manufacturer_list.length; i++) {
                $("#manufacturer_selection").append(`<option value="${manufacturer_list[i]}">${manufacturer_list[i]}</option>`);
            }

            $("#selectOptionSearchField").append(`<button type="submit" class="btn btn-outline-secondary" id="searchButton">Search</button>`)
        }
    })
})