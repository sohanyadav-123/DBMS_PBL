document.addEventListener('DOMContentLoaded', async () => {
    const tableBody = document.getElementById('tickets-table-body');
    const form = document.getElementById('create-ticket-form');

    // Load tickets
    const loadTickets = async () => {
        const tickets = await fetchJSON('/api/tickets');
        if (tickets && tableBody) {
            tableBody.innerHTML = '';
            tickets.forEach(t => {
                tableBody.insertAdjacentHTML('beforeend', `
                    <tr>
                        <td><a href="/ticket_details/${t.ticket_id}">#T${t.ticket_id}</a></td>
                        <td>${t.user_name || 'N/A'}</td>
                        <td>${t.category_name || 'N/A'}</td>
                        <td>${t.asset_tag || '-'}</td>
                        <td><span class="badge ${getBadgeClass(t.priority)}">${t.priority}</span></td>
                        <td><span class="badge ${getBadgeClass(t.status)}">${t.status}</span></td>
                        <td>${new Date(t.created_at).toLocaleDateString()}</td>
                        <td><a href="/ticket_details/${t.ticket_id}" class="btn" style="background:#e2e3e5; padding:0.25rem 0.5rem; font-size:0.875rem;">View</a></td>
                    </tr>
                `);
            });
        }
    };

    if (tableBody) loadTickets();

    // Setup form if it exists
    if (form) {
        // load categories
        const cats = await fetchJSON('/api/categories');
        const catSelect = document.getElementById('cat-select');
        if (cats && catSelect) {
            cats.forEach(c => {
                catSelect.insertAdjacentHTML('beforeend', `<option value="${c.category_id}">${c.name}</option>`);
            });
        }

        // load assets
        const assets = await fetchJSON('/api/assets');
        const assetSelect = document.getElementById('asset-select');
        if (assets && assetSelect) {
            assets.forEach(a => {
                assetSelect.insertAdjacentHTML('beforeend', `<option value="${a.asset_id}">${a.asset_tag} - ${a.type}</option>`);
            });
        }

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                category_id: catSelect.value,
                asset_id: assetSelect.value || null,
                priority: document.getElementById('priority-select').value,
                description: document.getElementById('desc-input').value
            };

            try {
                const res = await fetch('/api/tickets', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await res.json();
                if (res.ok) {
                    alert(result.message);
                    form.reset();
                    loadTickets();
                } else {
                    alert(result.error);
                }
            } catch (err) {
                console.error(err);
            }
        });
    }
});
