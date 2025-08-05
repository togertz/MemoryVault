document.addEventListener("DOMContentLoaded", async function() {

    const vaultSelect = document.getElementById('vault-select');
    const periodSelect = document.getElementById('collection-period');

    /**
     * Update the available select options depending on the choosen vault.
     */
    const updatePeriodSelection = function(){
        let periodOptions = periods[vaultSelect.value];
        periodSelect.innerHTML = '';

        periodOptions.forEach(element => {
            let option = document.createElement('option');
            option.value = element["period_start"] + "-" + element["period_end"];
            option.textContent = element["period_start"] + " - " + element["period_end"];
            periodSelect.appendChild(option);
        });
    }

    if (vaultSelect){
        updatePeriodSelection();

        vaultSelect.addEventListener("change", async function() {
            updatePeriodSelection();
        });
    }
});