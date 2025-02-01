// Fetch data from Flask backend
fetch('http://127.0.0.1:5000/api/data')
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Display message in console
        document.querySelector("#flask-message").innerText = data.message;
    })
    .catch(error => console.error("Error fetching data:", error));

// Sending data to Flask
document.querySelector("#sendButton").addEventListener("click", () => {
    fetch('http://127.0.0.1:5000/api/send', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: "Hello from Frontend!" })
    })
    .then(response => response.json())
    .then(data => console.log(data.response))
    .catch(error => console.error("Error sending data:", error));
});



// Mobile menu functionality
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
const navLinksA = document.querySelectorAll('.nav-links a');

hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    hamburger.classList.toggle('active');
});

navLinksA.forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        hamburger.classList.remove('active');
    });
});  
// Slider functionality
const slides = document.querySelectorAll('.slide');
let currentSlide = 0;

function showSlide(index) {
    slides.forEach(slide => slide.classList.remove('active'));
    slides[index].classList.add('active');
}

setInterval(() => {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
}, 5000);

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
