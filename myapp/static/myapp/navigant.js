document.addEventListener("DOMContentLoaded", () => {
    // Événement pour ajouter un employé navigant
    const addBtn = document.getElementById("addNavigantBtn");
    addBtn.addEventListener("click", addNavigant);

    const tableBody = document.querySelector("tbody");
    tableBody.addEventListener("click", (event) => {
        const target = event.target;
        if (target.classList.contains("edit-btn")) editNavigant(event);
        else if (target.classList.contains("delete-btn")) deleteNavigant(event);
    });
});

function editNavigant(event) {
    const button = event.target;
    const id = button.getAttribute("data-id");
    const nom = button.getAttribute("data-nom");
    const prenom = button.getAttribute("data-prenom");
    const heuresVol = button.getAttribute("data-heures_vol");
    const heuresMoisVol = button.getAttribute("data-heures_mois_vol");
    const avions = button.getAttribute("data-avions").split(", ");

    document.getElementById("navigant-id").value = id;
    document.getElementById("navigant-nom").value = nom;
    document.getElementById("navigant-prenom").value = prenom;
    document.getElementById("navigant-heures_vol").value = heuresVol;
    document.getElementById("navigant-heures_mois_vol").value = heuresMoisVol;

    // Sélectionner les avions
    const selectAvions = document.getElementById("navigant-avions");
    for (let option of selectAvions.options) {
        option.selected = avions.includes(option.value);
    }

    const modal = new bootstrap.Modal(document.getElementById("editNavigantModal"));
    modal.show();

    const form = document.getElementById("editNavigantForm");
    form.onsubmit = (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        fetch(`/modifier-employe-navigant/`, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                // Mettre à jour la ligne du tableau
                button.setAttribute("data-nom", formData.get("nom"));
                button.setAttribute("data-prenom", formData.get("prenom"));
                button.setAttribute("data-heures_vol", formData.get("heures_vol"));
                button.setAttribute("data-heures_mois_vol", formData.get("heures_mois_vol"));

                const row = button.closest("tr");
                row.children[0].textContent = formData.get("nom");
                row.children[1].textContent = formData.get("prenom");
                row.children[2].textContent = formData.get("heures_vol");
                row.children[3].textContent = formData.get("heures_mois_vol");
                
                modal.hide();
            } else {
                alert(data.message);
            }
        });
    };
}

function deleteNavigant(event) {
    const button = event.target;
    const id = button.getAttribute("data-id");

    const modal = new bootstrap.Modal(document.getElementById("deleteNavigantModal"));
    modal.show();

    const confirmDelete = document.getElementById("confirmDeleteBtn");
    confirmDelete.onclick = () => {
        fetch(`/delete-employe-navigant/${id}/`, {
            method: "DELETE",
            headers: { "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                // Supprimer la ligne
                const row = button.closest("tr");
                row.remove();
                modal.hide();
            } else {
                alert(data.message);
            }
        });
    };
}

function addNavigant() {
    const modalAdd = new bootstrap.Modal(document.getElementById("addNavigantModal"));
    modalAdd.show();

    const formAdd = document.getElementById("addNavigantForm");
    formAdd.addEventListener("submit", (event) => {
        event.preventDefault();

        const formData = new FormData(formAdd);
        fetch("/add-employe-navigant/", {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                // Ajouter ligne au tableau
                const tableBody = document.querySelector("tbody");
                const newRow = document.createElement("tr");
                newRow.innerHTML = `
                    <td>${data.nom}</td>
                    <td>${data.prenom}</td>
                    <td>${data.date_embauche}</td>
                    <td>${data.avions.join(', ')}</td>
                    <td>${data.heures_vol}</td>
                    <td>${data.heures_mois_vol}</td>
                    <td>
                        <button class="btn btn-primary edit-btn" data-id="${data.id}" data-nom="${data.nom}" data-prenom="${data.prenom}" data-heures_vol="${data.heures_vol}" data-heures_mois_vol="${data.heures_mois_vol}" data-avions="${data.avions}">
                            Modifier
                        </button>
                    </td>
                    <td>
                        <button class="btn btn-danger delete-btn" data-id="${data.id}">
                            Supprimer
                        </button>
                    </td>
                `;
                tableBody.appendChild(newRow);
                modalAdd.hide();
            } else {
                alert(data.message);
            }
        });
    });
}
