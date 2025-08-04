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
                let registerBtn = document.getElementById('register-btn');

                if (exists) {
                    usernameInput.style.border = "2px solid #da4343";
                    msgElem.textContent = 'Username is already taken.';
                    registerBtn.disabled = true;
                } else {
                    usernameInput.style.border = "1px solid #008000";
                    msgElem.textContent = '';
                    registerBtn.disabled = false;
                }
            })
    })

    // ----------------- Check if passwords are the same -----------------
    const pw = document.getElementById('password')
    const pwRepeat = document.getElementById('password-repeat');

    pwRepeat.addEventListener('focusout', async function (event) {
        let password = document.getElementById('password').value;
        let password_repeat = document.getElementById('password-repeat').value;

        let msgElem = document.getElementById('form-warning-password');
        let registerBtn = document.getElementById('register-btn');

        if (password != password_repeat) {
            pw.style.border = "2px solid #da4343";
            pwRepeat.style.border = "2px solid #da4343";
            msgElem.textContent = 'Passwords must be the same.';
            registerBtn.disabled = true;
        } else {
            pw.style.border = "1px solid #008000";
            pwRepeat.style.border = "1px solid #008000";
            msgElem.textContent = '';
            registerBtn.disabled = false;
        }
    })

    // ----------------- Display Admin Token -----------------
    const adminCheckbox = document.getElementById('admin-checkbox');
    const adminTokenDiv = document.getElementById('admin-token-div');

    adminCheckbox.addEventListener("change", function() {
        if (adminCheckbox.checked){
            adminTokenDiv.style.display = "block";
        } else {
            adminTokenDiv.style.display = "none";
        }
    });

})