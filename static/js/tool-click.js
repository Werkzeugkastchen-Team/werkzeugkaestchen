// Mobile detection and double-click handling for tools
document.addEventListener('DOMContentLoaded', function() {
    // Check if device is mobile by screen width rather than user agent for better reliability
    const isMobile = window.innerWidth <= 767;
    
    if (isMobile) {
        // Get all tool cards
        const toolCards = document.querySelectorAll('.tool-card a');
        
        // Keep track of the last clicked card and timestamp
        let lastClicked = null;
        let lastClickTime = 0;
          // Function to reset all cards
        function resetAllCards() {
            document.querySelectorAll('.card.first-click').forEach(card => {
                card.classList.remove('first-click');
            });
        }
        
        // Reset cards when clicking elsewhere on the page
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.tool-card')) {
                resetAllCards();
                lastClicked = null;
            }
        });
        
        // Add click event listeners to all tool cards
        toolCards.forEach(link => {
            link.addEventListener('click', function(e) {
                const currentTime = new Date().getTime();
                const clickTimeDiff = currentTime - lastClickTime;
                const currentCard = this;
                const card = currentCard.querySelector('.card');
                
                // If this is the first click or a click on a different card or time expired (3 seconds)
                if (lastClicked !== currentCard || clickTimeDiff > 3000) {
                    e.preventDefault(); // Prevent navigation
                      // Reset all cards first
                    resetAllCards();
                    
                    // Visual feedback for first click
                    card.classList.add('first-click');
                    
                    // Update last clicked card and time
                    lastClicked = currentCard;
                    lastClickTime = currentTime;
                    
                    // Auto reset after 3 seconds
                    setTimeout(function() {
                        if (lastClicked === currentCard) {
                            card.classList.remove('first-click');
                            lastClicked = null;
                        }
                    }, 3000);
                } 
                // Second click within time window - navigate to the tool
                else {
                    // Navigation happens naturally
                    return true;
                }
            });
        });
        
        // Also check on window resize
        window.addEventListener('resize', function() {
            const nowMobile = window.innerWidth <= 767;
            // If we switched from mobile to desktop
            if (isMobile && !nowMobile) {
                location.reload(); // Easy way to reset the behavior
            }
        });
    }
    // For desktop devices, keep default behavior
});
