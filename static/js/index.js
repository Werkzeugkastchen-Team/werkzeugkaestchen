function filterTools() {
    let input = document.getElementById('searchInput').value.toLowerCase();
        let toolCards = document.querySelectorAll('.tool-card');

        toolCards.forEach(card => {
            let title = card.getAttribute('data-title').toLowerCase();
            let description = card.getAttribute('data-description').toLowerCase();

            if (title.includes(input) || description.includes(input)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    }