document.addEventListener('DOMContentLoaded', async function() {

    // ----------------- Check if username is already taken -----------------
    const usernameInput = document.getElementById('username');

    usernameInput.addEventListener('change', async function(event) {
        const username = usernameInput.value;

        fetch(`/u/username-taken?username=${encodeURIComponent(username)}`)
            .then(response => response.json())
            .then(data => {
                const exists = data.exists;
                let msgElem = document.getElementById('form-warning-username');

                if (exists) {
                    usernameInput.style.border = "2px solid #da4343";
                    msgElem.textContent = 'Username is already taken.';
                } else {
                    usernameInput.style.border = "1px solid #008000";
                    msgElem.textContent = '';
                }
            })
    })

    // ----------------- Check if passwords are the same -----------------
    const pw = document.getElementById('password')
    const pwRepeat = document.getElementById('password-repeat');

    pwRepeat.addEventListener('focusout', async function (event) {
        let password = document.getElementById('password').value;
        let password_repeat = document.getElementById('password-repeat').value;

        let msgElem = document.getElementById('form-warning-password')

        if (password != password_repeat) {
            pw.style.border = "2px solid #da4343";
            pwRepeat.style.border = "2px solid #da4343";
            msgElem.textContent = 'Passwords must be the same.';
        } else {
            pw.style.border = "1px solid #008000";
            pwRepeat.style.border = "1px solid #008000";
            msgElem.textContent = '';
        }
    })

})