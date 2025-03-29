document.addEventListener('DOMContentLoaded', function() {
    const presetForm = document.getElementById('preset-form');
    const themeInput = document.getElementById('preset-theme');
    const generateBtn = document.getElementById('generate-btn');
    const loadingSection = document.getElementById('loading');
    const successAnimation = document.getElementById('success-message');
    const errorMessage = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    const exampleChips = document.querySelectorAll('.chip');

    // Theme toggle button
    const themeSwitch = document.getElementById('theme-switch');
    const themeText = document.getElementById('theme-text');
    const body = document.body;

    // Check for saved user preference, default to dark mode
    const savedTheme = localStorage.getItem('theme') || 'dark-mode';

    // Set initial state based on saved theme
    if (savedTheme === 'light-mode') {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        themeSwitch.checked = true;
        themeText.textContent = 'Light Mode';
    } else {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        themeSwitch.checked = false;
        themeText.textContent = 'Dark Mode';
    }

    localStorage.setItem('theme', savedTheme);

    // Toggle theme
    themeSwitch.addEventListener('change', function() {
        if (this.checked) {
            body.classList.remove('dark-mode');
            body.classList.add('light-mode');
            themeText.textContent = 'Light Mode';
            localStorage.setItem('theme', 'light-mode');
        } else {
            body.classList.remove('light-mode');
            body.classList.add('dark-mode');
            themeText.textContent = 'Dark Mode';
            localStorage.setItem('theme', 'dark-mode');
        }
    });

    // Track if a download is in progress
    let downloadInProgress = false;

    // Handle form submission
    presetForm.addEventListener('submit', async function(event) {
        // Prevent the default form submission
        event.preventDefault();

        let preset = themeInput.value;

        if (!preset) {
            showError("Please enter a preset theme description");
            return;
        }

        // Sanitize the theme input
        preset = sanitizeTheme(themeInput.value);

        if (preset.length < 3 || preset.length > 100) {
            showError("Theme description must be between 3 and 100 characters");
            return;
        }

        if (downloadInProgress) {
            return;
        }

        // Show loading, hide other states
        loadingSection.classList.remove('hidden');
        successAnimation.classList.add('hidden');
        errorMessage.classList.add('hidden');
        generateBtn.disabled = true;
        downloadInProgress = true;

        try {
            // Create form data for the request
            const formData = new FormData();
            formData.append('theme', preset);

            // Get the altcha payload
            const altchaPayload = document.querySelector('input[name="altcha"]').value;
            formData.append('altcha', altchaPayload);

            // Send request to server
            const response = await fetch('/generate-preset', {
                method: 'POST',
                body: formData
            });

            //console.log("Response:", response);

            // Parse the JSON response
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate preset');
            }

            if (!data.success) {
                throw new Error(data.error || 'Failed to generate preset');
            }

            // Create and download the XMP file
            downloadXmpFile(data.xmp_content, data.preset_name);

            // Show success animation
            showSuccess();

        } catch (error) {
            console.error('Error:', error);
            showError(error.message);
        }
    });

    // Function to create and download an XMP file
    function downloadXmpFile(xmpContent, presetName) {
        // Create a blob with the XMP content
        const blob = new Blob([xmpContent], { type: 'application/xml' });

        // Create a URL for the blob
        const url = URL.createObjectURL(blob);

        // Create a temporary link element
        const link = document.createElement('a');
        link.href = url;
        link.download = `${presetName}.xmp`;

        // Append to the document, click it, and remove it
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // Clean up the URL object
        URL.revokeObjectURL(url);
    }

    // Function to show success state
    function showSuccess() {
        loadingSection.classList.add('hidden');
        errorMessage.classList.add('hidden');
        successAnimation.classList.remove('hidden');

        // Reset state after animation
        setTimeout(function() {
            successAnimation.classList.add('hidden');
            generateBtn.disabled = false;
            downloadInProgress = false;
        }, 3000);
    }

    // Function to show error state
    function showError(message) {
        loadingSection.classList.add('hidden');
        successAnimation.classList.add('hidden');
        errorText.textContent = message;
        errorMessage.classList.remove('hidden');
        generateBtn.disabled = false;
        downloadInProgress = false;
    }

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

function sanitizeTheme(input) {
    // Allow only letters, numbers, and spaces
    const sanitized = input.trim()
        .replace(/[^a-zA-Z0-9 ]/g, "")
        .substring(0, 100); // Limit to 100 characters

    console.log("Sanitized input:", sanitized);
    return sanitized;
}