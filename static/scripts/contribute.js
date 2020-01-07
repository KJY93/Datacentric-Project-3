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

    // display and hide the input field to let user to key in the manufacturer name
    // only shows if "others" is selected in the manufacturer dropdown list
    $("#manufacturer_option_selection").change(function () {
        if ($("#manufacturer_option_selection").val() === "Others") {
            $("#othersOption").append(`<input type="text" class="form-control" id="new_manufacturer" name="new_manufacturer" placeholder="Enter manufacturer name..." required>`); 
        };

        if ($("#manufacturer_option_selection").val() !== "Others") {
            $("#othersOption").empty();
        };
    })

    // WORK IN PROGRESS!!!
    // perform an AJAX query check before letting user submit the form
    $("#contributeForm").submit(function(event) {
        event.preventDefault();
        if ($("#manufacturer_option_selection").val() === "Others") {

            $.get('/contributecheck', {new_mfr:$("#new_manufacturer").val(), manufacturer:$("#manufacturer_option_selection").val(), cereal:$('input[name=cereal_name]').val()},
            function(data) {
                if (data.mfr_name_status == "taken") {
                    alert("This manufacturer already exist in the database.");
                }
                // allow differerent brand with same cereal name and different brand with different cereal name to be submitted as a new cereal item to the Cereals table
                else if (((data.mfr_name_status == "available") && (data.cereal_name_status == "taken")) || ((data.mfr_name_status == "available") && (data.cereal_name_status == "available"))) {
                    event.currentTarget.submit();
                }
            })
        }

        else if ($("#manufacturer_option_selection").val() !== "Others") {
            $.get('/contributecheck', {manufacturer:$("#manufacturer_option_selection").val(), cereal:$('input[name=cereal_name]').val()}, 
            function(data) {
                if (data.cereal_name_status == "taken") {
                    alert("This cereal already exist in the database.");
                }
                else if (data.cereal_name_status == "available") {
                    // submit to commit
                    event.currentTarget.submit();
                }
            })

        }
    })

})