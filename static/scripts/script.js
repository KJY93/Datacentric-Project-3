$(document).ready(function () {

    // Based on windows size, set canvas width and height
    let mediaQuerysize = window.matchMedia("(max-width: 575.98px)");

    function cardElementDimension(e) {
        if (e.matches) {
            $(".card").removeClass("w-75");
        }
        else {
            $(".card").addClass("w-75");
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
            $("#cereal_type").removeAttr("checked");
            $("#cereal_name").removeAttr("checked");
            $("#calories").removeAttr("checked");
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

    // if cereal type is selected
    $("#cereal_type").click(function () {
        if (document.getElementById("cereal_type").hasAttribute("checked") === false) {

            $("#cereal_type").attr("checked", "checked");
            $("#manufacturer").removeAttr("checked");
            $("#cereal_name").removeAttr("checked");
            $("#calories").removeAttr("checked");
            $("#selectOptionSearchField").empty();

            $("#selectOptionSearchField").append(`<select class="custom-select" id="cereal_type_selection" name="cereal_type_selection" required></select>`);
            $("#cereal_type_selection").append('<option value="" selected disabled hidden>Choose...</option>');
            let cereal_type_list = ["Hot", "Cold"];
            for (let i = 0; i < cereal_type_list.length; i++) {
                $("#cereal_type_selection").append(`<option value="${cereal_type_list[i]}">${cereal_type_list[i]}</option>`);
            }

            $("#selectOptionSearchField").append(`<button type="submit" class="btn btn-outline-secondary" id="searchButton">Search</button>`)
        }
    })

    // if cereal name is selected
    $("#cereal_name").click(function () {
        if (document.getElementById("cereal_name").hasAttribute("cereal_name") === false) {
            $("#cereal_name").attr("checked", "checked");
            $("#manufacturer").removeAttr("checked");
            $("#cereal_type").removeAttr("checked");
            $("#calories").removeAttr("checked");
            $("#selectOptionSearchField").empty();

            $("#selectOptionSearchField").append(`<input type="text" id="cereal-name-input" name="cereal-name-input" class="typeahead tt-query" placeholder="Enter cereal name..." autocomplete="off" required>`);

            // Constructing the suggestion engine
            // Code modified from https://www.tutorialrepublic.com/twitter-bootstrap-tutorial/bootstrap-typeahead.php
            // Get cereal list from localStorage
            var cereal_array = JSON.parse(localStorage.getItem("cereal_list"));
            
            var cereal_array = new Bloodhound({
                datumTokenizer: Bloodhound.tokenizers.whitespace,
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                local: cereal_array
            });

            // Initializing the typeahead
            $('.typeahead').typeahead({
                hint: true,
                highlight: true, /* Enable substring highlighting */
                minLength: 1 /* Specify minimum characters required for showing suggestions */
            },
            {
                name: 'cereals',
                source: cereal_array
            });

            $("#selectOptionSearchField").append(`<button type="submit" class="btn btn-outline-secondary" id="searchButton">Search</button>`)
        }
    })

    // if calories is selected
    $("#calories").click(function () {
        if (document.getElementById("calories").hasAttribute("checked") === false) {
            
            // need to commit this 311219
            $("#calories").attr("checked", "checked");
            $("#manufacturer").removeAttr("checked");
            $("#cereal_name").removeAttr("checked");
            $("#cereal_type").removeAttr("checked");
            $("#selectOptionSearchField").empty();

            $("#selectOptionSearchField").append(`<select class="custom-select" id="calories_selection" name="calories_selection" required></select>`);
            $("#calories_selection").append('<option value="" selected disabled hidden>Choose...</option>');
            let calories_list = ["Below 100", "Above and include 100"];
            for (let i = 0; i < calories_list.length; i++) {
                $("#calories_selection").append(`<option value="${calories_list[i]}">${calories_list[i]} cal</option>`);
            }

            $("#selectOptionSearchField").append(`<button type="submit" class="btn btn-outline-secondary" id="searchButton">Search</button>`)
        }
    })  

})