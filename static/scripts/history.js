$(document).ready(function () {

    // Based on windows size, set card width and height
    let mediaQuerysize = window.matchMedia("(max-width: 575.98px)");

    function cardElementDimension(e) {
        if (e.matches) {
            $(".card").removeClass("w-75");
        }
        else {
            $(".card").addClass("w-75");
        }
    }

    // Call the function at run time in order to resize the card element dimension
    cardElementDimension(mediaQuerysize);

    // attach listener to respond on state changes
    mediaQuerysize.addListener(cardElementDimension);


    $("#updateDeleteRatings").click(function () {

        // when rating info is selected
        // populate the ratings that can be updated and deleted
        if (document.getElementById("updateDeleteRatings").hasAttribute("checked") === false) {

            $("#updateDeleteRatings").attr("checked", "checked");
            $("#updateDeleteCerealInfo").removeAttr("checked");
            $("#updateDeleteField").empty();

            $("#updateDeleteField").append('<hr>');

            for (let i = 0; i < rating_query.length; i++) {
                $("#updateDeleteField").append(`<p>Name: ${rating_query[i]['name']}</p>`);
                $("#updateDeleteField").append(`<p>Comment: ${rating_query[i]['comment']}</p>`);
                $("#updateDeleteField").append(`<p>Ratings: ${rating_query[i]['ratings']}</p>`);
                $("#updateDeleteField").append(`<button type="button" class="btn btn-secondary editRatingButton" value=${rating_query[i]['cereal_id']}><i class="far fa-edit fa-fw"></i></button>`);
                $("#updateDeleteField").append(`<button type="button" class="btn btn-secondary deleteRatingButton" value=${rating_query[i]['cereal_id']}><i class="fas fa-trash-alt fa-fw"></i></button>`);
                $("#updateDeleteField").append('<hr>');

            }

            // if edit rating button is clicked
            $(".editRatingButton").click(function () {
                $("#modalForm").empty();
                $("#modalForm").append(
                    `<div class="modal fade ratingsModal" role="dialog">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Update Your Ratings</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                                <div class="modal-body">
                                    <form>
                                        <div class="form-group">
                                            <input type="number" placeholder="Your ratings here (1 to 5)"
                                                class="form-control mb-3" name="user_ratings_update" min="0.00"
                                                step="0.01" max="5.00" required>
                                        </div>

                                        <div class="form-group">
                                            <textarea class="form-control" placeholder="Your comments here..."
                                                name="user_comment_update" rows="3"
                                                required></textarea>
                                        </div>

                                        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Submit</button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>`
                );

                $("form").attr("method", "post");
                let cereal_id_formatted = ($(this).val());

                $("form").attr("action", `/editratings/${cereal_id_formatted}`);
                $(".ratingsModal").modal('show');
            })

            // if delete rating button is clicked
            $(".deleteRatingButton").click(function () {
                $("#modalForm").empty();
                $("#modalForm").append(
                    `<div class="modal fade ratingsModal" role="dialog">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Delete Your Ratings</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                                <div class="modal-body">
                                    <form>
                                        <div class="form-group">
                                            Are you sure you want to delete this review ratings?
                                        </div>

                                        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Submit</button>

                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>`
                );

                $("form").attr("method", "post");
                let delete_cereal_id = ($(this).val());

                $("form").attr("action", `/deleteratings/${delete_cereal_id}`);
                $(".ratingsModal").modal('show');
            })

        }

    })

    
    $("#updateDeleteCerealInfo").click(function () {

        // if cereal info option is selected
        // show the user the cereals that they can edit or delete
        if (document.getElementById("updateDeleteCerealInfo").hasAttribute("checked") === false) {

            $("#updateDeleteCerealInfo").attr("checked", "checked");
            $("#updateDeleteRatings").removeAttr("checked");
            $("#updateDeleteField").empty();

            $("#updateDeleteField").append('<hr>');

            for (let j = 0; j < contribute_query.length; j++) {
                $("#updateDeleteField").append(`<p>Name: ${contribute_query[j]['name']}</p>`);
                $("#updateDeleteField").append(`<p>Manufacturer: ${contribute_query[j]['manufacturer_description']}</p>`);
                $("#updateDeleteField").append(`<button type="submit" class="btn btn-secondary editContributeButton" value=${contribute_query[j]['cereal_id']}><i class="far fa-edit fa-fw"></i></button>`);
                $("#updateDeleteField").append(`<button type="submit" class="btn btn-secondary deleteContributeButton" value=${contribute_query[j]['cereal_id']}><i class="fas fa-trash-alt fa-fw"></i></button>`);
                $("#updateDeleteField").append('<hr>');

            }

            // if edit cereal contribution button is clicked
            $(".editContributeButton").click(function () {
                $("#modalForm").empty();
                $("#modalForm").append(
                    `<div class="modal fade contributeModal" role="dialog">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Update Your Cereal Info</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                                <div class="modal-body">
                                    <form>
                                        <div class="input-group mb-3">
                                            <div class="input-group-prepend">
                                                <span class="input-group-text">Manufacturer</span>
                                            </div>

                                            <select class="custom-select" id="manufacturer_option_selection"
                                                name="manufacturer_option_selection" required>
                                                <option value="" selected disabled hidden>Choose...</option>

                                                ${mfr_list.map(item => `
                                                    <option value='${item}'> ${item}</option>`).join('')}
                                            </select>
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-prepend">
                                                <span class="input-group-text">Cereal</span>
                                            </div>
                                            <input name="cereal_name" type="text" class="form-control" required>
                                        </div>


                                        <div class="input-group mb-3">
                                            <div class="input-group-prepend">
                                                <span class="input-group-text">Cereal Type</span>
                                            </div>

                                            <select class="custom-select" id="cereal_option_list" name="cereal_option_list" required>
                                                <option value="" selected disabled hidden>Choose...</option>
                                                <option value="1">Cold</option>
                                                <option value="2">Hot</option>
                                            </select>
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-prepend">
                                                <span class="input-group-text">Calories</span>
                                            </div>
                                            <input type="number" class="form-control" name="calories" min="0.00" step="0.01" required>
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-prepend">
                                                <span class="input-group-text">Protein</span>
                                            </div>
                                            <input type="number" class="form-control" name="protein" min="0.00" step="0.01" required>
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-prepend">
                                                <span class="input-group-text">Fat</span>
                                            </div>
                                            <input type="number" class="form-control" name="fat" min="0.00" step="0.01" required>
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-prepend">
                                                <span class="input-group-text">Sodium</span>
                                            </div>
                                            <input type="number" class="form-control" name="sodium" min="0.00" step="0.01" required>
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-prepend">
                                                <span class="input-group-text">Fiber</span>
                                            </div>
                                            <input type="number" class="form-control" name="fiber" min="0.00" step="0.01" required>
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-prepend">
                                                <span class="input-group-text">Carbohydrates</span>
                                            </div>
                                            <input type="number" class="form-control" name="carbohydrates" min="0.00" step="0.01"
                                                required>
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-prepend">
                                                <span class="input-group-text">Sugars</span>
                                            </div>
                                            <input type="number" class="form-control" name="sugars" min="0.00" step="0.01" required>
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-prepend">
                                                <span class="input-group-text">Potassium</span>
                                            </div>
                                            <input type="number" class="form-control" name="potassium" min="0.00" step="0.01" required>
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-prepend">
                                                <span class="input-group-text">Vitamins</span>
                                            </div>
                                            <input type="number" class="form-control" name="vitamins" min="0.00" step="0.01" required>
                                        </div>

                                        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Submit</button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>`
                );

                $("form").attr("method", "post");
                let contribute_cereal_id = ($(this).val());

                $("form").attr("action", `/editcontribution/${contribute_cereal_id}`);
                $(".contributeModal").modal('show');
            })

            // if delete contribution button is clicked
            $(".deleteContributeButton").click(function () {
                $("#modalForm").empty();
                $("#modalForm").append(
                    `<div class="modal fade contributeModal" role="dialog">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Delete Your Contribution</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                                <div class="modal-body">
                                    <form>
                                        <div class="form-group">
                                            Are you sure you want to delete this cereal contribution?
                                        </div>

                                        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Submit</button>

                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>`
                );

                $("form").attr("method", "post");
                let delete_cereal_id = ($(this).val());

                $("form").attr("action", `/deletecontribution/${delete_cereal_id}`);
                $(".contributeModal").modal('show');
            })
        }
    })

})