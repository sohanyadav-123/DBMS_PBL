document.addEventListener('DOMContentLoaded', () => {
    // Shared functions for API calls and UI updates
    window.fetchJSON = async (url, options = {}) => {
        try {
            const response = await fetch(url, {
                headers: { 'Content-Type': 'application/json' },
                ...options
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'API Error');
            return data;
        } catch (err) {
            console.error(err);
            alert(err.message);
            return null;
        }
    };

    window.getBadgeClass = (statusOrPriority) => {
        const map = {
            'Open': 'badge-open',
            'In Progress': 'badge-progress',
            'Resolved': 'badge-resolved',
            'Closed': 'badge-closed',
            'High': 'badge-high',
            'Medium': 'badge-medium',
            'Low': 'badge-low',
            'Available': 'badge-resolved',
            'Assigned': 'badge-open',
            'Maintenance': 'badge-progress',
            'Retired': 'badge-closed'
        };
        return map[statusOrPriority] || 'badge-open';
    };

    // Global logout confirmation
    document.addEventListener('click', (e) => {
        const logoutLink = e.target.closest('a[href="/logout"]');
        if (logoutLink) {
            if (!confirm('Are you sure you want to log out?')) {
                e.preventDefault();
            }
        }
    });
});
