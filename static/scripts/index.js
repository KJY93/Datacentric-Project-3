$(document).ready(function () {

    // declare an empty array to save all the JSON formatted cereals item
    var cereal_menu_item_record_array = [];

    // loop through all the cereal record and save it in an array
    for (let k = 0; k < cereal_menu_item_record.length; k++) {
        cereal_menu_item_record_array.push(cereal_menu_item_record[k]);
    }

    // save cereal list to localStorage so that it could be retrieved later on
    localStorage.setItem("cereal_list", JSON.stringify(cereal_menu_item_record_array));

    // save manufacturer list to localStorage it could be retrieved later on
    localStorage.setItem("manufacturer_list", JSON.stringify(manufacturer_list_array));

    // Constructing the suggestion engine for input search
    // Code modified from https://www.tutorialrepublic.com/twitter-bootstrap-tutorial/bootstrap-typeahead.php
    var cereal_menu_item_record_autocomplete_array = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        local: cereal_menu_item_record_array
    });

    // Initializing the typeahead
    $('.typeahead').typeahead({
        hint: true,
        highlight: true, /* Enable substring highlighting */
        minLength: 1 /* Specify minimum characters required for showing suggestions */
    },
    {
        name: 'cereals',
        source: cereal_menu_item_record_autocomplete_array
    });

    // declare an empty array to save all the JSON formatted manufacturer and cereal count data
    let manufacturer_array = [];
    let cereal_item_count_array = []; 

    // loop through the cereal item manufacturer count record and save the manufacturer and 
    // the cereal item to an array
    for (let i = 0; i < cereal_item_manufacturer_count_array_format.length; i++) {
        manufacturer_array.push(cereal_item_manufacturer_count_array_format[i]['manufacturer_description']);
        cereal_item_count_array.push(cereal_item_manufacturer_count_array_format[i]['count']);
    }

    // Generate random colors that are distinguishable from each other (using hsla)
    // https://mika-s.github.io/javascript/colors/hsl/2017/12/05/generating-random-colors-in-javascript.html
    let color_code_array = [];

    // Represents how many color will be generated
    // This will be based on how many items are there in the manufacturer category
    let color_quantity = manufacturer_array.length;
    let hue_delta = Math.trunc(360 / color_quantity);

    // set the saturation, alpha and lightness value to be constant
    let lightness = 50;
    let saturation = 100;
    let alpha = 1;

    for (let j = 0; j < color_quantity; j++) {
        let hue = j * hue_delta;
        color_code_array.push(`hsla(${hue},${saturation}%,${lightness}%,${alpha})`);
    }

    // Overview of cereals by manufacturer in the database
    // Doughnut Chart
    new Chart(document.getElementById("doughnut-chart"), {
        type: 'doughnut',
        data: {
            labels: manufacturer_array,
            datasets: [
                {
                    label: "Cereal manufacturer category (unit)",
                    backgroundColor: color_code_array,
                    data: cereal_item_count_array
                }
            ]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                labels: {
                    render: 'value',
                    arc: true,
                    fontColor: '#808080',
                    fontStyle: 'bold',
                    position: 'outside'
                }
            },

            title: {
                display: true,
                text: 'Cereal breakdown by manufacturer overview'
            }
        }
    });

    // empty array to store top 3 cereals with its highest calories values
    let cereal_item_array = [];
    let cereal_rating_array = [];

    // loop through the top 3 cereals item record and save the cereal item and its calories to an empty array
    for (let k = 0; k < top_3_cereals_item.length; k++) {
        // cereal_item_array.push(top_3_cereals_item[k]['name'])

        cereal_item_array.push(top_3_cereals_item[k]['manufacturer_with_cereal_name']);

        cereal_rating_array.push(top_3_cereals_item[k]['calories']);
    }

    // Bar chart to show menu with top 3 highest ratings cereal
    new Chart(document.getElementById("bar-chart"), {
        type: 'horizontalBar',
        data: {
            labels: cereal_item_array,
            datasets: [
                {
                    label: "Calories (cal)",
                    backgroundColor: ["hsla(30, 100%, 63%, 0.3)", "hsla(180, 48%, 52%, 0.3)", "hsla(204, 82%, 57%, 0.3)"],
                    data: cereal_rating_array
                }
            ]
        },
        options: {
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Top 3 cereals with highest calories   '
            },
            scales: {
                xAxes: [{ ticks: { min: cereal_rating_array[2] - 30 }}],
                yAxes: [{ ticks: { mirror: true, fontColor: '#808080' } }]
            }
        }
    });

    // Trigger this typeahead event when cereal name is being looked up
    jQuery('#autocomplete-input').on('typeahead:selected typeahead:autocompleted', function (e, datum) {

        jQuery.get('/query', { item: datum },
            function (data) {
                if (data["cereal"] === "not found") {
                    $("#cardResultBody").html("<div class='alert alert-info' role='alert'>No results found!</div>");
                }
                else {
                    let table_body = document.querySelector('tbody');
                    // commit 0701
                    let table_header = Object.keys(data["cereal"]);
                    let table_data = "";
                    let data_units = ["cal", "g", "g", "g", "mg", "g", "mg", "g", "%"];

                    // commit 0701
                    for (let d = 0; d < table_header.length; d++) {

                        if ((table_header[d]).includes("_")) {
                            // replace "_" with a spacebar
                            var formatted_table_header = table_header[d].replace(/_/g, " ");
                        }
                        else {
                            var formatted_table_header = table_header[d];
                        }

                        table_data += `<tr><td>${formatted_table_header}</td><td>${data["cereal"][table_header[d]]}${data_units[d]}</td></tr>`;
                    }

                    table_body.innerHTML = table_data.replace(/\"/g, "");
                }
            }, 'json');
    });

});