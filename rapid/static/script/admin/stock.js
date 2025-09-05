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
    document.getElementById("modalItemTypes").innerText = data.item_type || "—";
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


document.addEventListener("click", (e) => {
    if (e.target.matches(".details-btn")) {
        showStockModal(e.target.dataset.id);
    }
});

const stockModal = document.getElementById("stockModal");
const addStockModal = document.getElementById("addStockModal");
const addItemModal = document.getElementById("addItemModal");

stockModal.querySelector(".close").onclick = () => stockModal.style.display = "none";
document.getElementById("closeAddStock").onclick = () => addStockModal.style.display = "none";
document.getElementById("closeAddItem").onclick = () => addItemModal.style.display = "none";

document.getElementById("openAddStockModal").onclick = () => addStockModal.style.display = "block";
document.getElementById("openAddItemModal").onclick = () => addItemModal.style.display = "block";

window.onclick = (e) => {
    if (e.target === stockModal) stockModal.style.display = "none";
    if (e.target === addStockModal) addStockModal.style.display = "none";
    if (e.target === addItemModal) addItemModal.style.display = "none";
};

const stockItemSelect = document.getElementById("newItemId");
const stockItemTypeInput = document.getElementById("autoItemType");
const stockItemIdInput = document.getElementById("autoItemId");

stockItemSelect.addEventListener("change", () => {
    const selectedOption = stockItemSelect.options[stockItemSelect.selectedIndex];
    stockItemIdInput.value = selectedOption.value;
    stockItemTypeInput.value = selectedOption.dataset.type || "";
});

document.getElementById("addStockForm").onsubmit = async (e) => {
    e.preventDefault();
    const data = {
        price: document.getElementById("newPrice").value,
        quantity: document.getElementById("newQuantity").value,
        expire_date: document.getElementById("newExpireDate").value || null,
        item_id: stockItemSelect.value,
        stock_date: document.getElementById("newStockDate").value,
        purchase_date: document.getElementById("newPurchaseDate").value
    };

    const res = await fetch("/admin_add_stock", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert("Stock added successfully!");
        addStockModal.style.display = "none";
        location.reload();
    } else alert("Failed to add stock");
};

const itemIdInput = document.getElementById("itemId");        
const itemTypeSelect = document.getElementById("itemType");  
const newTypeContainer = document.getElementById("newTypeContainer");
const newTypeInput = document.getElementById("newTypeName");

itemTypeSelect.addEventListener("change", () => {
    if (itemTypeSelect.value === "__new_type__") {
        newTypeContainer.style.display = "block";
        newTypeInput.required = true;
    } else {
        newTypeContainer.style.display = "none";
        newTypeInput.required = false;
    }
});

// --- Submit Add Item Form ---
document.getElementById("addItemForm").onsubmit = async (e) => {
    e.preventDefault();

    let typeName = itemTypeSelect.value;
    if (typeName === "__new_type__") {
        typeName = newTypeInput.value.trim();
        if (!typeName) return alert("Enter new type name");
    }

    const data = {
        item_id: itemIdInput.value,
        name: document.getElementById("itemName").value.trim(),
        type_name: typeName
    };

    if (!data.name || !data.type_name) return alert("Please fill all fields!");

    const res = await fetch("/admin_add_item", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert("Item added successfully!");
        addItemModal.style.display = "none";
        location.reload(); 
    } else alert("Failed to add item");
};
