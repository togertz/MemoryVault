document.addEventListener('DOMContentLoaded', async function() {

    /**
     * Dynamically changes the available select-field options based on the user's input.
     * @param {Object} param0 - Configuration object
     * @param {string} param0.durationSelectID - ID of the duration select element
     * @param {string} param0.startDivId - ID of the start select div element
     * @param {string} param0.startSelectID - ID of the start select element
     * @param {string} param0.infoFieldId - ID of the information div element
     * @returns
     */
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
        /**
         * Normalizes month and year values so that month is always between 1 and 12.
         * @param {number} month - Month (can be out of range)
         * @param {number} year
         * @returns {{month: number, year:number}} - Normalized year and month
         */
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

        /**
         * Fills the select field with options based on the selected duration.
         * Also updates visibility of startDiv.
         */
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

        /**
         * Fills the information field with the end of the next Collection Period.
         */
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

    // Setup code for Vault form
    setUpCollectionPeriodForm({
        durationSelectID: "vault-collection-period-duration",
        startDivId: "vault-collection-period-start-div",
        startSelectID: "vault-collection-period-start",
        infoFieldId: "vault-period-end-info"
    })

    // Setup code for Family form
    setUpCollectionPeriodForm({
        durationSelectID: "family-collection-period-duration",
        startDivId: "family-collection-period-start-div",
        startSelectID: "family-collection-period-start",
        infoFieldId: "family-period-end-info"
    })
})