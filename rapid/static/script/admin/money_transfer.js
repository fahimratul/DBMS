function showTransferModal(button) {
    document.getElementById("modalTransactionId").innerText = button.dataset.id || "—";
    document.getElementById("modalDonorId").innerText = button.dataset.donorid || "—";
    document.getElementById("modalDonorName").innerText = button.dataset.name || "—";
    document.getElementById("modalDonationMessage").innerText = button.dataset.message || "No message provided";

    document.getElementById("transferModal").style.display = "block";
}


document.addEventListener("click", (e) => {
    if (e.target.matches(".details-btn")) {
        showTransferModal(e.target);
    }
});

document.getElementById("searchInput").addEventListener("keyup", function () {
    const query = this.value.toLowerCase();
    document.querySelectorAll("#transfers_table tbody tr").forEach(row => {
        row.style.display = Array.from(row.cells).some(td =>
            td.innerText.toLowerCase().includes(query)
        ) ? "" : "none";
    });
});
const transferModal = document.getElementById("transferModal");
const closeBtn = transferModal.querySelector(".close");

closeBtn.onclick = () => transferModal.style.display = "none";

window.onclick = (e) => {
    if (e.target === transferModal) transferModal.style.display = "none";
};
