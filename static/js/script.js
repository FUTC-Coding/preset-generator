document.addEventListener('DOMContentLoaded', function() {
    const presetForm = document.getElementById('preset-form');
    const themeInput = document.getElementById('preset-theme');
    const generateBtn = document.getElementById('generate-btn');
    const loadingSection = document.getElementById('loading');
    const exampleChips = document.querySelectorAll('.chip');

    // Handle form submission
    presetForm.addEventListener('submit', function(event) {
        const theme = themeInput.value.trim();

        if (!theme) {
            event.preventDefault();
            alert('Please enter a preset theme description');
            return;
        }

        // Show loading, hide button
        loadingSection.classList.remove('hidden');
        generateBtn.disabled = true;
    });

    // Handle example chips
    exampleChips.forEach(chip => {
        chip.addEventListener('click', function() {
            const theme = this.dataset.theme;
            themeInput.value = theme;
            themeInput.focus();

            // Optional: Scroll to ensure the form is visible
            presetForm.scrollIntoView({ behavior: 'smooth' });
        });
    });
});