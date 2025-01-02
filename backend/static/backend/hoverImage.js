document.addEventListener('DOMContentLoaded', () => {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'preview-overlay';
    document.body.appendChild(overlay);

    // Keep track of the current image being previewed
    let currPreview;

    // Get all preview links
    const links = document.querySelectorAll('.hover-preview');
    
    links.forEach(link => {
        preloadImg(link);

        link.addEventListener('mouseover', () => {
            currPreview = preloadImg(link);
            currPreview.style.display = 'block';
            overlay.style.display = 'block';
        });

        link.addEventListener('mouseout', () => {
            currPreview.style.display = 'none';
            overlay.style.display = 'none';
        });
    });
});


/**
 * Preloads the image at the link provided, creating an element with id matching the link.
 * @param {Element} link - the link element related to the image
 * @returns {Element}
 */
function preloadImg(link) {
    let preloadImg = document.getElementById(link.dataset.preview);
    if (preloadImg !== null)
        return preloadImg;
    preloadImg = document.createElement('img');
    preloadImg.className = 'preview-image';
    preloadImg.id = link.dataset.preview;
    preloadImg.src = link.dataset.preview;
    preloadImg.style.display = 'none';
    document.body.appendChild(preloadImg);
    return preloadImg;
}
