document.addEventListener('DOMContentLoaded', () => {
    // Navigation
    const navItems = document.querySelectorAll('.nav-item[data-view]');
    const views = document.querySelectorAll('main[id^="view-"]');
    const viewTitle = document.getElementById('view-title');
    const parentWord = document.getElementById('parent-word');
    const navWordTrigger = document.getElementById('nav-word-trigger');
    
    // Selectors
    const refTplSelect = document.getElementById('ref-tpl-select');
    const tplTableBody = document.getElementById('tpl-table-body');
    const historyTableBody = document.getElementById('history-table-body');
    const historyPagination = document.getElementById('history-pagination');

    // Modal Selectors
    const previewModal = document.getElementById('preview-modal');
    const docxContainer = document.getElementById('docx-container');
    const closeModalBtn = document.getElementById('close-modal');
    const downloadModalBtn = document.getElementById('download-modal-btn');
    const modalTitle = document.getElementById('modal-title');

    // Header Dropdown Selectors
    const dropdownTrigger = document.getElementById('user-dropdown-trigger');
    const dropdownMenu = document.getElementById('user-dropdown-menu');
    const displayUserName = document.getElementById('display-user-name');
    const userAvatarInitials = document.getElementById('user-avatar-initials');
    const logoutBtn = document.getElementById('logout-btn');
    const userStatusText = document.querySelector('.user-status');

    let currentHistoryPage = 1;

    // Title Mapping
    const viewTitles = {
        overview: 'Tổng quan hệ thống',
        reformat: 'Smart Reformat - Nâng cấp tài liệu',
        template: 'Quản lý kho Templates',
        history: 'Lịch sử báo cáo đã tạo'
    };

    // Initialize Lucide
    if (window.lucide) lucide.createIcons();

    // Toggle Submenu
    if (navWordTrigger) {
        navWordTrigger.addEventListener('click', () => {
            parentWord.classList.toggle('open');
        });
    }

    // Toggle Header Dropdown
    if (dropdownTrigger && dropdownMenu) {
        dropdownTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdownMenu.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (!dropdownTrigger.contains(e.target)) {
                dropdownMenu.classList.remove('active');
            }
        });
    }

    const switchView = (activeKey) => {
        const viewId = `view-${activeKey}`;
        window.location.hash = activeKey;

        views.forEach(v => {
            v.classList.toggle('hidden', v.id !== viewId);
        });

        navItems.forEach(item => {
            item.classList.toggle('active', item.dataset.view === activeKey);
        });
        
        if (['reformat', 'template', 'history'].includes(activeKey)) {
            parentWord.classList.add('open');
        }

        viewTitle.innerText = viewTitles[activeKey] || 'SmartPro';

        // Load Data
        if (activeKey === 'history' || activeKey === 'overview') loadHistory(currentHistoryPage);
        if (['template', 'overview', 'reformat'].includes(activeKey)) loadTemplates();
    };

    navItems.forEach(item => {
        item.addEventListener('click', () => switchView(item.dataset.view));
    });

    // --- AUTH LOGIC ---
    async function checkAuthAndLoad() {
        try {
            const resp = await fetch('/api/auth/me');
            if (resp.status === 401) {
                window.location.href = '/login';
                return;
            }
            const user = await resp.json();
            if (displayUserName) displayUserName.innerText = user.name;
            if (userAvatarInitials) {
                const initials = user.name.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);
                userAvatarInitials.innerText = initials || 'US';
            }
            
            if (userStatusText) {
                if (user.role === 'admin') {
                    userStatusText.innerText = "V.I.P Admin";
                    userStatusText.style.color = "var(--primary)";
                } else {
                    userStatusText.innerText = "Hội viên Pro";
                }
            }

            // After auth, load view
            const initialHash = window.location.hash.substring(1);
            switchView(initialHash && viewTitles[initialHash] ? initialHash : 'overview');
        } catch (e) {
            window.location.href = '/login';
        }
    }

    if (logoutBtn) {
        logoutBtn.onclick = async () => {
            if (confirm('Bạn có chắc muốn đăng xuất?')) {
                await fetch('/api/auth/logout', { method: 'POST' });
                window.location.href = '/login';
            }
        };
    }

    checkAuthAndLoad();

    // --- LOGIC: TEMPLATE PREVIEW MODAL ---
    window.openPreview = async (tid, name) => {
        previewModal.classList.add('active');
        docxContainer.innerHTML = '<div class="preview-placeholder">Đang tải và chuẩn bị nội dung...</div>';
        modalTitle.innerText = `Đang xem: ${name}`;
        
        downloadModalBtn.onclick = () => window.location.href = `/api/templates/preview/${tid}`;

        try {
            const response = await fetch(`/api/templates/preview/${tid}`);
            if (response.status === 401) return window.location.href = '/login';
            
            const blob = await response.blob();
            docxContainer.innerHTML = '';
            await docx.renderAsync(blob, docxContainer);
            lucide.createIcons();
        } catch (e) {
            console.error("Preview error:", e);
            docxContainer.innerHTML = '<div class="preview-placeholder" style="color:var(--danger)">Lỗi khi tải bản xem trước.</div>';
        }
    };

    const closePreview = () => {
        previewModal.classList.remove('active');
        docxContainer.innerHTML = '';
    };

    if (closeModalBtn) closeModalBtn.addEventListener('click', closePreview);
    if (previewModal) {
        previewModal.addEventListener('click', (e) => {
            if (e.target === previewModal) closePreview();
        });
    }

    // --- LOGIC: TEMPLATES ---
    async function loadTemplates() {
        try {
            const resp = await fetch('/api/templates');
            if (resp.status === 401) return window.location.href = '/login';
            
            const data = await resp.json();
            const options = data.map(t => `<option value="${t.id}">${t.name}${t.is_master ? ' (Master)' : ''}</option>`).join('');
            
            if (refTplSelect) refTplSelect.innerHTML = options;
            const statTpl = document.getElementById('stat-templates');
            if (statTpl) statTpl.innerText = data.length;

            if (tplTableBody) {
                tplTableBody.innerHTML = data.map(t => `
                    <tr>
                        <td style="font-weight:600">${t.name}</td>
                        <td>${new Date(t.created_at).toLocaleDateString('vi-VN')}</td>
                        <td>${t.is_master ? '<span class="badge" style="background:var(--primary-light); color:var(--primary)">Hệ thống</span>' : 'Tùy chỉnh'}</td>
                        <td>
                            <div style="display: flex; gap: 0.5rem;">
                                <button class="btn btn-secondary btn-sm" onclick="openPreview(${t.id}, '${t.name}')" title="Xem trực tiếp">
                                    <i data-lucide="eye" style="width:14px"></i>
                                </button>
                                ${t.is_master ? '' : `
                                <button class="btn btn-danger btn-sm" onclick="deleteTemplate(${t.id})" title="Xóa mẫu">
                                    <i data-lucide="trash-2" style="width:14px"></i>
                                </button>`}
                            </div>
                        </td>
                    </tr>
                `).join('');
                if (window.lucide) lucide.createIcons();
            }
        } catch (e) {
            console.error("Error loading templates:", e);
        }
    }

    window.deleteTemplate = async (id) => {
        if (!confirm('Xóa template này?')) return;
        const resp = await fetch(`/api/templates/${id}`, { method: 'DELETE' });
        if (resp.status === 401) return window.location.href = '/login';
        if (resp.ok) loadTemplates();
    };

    // --- LOGIC: REFORMAT ---
    const refBtn = document.getElementById('reformat-btn');
    if (refBtn) {
        refBtn.addEventListener('click', async () => {
            const title = document.getElementById('ref-title').value;
            const fileInput = document.getElementById('ref-file');
            if (!title || !fileInput.files[0]) return alert('Thiếu thông tin!');
            const fd = new FormData();
            fd.append('title', title);
            fd.append('version', document.getElementById('ref-version').value);
            fd.append('template_id', document.getElementById('ref-tpl-select').value);
            fd.append('file', fileInput.files[0]);
            
            refBtn.innerText = "Đang xử lý...";
            refBtn.disabled = true;
            try {
                const resp = await fetch('/api/reformat', { method: 'POST', body: fd });
                if (resp.status === 401) return window.location.href = '/login';
                const res = await resp.json();
                if (res.status === 'success') {
                    alert('Định dạng thành công!');
                    loadHistory(1);
                    window.location.href = `/api/download/${res.filename}`;
                } else alert('Lỗi: ' + res.detail);
            } finally {
                refBtn.innerText = "Tải lên & Tự động định dạng";
                refBtn.disabled = false;
            }
        });
    }

    // --- LOGIC: HISTORY & PAGINATION ---
    async function loadHistory(page = 1) {
        try {
            currentHistoryPage = page;
            const resp = await fetch(`/api/history?page=${page}&limit=10`);
            if (resp.status === 401) return window.location.href = '/login';
            const data = await resp.json();
            
            if (document.getElementById('stat-total')) document.getElementById('stat-total').innerText = data.total;
            
            if (historyTableBody) {
                historyTableBody.innerHTML = data.items.map(item => `
                    <tr>
                        <td style="font-weight: 500">${item.title}</td>
                        <td>v${item.version}</td>
                        <td>${new Date(item.created_at).toLocaleString('vi-VN')}</td>
                        <td><a href="/api/download/${item.filename}" class="btn btn-secondary btn-sm"><i data-lucide="download" style="width:14px"></i></a></td>
                    </tr>
                `).join('');
                renderPagination(data);
                if (window.lucide) lucide.createIcons();
            }
        } catch (e) {
            console.error("Error loading history:", e);
        }
    }

    function renderPagination(data) {
        if (!historyPagination) return;
        historyPagination.innerHTML = `
            <button class="page-btn" ${data.page === 1 ? 'disabled' : ''} id="prev-page">
                <i data-lucide="chevron-left"></i> Trước
            </button>
            <span class="page-info">Trang ${data.page} / ${data.pages || 1}</span>
            <button class="page-btn" ${data.page === data.pages || data.pages === 0 ? 'disabled' : ''} id="next-page">
                Sau <i data-lucide="chevron-right"></i>
            </button>
        `;
        document.getElementById('prev-page').onclick = () => loadHistory(data.page - 1);
        document.getElementById('next-page').onclick = () => loadHistory(data.page + 1);
        if (window.lucide) lucide.createIcons();
    }
});
