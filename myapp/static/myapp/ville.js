document.addEventListener("DOMContentLoaded", () => {
    // Événement bouton Ajouter
    const addBtn = document.getElementById("addVilleBtn");
    addBtn.addEventListener("click", addVille);

    const tableBody = document.querySelector("tbody");
    tableBody.addEventListener("click", (event) => {
        const target = event.target;
        // Modifier ou Supprimer
        if (target.classList.contains("edit-btn")) editVille(event);
        else if (target.classList.contains("delete-btn")) deleteVille(event);
    });
});

function editVille(event) {
    const button = event.target;
    const id = button.getAttribute("data-id");
    const name = button.getAttribute("data-nom");
    const country = button.getAttribute("data-nom_pays");

    // Remplir modal
    document.getElementById("ville-id").value = id;
    document.getElementById("ville-nom").value = name;
    document.getElementById("ville-nom-pays").value = country;

    const modal = new bootstrap.Modal(document.getElementById("editVilleModal"));
    modal.show();

    const form = document.getElementById("editVilleForm");
    form.onsubmit = (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        fetch(`/modifier-ville/`, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);

                // Mettre à jour les données du bouton
                button.setAttribute("data-nom", formData.get("nom"));
                button.setAttribute("data-nom_pays", formData.get("nom_pays"));
                const row = button.closest("tr");
                row.children[0].textContent = formData.get("nom");
                row.children[1].textContent = formData.get("nom_pays");

                modal.hide();
            } else alert(data.message);
        });
    };
}

function deleteVille(event) {
    const button = event.target;
    const id = button.getAttribute("data-id");

    const modal = new bootstrap.Modal(document.getElementById("deleteVilleModal"));
    modal.show();

    const confirmDelete = document.getElementById("confirmDeleteBtn");
    confirmDelete.onclick = () => {
        fetch(`/delete-ville/${id}/`, {
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
            } else alert(data.message);
        });
    };
}

function addVille() {
    const modalAdd = new bootstrap.Modal(document.getElementById("addVilleModal"));
    modalAdd.show();

    const formAdd = document.getElementById("addVilleForm");
    formAdd.addEventListener("submit", (event) => {
        event.preventDefault();

        const formData = new FormData(formAdd);
        fetch("/add-ville/", {
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
                    <td>${data.nom_pays}</td>
                    <td>
                        <button class="btn btn-primary edit-btn" data-id="${data.id}" data-nom="${data.nom}" data-nom_pays="${data.nom_pays}">
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
            } else alert(data.message);
        });
    });
}
