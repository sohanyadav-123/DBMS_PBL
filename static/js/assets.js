document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.getElementById('assets-table-body');
    const form = document.getElementById('add-asset-form');

    const loadAssets = async () => {
        const assets = await fetchJSON('/api/assets');
        if (assets && tableBody) {
            tableBody.innerHTML = '';
            assets.forEach(a => {
                tableBody.insertAdjacentHTML('beforeend', `
                    <tr>
                        <td>${a.asset_id}</td>
                        <td>${a.asset_tag}</td>
                        <td>${a.type}</td>
                        <td>${a.serial_no || '-'}</td>
                        <td>${a.purchase_date ? new Date(a.purchase_date).toLocaleDateString() : '-'}</td>
                        <td>${a.warranty_end ? new Date(a.warranty_end).toLocaleDateString() : '-'}</td>
                        <td><span class="badge ${getBadgeClass(a.status)}">${a.status}</span></td>
                        <td>
                            <button onclick="deleteAsset(${a.asset_id})" class="btn" style="background:var(--danger); color:white; padding:0.25rem 0.5rem; font-size:0.875rem;">Delete</button>
                        </td>
                    </tr>
                `);
            });
        }
    };

    if (tableBody) loadAssets();

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                asset_tag: document.getElementById('a-tag').value,
                type: document.getElementById('a-type').value,
                serial_no: document.getElementById('a-serial').value || null,
                purchase_date: document.getElementById('a-purchase').value || null,
                warranty_end: document.getElementById('a-warranty').value || null,
                status: document.getElementById('a-status').value
            };

            try {
                const res = await fetch('/api/assets', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await res.json();
                if (res.ok) {
                    alert(result.message);
                    form.reset();
                    loadAssets();
                } else {
                    alert(result.error);
                }
            } catch (err) {
                console.error(err);
            }
        });
    }

    window.deleteAsset = async (id) => {
        if (!confirm('Are you sure you want to delete this asset?')) return;
        try {
            const res = await fetch('/api/assets/' + id, { method: 'DELETE' });
            if (res.ok) {
                loadAssets();
            } else {
                const data = await res.json();
                alert(data.error || 'Failed to delete');
            }
        } catch (err) {
            console.error(err);
        }
    };
});
