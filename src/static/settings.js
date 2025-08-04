document.addEventListener('DOMContentLoaded', async function() {

    function setUpCollectionPeriodForm({
        durationSelectID,
        startDivId,
        startSelectID,
        infoFieldId
    }){
        const durationSelection = document.getElementById(durationSelectID);
        const startDiv = document.getElementById(startDivId);
        const startSelection = document.getElementById(startSelectID);
        const information_field = document.getElementById(infoFieldId);

        if (!durationSelection || !startDiv || !startSelection) return;

        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        let normalizeMonthYear = function (month, year) {
            const normalizedMonth =  ((month % 12) + 12) % 12;
            const yearAdjustment = Math.floor((month - normalizedMonth) / 12);
            const normalizedYear = year + yearAdjustment;

            return {
                "month": normalizedMonth,
                "year": normalizedYear
            };
        };
        const currentMonth = (new Date()).getMonth();
        const currentYear = (new Date()).getFullYear();

        let selectionFiller = function () {
            const duration = durationSelection.value;
            let numberOfMonths = 0;

            startSelection.innerHTML = "";

            switch (duration){
                case "1":
                    startDiv.style.visibility = "hidden";
                    let option = document.createElement("option");
                    option.value = currentMonth + "-" + currentYear;
                    option.textContent = monthNames[currentMonth] + " " + currentYear;
                    startSelection.appendChild(option);
                    break;
                case "3":
                    startDiv.style.visibility = "visible";
                    numberOfMonths = 3;
                    break;
                case "6":
                    startDiv.style.visibility = "visible";
                    numberOfMonths = 6;
                    break;
                case "12":
                    startDiv.style.visibility = "visible";
                    numberOfMonths = 12;
                    break;
                default :
                    break;
            }

            for (let index = currentMonth - numberOfMonths + 1; index <= currentMonth; index++) {
                let normalizedDate = normalizeMonthYear(index, currentYear);
                let option = document.createElement("option");
                option.value = (normalizedDate["month"]) + "-" + normalizedDate["year"];
                option.textContent = monthNames[normalizedDate["month"]] + " " + normalizedDate["year"];
                startSelection.appendChild(option);
            }
        };

        let informationFiller = function() {
            const duration = parseInt(durationSelection.value, 10);
            let [startMonth, startYear] = startSelection.value.split("-").map(Number);

            const endDate = normalizeMonthYear(startMonth + (duration - 1), startYear);
            information_field.innerHTML = "Collection peroid would end on last day of <b>" + monthNames[endDate["month"]]  + " " + endDate["year"] + "</b>.";
        };

        selectionFiller();
        informationFiller();

        durationSelection.addEventListener("change", async function (event) {
            selectionFiller();
            informationFiller();
        });

        startSelection.addEventListener("change", async function (event) {
            informationFiller();
        });
    }

    // Vault Form
    setUpCollectionPeriodForm({
        durationSelectID: "vault-collection-period-duration",
        startDivId: "vault-collection-period-start-div",
        startSelectID: "vault-collection-period-start",
        infoFieldId: "vault-period-end-info"
    })

    // Family Form
    setUpCollectionPeriodForm({
        durationSelectID: "family-collection-period-duration",
        startDivId: "family-collection-period-start-div",
        startSelectID: "family-collection-period-start",
        infoFieldId: "family-period-end-info"
    })
})