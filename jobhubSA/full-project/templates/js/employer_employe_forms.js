// Get all navigation links
const navLinks = document.querySelectorAll('.nav-link');

// Get all content divs
const contents = document.querySelectorAll('.container');

// Add event listeners to each navigation link
navLinks.forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();

        // Remove active class from all links
        navLinks.forEach(nav => nav.classList.remove('active'));

        // Hide all content divs
        contents.forEach(content => content.classList.remove('active'));

        // Add active class to the clicked link
        link.classList.add('active');

        // Show the corresponding content
        const contentId = link.id === 'nav1' ? 'content1' : 'content2';
        document.getElementById(contentId).classList.add('active');
    });
});
