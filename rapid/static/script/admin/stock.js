const stockTableData = jsStockTableData;
function showStockModal(stockId) {
    const data = stockTableData.find(s => s.stock_id == stockId);
    if (!data) return;

    document.getElementById("modalStockId").innerText = data.stock_id;
    document.getElementById("modalPrice").innerText = data.price + " BDT";
    document.getElementById("modalQuantity").innerText = data.quantity;
    document.getElementById("modalPurchaseDate").innerText = data.purchase_date ? new Date(data.purchase_date).toLocaleDateString() : "—";
    document.getElementById("modalStockDate").innerText = data.stock_date ? new Date(data.stock_date).toLocaleDateString() : "—";
    document.getElementById("modalExpirationDate").innerText = data.expire_date ? new Date(data.expire_date).toLocaleDateString() : "—";
    document.getElementById("modalItemIds").innerText = data.item_id || "—";
    document.getElementById("modalItemTypes").innerText = data.item_name || "—";
    document.getElementById("modalAccountId").innerText = data.account_id || "—";

    document.getElementById("stockModal").style.display = "block";
}
document.getElementById("stock_search").addEventListener("keyup", function() {
    const query = this.value.toLowerCase();
    document.querySelectorAll("#stockTable tbody tr").forEach(row => {
        row.style.display = Array.from(row.cells).some(td =>
            td.innerText.toLowerCase().includes(query)
        ) ? "" : "none";
    });
});


// Event listeners
document.addEventListener("click", (e) => {
    if (e.target.matches(".details-btn")) {
        showStockModal(e.target.dataset.id);
    }
});

const modal = document.getElementById("stockModal");
modal.querySelector(".close").onclick = () => modal.style.display = "none";
window.onclick = e => { if (e.target === modal) modal.style.display = "none"; }