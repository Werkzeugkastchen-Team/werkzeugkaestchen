// Add ripple effect to fancy buttons
document.addEventListener('DOMContentLoaded', function () {
    // Find all fancy buttons and add click event listener
    document.querySelectorAll('.fancy-button').forEach(button => {
        button.addEventListener('click', function (e) {
            // Create ripple element
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);

            // Position the ripple where clicked
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height) * 2;
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${e.clientX - rect.left - (size / 2)}px`;
            ripple.style.top = `${e.clientY - rect.top - (size / 2)}px`;

            // Remove ripple after animation completes
            setTimeout(() => {
                ripple.remove();
            }, 700);

            // Don't prevent default so that the link still works
        });
    });
});