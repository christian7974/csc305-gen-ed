const observer = new IntersectionObserver(entries => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            return;
        }
        // entry.target.classList.remove('fade-in');
    });
});

observer.observe(document.querySelector('#get-coursiquity #title-section'));
observer.observe(document.querySelector('#get-coursiquity #content-section'));
observer.observe(document.querySelector('#about-page #title-section'));
observer.observe(document.querySelector('#about-page #content-section'));
observer.observe(document.querySelector('#how-to-use #content'));

// Optional Feature of Making the Images Larger
// const imagesInTable = document.querySelectorAll("td img");
// imagesInTable.forEach(function(image) {
//     console.log(image);
//     image.addEventListener('mouseover', () => {
//         image.style.height = "400px";
//     });
//     image.addEventListener('mouseout', () => {
//         image.style.height = "300px";
//     });
// });


