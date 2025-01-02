document.addEventListener('DOMContentLoaded', () => {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'preview-overlay';
    document.body.appendChild(overlay);

    // Create a single preview image element to be reused
    const preview = document.createElement('img');
    preview.className = 'preview-image';
    document.body.appendChild(preview);

    // Get all preview links
    const links = document.querySelectorAll('.hover-preview');
    
    links.forEach(link => {
        link.addEventListener('mousemove', (e) => {
            preview.src = link.dataset.preview;
            preview.style.display = 'block';
            overlay.style.display = 'block';
        });

        link.addEventListener('mouseout', () => {
            preview.style.display = 'none';
            overlay.style.display = 'none';
        });
    });
});
