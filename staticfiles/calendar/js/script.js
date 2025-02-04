// Add functionality for navigation or dynamic event loading
document.addEventListener('DOMContentLoaded', () => {
    const eventLinks = document.querySelectorAll('.event-link');
  
    eventLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        alert(`Event: ${e.target.textContent}`);
      });
    });
  });
  