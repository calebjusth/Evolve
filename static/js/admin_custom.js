// static/js/admin_custom.js

document.addEventListener('DOMContentLoaded', function() {
    // Enhance user profile in navbar
    const userPanel = document.querySelector('.user-panel');
    if (userPanel) {
        // Add custom profile picture if available
        const profileImage = userPanel.querySelector('img');
        if (profileImage && !profileImage.src.includes('default')) {
            profileImage.style.boxShadow = '0 2px 4px rgba(1, 177, 47, 0.3)';
        }
    }
    
    // Add icons to action buttons
    
    const saveButtons = document.querySelectorAll('.btn-primary, .btn-primary-custom');
    saveButtons.forEach(btn => {
        if (btn.textContent.includes('Save')) {
            btn.innerHTML = '<i class="fas fa-save mr-1"></i>' + btn.innerHTML;
        }
    });
    
    const deleteButtons = document.querySelectorAll('.btn-danger, .btn-danger-custom');
    deleteButtons.forEach(btn => {
        if (btn.textContent.includes('Delete')) {
            btn.innerHTML = '<i class="fas fa-trash-alt mr-1"></i>' + btn.innerHTML;
        }
    });
});