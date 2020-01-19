$(document).ready(function () {

    $("form").submit(function(event) {
        // prevent form from submitting before validation is done
        event.preventDefault();

        // AJAX query to validate whether username is already exist in the username
        $.get('/validate', { username: document.querySelector('input[name="username"]').value },
            function (data) {
                // Username cannot start or end with "" or '
                if (data.status === "invalid") {
                    alert("Username cannot start or end with \" or \'.");
                }
                // Username field cannot be empty
                else if (data.status === "") {
                    alert("Username field is empty!");
                }
                // Username is already taken
                else if (data.status === "taken") {
                    alert("Username is already taken!");
                }
                // Username is available
                else if (data.status === "available") {
                    // Check whether is password field empty
                    if ((!document.querySelector('input[name="password"]').value) || (!document.querySelector('input[name="repeat_password"]').value)) {
                        alert('Password field is empty!');
                    }

                    // call the check_pass_field function to validate if password fulfill the password combination criteria

                    const check_pass = check_pass_field();

                    if (check_pass === "true") {
                        event.currentTarget.submit();
                    }
                    else if (check_pass === "false") {
                        alert('Password must contain alphanumeric characters and special symbols(!@#$%^&*) and be 8 to 15 characters long.');
                    }
                    else if (check_pass === "not equal") {
                        alert('Password field(s) do not match!');
                    }
                }
            }, 'json');
        
        // function to check password combination
        function check_pass_field() {
            // if both passwords field are not empty (i.e the password & repeat password field)
            // proceed to check whether if they are equal
            // if they are equal, call the passverification function which uses REGEX to check the password combination
            if ((document.querySelector('input[name="password"]').value) && (document.querySelector('input[name="repeat_password"]').value)) {
                if ((document.querySelector('input[name="password"]').value) === (document.querySelector('input[name="repeat_password"]').value)) {
                    // add in to ensure password key in must consist of numbers, letters and special symbol //
                    const password_validity = passverification(document.querySelector('input[name="password"]').value);
                    if (password_validity === true) {
                        return "true";
                    }
                    else if (password_validity === false) {
                        return "false";
                    }
                }
                else if ((document.querySelector('input[name="password"]').value) !== (document.querySelector('input[name="repeat_password"]').value)) {

                    return "not equal";
                }
            }
        }

        // use regular expression in JavaScript for password validation
        function passverification(param1) {
            var regex = /^(?=.*[A-Z])(?=.*[0-9])(?=.*[a-z])(?=.*[!@#$%^&*]).{8,15}$/;
            return regex.test(param1);
        }

    });

});
