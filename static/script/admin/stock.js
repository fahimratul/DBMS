const stockTableData = {
    S001: {
        price: 1500,
        quantity: 50,
        purchaseDate: "10 Jan, 2025",
        stockDate: "12 Jan, 2025",
        expirationDate: "12 Jan, 2026",
        itemIds: ["I001"],
        itemTypes: ["Rice"],
        accountId: "A001"
    },
    S002: {
        price: 500,
        quantity: 120,
        purchaseDate: "15 Feb, 2025",
        stockDate: "16 Feb, 2025",
        expirationDate: "16 Feb, 2026",
        itemIds: ["I002"],
        itemTypes: ["Blankets"],
        accountId: "A002"
    },
    S003: {
        price: 300,
        quantity: 200,
        purchaseDate: "05 Mar, 2025",
        stockDate: "06 Mar, 2025",
        expirationDate: "06 Mar, 2026",
        itemIds: ["I003"],
        itemTypes: ["Cooking Oil"],
        accountId: null
    },
    S004: {
        price: 750,
        quantity: 80,
        purchaseDate: "20 Apr, 2025",
        stockDate: "21 Apr, 2025",
        expirationDate: "21 Apr, 2026",
        itemIds: ["I004"],
        itemTypes: ["Flour"],
        accountId: "A004"
    },
    S005: {
        price: 100,
        quantity: 500,
        purchaseDate: "01 May, 2025",
        stockDate: "02 May, 2025",
        expirationDate: "02 May, 2026",
        itemIds: ["I005"],
        itemTypes: ["Bottled Water"],
        accountId: null
    }
};

const stockBody = document.getElementById("stockTableBody");
for (const stockId in stockTableData) {
    const stock = stockTableData[stockId];
    const tr = document.createElement("tr");
    tr.innerHTML = `
        <td>${stockId}</td>
        <td>${stock.quantity}</td>
        <td>${stock.stockDate}</td>
        <td>${stock.expirationDate}</td>
        <td>${stock.itemIds.join(", ")}</td>
        <td>${stock.itemTypes.join(", ")}</td>
        <td><button class="details-btn" data-id="${stockId}">Details</button></td>
    `;
    stockBody.appendChild(tr);
}

const modal = document.getElementById("stockModal");
const closeBtn = modal.querySelector(".close");

function showStockModal(stockId) {
    const data = stockTableData[stockId];
    document.getElementById("modalStockId").innerText = stockId;
    document.getElementById("modalPrice").innerText = `${data.price} BDT`;
    document.getElementById("modalQuantity").value = data.quantity;
    document.getElementById("modalPurchaseDate").innerText = data.purchaseDate;
    document.getElementById("modalStockDate").innerText = data.stockDate;
    document.getElementById("modalExpirationDate").innerText = data.expirationDate;
    document.getElementById("modalItemIds").innerText = data.itemIds.join(", ");
    document.getElementById("modalItemTypes").innerText = data.itemTypes.join(", ");
    document.getElementById("modalAccountId").innerText = data.accountId ? data.accountId : "—";
    modal.style.display = "block";
}

document.getElementById("increaseQty").onclick = () => {
    const qtyInput = document.getElementById("modalQuantity");
    qtyInput.value = parseInt(qtyInput.value) + 1;
};
document.getElementById("decreaseQty").onclick = () => {
    const qtyInput = document.getElementById("modalQuantity");
    if (parseInt(qtyInput.value) > 0) qtyInput.value = parseInt(qtyInput.value) - 1;
};

document.addEventListener("click", (e) => {
    if (e.target.matches(".details-btn")) {
        const stockId = e.target.getAttribute("data-id");
        showStockModal(stockId);
    }
});
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("stock_search");
    const tableBody = document.getElementById("stockTableBody");

    searchInput.addEventListener("keyup", function () {
        const filter = searchInput.value.toLowerCase();
        const rows = tableBody.getElementsByTagName("tr");

        for (let i = 0; i < rows.length; i++) {
            let rowText = rows[i].innerText.toLowerCase();
            if (rowText.includes(filter)) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    });
});

closeBtn.onclick = () => modal.style.display = "none";
window.onclick = (e) => {
    if (e.target === modal) modal.style.display = "none";
};

function searchTable(inputId, tableId) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const filter = input.value.trim().toLowerCase();
  const rows = document.querySelectorAll(`#${tableId} tbody tr`);
  rows.forEach(row => {
    row.style.display = filter === '' || row.textContent.toLowerCase().includes(filter) ? '' : 'none';
  });
}
