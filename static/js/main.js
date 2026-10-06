document.addEventListener('DOMContentLoaded', () => {
    // ── Global fetch helper ────────────────────────────
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
            showToast(err.message, 'error');
            return null;
        }
    };

    // ── Badge class mapper ─────────────────────────────
    window.getBadgeClass = (statusOrPriority) => {
        const map = {
            'Open':        'badge-open',
            'In Progress': 'badge-progress',
            'Resolved':    'badge-resolved',
            'Closed':      'badge-closed',
            'High':        'badge-high',
            'Medium':      'badge-medium',
            'Low':         'badge-low',
            'Available':   'badge-resolved',
            'Assigned':    'badge-open',
            'Maintenance': 'badge-progress',
            'Retired':     'badge-closed'
        };
        return map[statusOrPriority] || 'badge-open';
    };

    // ── Inject custom logout modal ─────────────────────
    const modalHTML = `
    <div id="logout-modal">
        <div class="modal-backdrop" id="logout-backdrop"></div>
        <div class="modal-box">
            <div class="modal-icon">👋</div>
            <h3>Signing Out?</h3>
            <p>You'll need to log back in to access the dashboard. Any unsaved work will be lost.</p>
            <div class="modal-actions">
                <button class="btn-cancel" id="logout-cancel">Stay Here</button>
                <a href="/logout" class="btn-logout" id="logout-confirm">Yes, Sign Out</a>
            </div>
        </div>
    </div>`;
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    const modal   = document.getElementById('logout-modal');
    const cancel  = document.getElementById('logout-cancel');
    const backdrop = document.getElementById('logout-backdrop');

    function openLogoutModal() {
        modal.classList.add('open');
    }
    function closeLogoutModal() {
        modal.classList.remove('open');
    }

    cancel.addEventListener('click', closeLogoutModal);
    backdrop.addEventListener('click', closeLogoutModal);

    // Intercept logout clicks (but NOT the confirm button inside the modal)
    document.addEventListener('click', (e) => {
        const logoutLink = e.target.closest('a[href="/logout"], .logout-btn[href="/logout"]');
        if (logoutLink && logoutLink.id !== 'logout-confirm') {
            e.preventDefault();
            openLogoutModal();
        }
    });

    // ── Minimal toast notification ─────────────────────
    window.showToast = (message, type = 'info') => {
        const toast = document.createElement('div');
        toast.style.cssText = `
            position:fixed; bottom:1.5rem; right:1.5rem; z-index:10000;
            background:${type === 'error' ? 'var(--danger)' : 'var(--success)'};
            color:#fff; padding:.75rem 1.25rem; border-radius:10px;
            font-size:.875rem; font-weight:600; font-family:inherit;
            box-shadow:0 8px 24px rgba(0,0,0,0.4);
            animation: slideUp .25s ease;
        `;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3500);
    };
});
