document.addEventListener('DOMContentLoaded', async function() {


    const alertElements = document.querySelectorAll(".alert");

    alertElements.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = "opacity 1s ease-out";
            alert.style.opacity = 0;
            setTimeout(() => alert.remove(), 1000);
        }, 20000);
    });

})