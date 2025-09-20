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

    if (e.target.matches(".delete-btn")) {
        const id = e.target.dataset.id;
        if (!id) return;
        if (confirm("⚠️ Are you sure you want to delete this account?")) {
            fetch(moneyTransferUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ delete_account_id: id })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) location.reload();
                else alert("❌ " + (data.error || "Failed to delete account"));
            })
            .catch(err => {
                console.error(err);
                alert("❌ Network error");
            });
        }
    }
});

const transferModal = document.getElementById("transferModal");
const closeTransferBtn = transferModal?.querySelector(".close");
if (closeTransferBtn) closeTransferBtn.onclick = () => transferModal.style.display = "none";

const addAccountModal = document.getElementById("addAccountModal");
document.getElementById("openAddAccountModal").onclick = () => addAccountModal.style.display = "block";
document.getElementById("closeAddAccount").onclick = () => addAccountModal.style.display = "none";

window.onclick = (e) => {
    if (e.target === transferModal) transferModal.style.display = "none";
    if (e.target === addAccountModal) addAccountModal.style.display = "none";
};

document.getElementById("addAccountForm").onsubmit = async (e) => {
    e.preventDefault();

    const accountId = document.getElementById("accountId").value.trim();
    const accountName = document.getElementById("accountName").value.trim();
    const methodName = document.getElementById("methodName").value.trim();

    if (!accountId || !accountName || !methodName) {
        alert("❌ Please fill all fields!");
        return;
    }

    try {
        const res = await fetch(moneyTransferUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                new_account: {
                    id: accountId,
                    name: accountName,
                    method: methodName
                }
            })
        });

        const result = await res.json();
        if (res.ok) {
            alert("✅ " + result.success);
            addAccountModal.style.display = "none";
            location.reload();
        } else {
            alert("❌ " + (result.error || "Failed to add account"));
        }
    } catch (err) {
        console.error(err);
        alert("❌ Network error");
    }
};

document.getElementById("account_search").addEventListener("keyup", function () {
    const query = this.value.toLowerCase();
    document.querySelectorAll("#accountTable tbody tr").forEach(row => {
        row.style.display = Array.from(row.cells).some(td =>
            td.innerText.toLowerCase().includes(query)
        ) ? "" : "none";
    });
});

document.getElementById("searchInput").addEventListener("keyup", function () {
    const query = this.value.toLowerCase();
    document.querySelectorAll("#transfers_table tbody tr").forEach(row => {
        row.style.display = Array.from(row.cells).some(td =>
            td.innerText.toLowerCase().includes(query)
        ) ? "" : "none";
    });
});
