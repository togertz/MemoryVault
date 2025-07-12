document.addEventListener('DOMContentLoaded', async function() {

    console.log("Executing flash.js")

    const alertElements = document.querySelectorAll(".alert");

    alertElements.forEach(function (alert) {
        console.log("Setting timeout")
        setTimeout(function () {
            console.log("Removing after timeout")
            alert.style.transition = "opacity 1s ease-out";
            alert.style.opacity = 0;
            setTimeout(() => alert.remove(), 1000);
        }, 5000);
    });

})