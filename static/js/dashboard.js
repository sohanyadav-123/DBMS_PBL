document.addEventListener('DOMContentLoaded', async () => {
    if (!document.getElementById('dashboard-stats')) return;

    const stats = await fetchJSON('/api/stats/dashboard');
    if (!stats) return;

    const container = document.getElementById('dashboard-stats');
    container.innerHTML = ''; // clear

    const keys = Object.keys(stats);
    keys.forEach(key => {
        const title = key.replace(/_/g, ' ').toUpperCase();
        const html = `
            <div class="stat-card">
                <h3>${title}</h3>
                <div class="value">${stats[key]}</div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', html);
    });

    // Also load recent tickets if the table exists
    const ticketsBody = document.getElementById('recent-tickets-body');
    if (ticketsBody) {
        const tickets = await fetchJSON('/api/tickets');
        if (tickets) {
            tickets.slice(0, 5).forEach(t => {
                ticketsBody.insertAdjacentHTML('beforeend', `
                    <tr>
                        <td><a href="/ticket_details/${t.ticket_id}">#T${t.ticket_id}</a></td>
                        <td>${t.user_name || 'N/A'}</td>
                        <td>${t.category_name || 'N/A'}</td>
                        <td><span class="badge ${getBadgeClass(t.priority)}">${t.priority}</span></td>
                        <td>${t.technician_name || 'Unassigned'}</td>
                        <td><span class="badge ${getBadgeClass(t.status)}">${t.status}</span></td>
                        <td>${new Date(t.created_at).toLocaleDateString()}</td>
                    </tr>
                `);
            });
        }
    }
});
