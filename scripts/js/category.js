document.addEventListener('DOMContentLoaded', function () {
    // Pobieramy wszystkie elementy category1 i category2
    let category1Elements = document.querySelectorAll('.category1');
    let category2Elements = document.querySelectorAll('.category2');
    let back2category = document.querySelectorAll('.back-to-category');

    // Dodajemy nas³uchiwanie na klikniêcia dla wszystkich category1
    category1Elements.forEach(function (element) {
        element.addEventListener('click', function () {
            document.getElementById('category-objects').style.display = 'none'; // Ukrycie category-objects
            document.getElementById('category1-items').style.display = 'block'; // Odkrycie category1-items
            document.getElementById('back-to-category').style.display = 'block'; // Odkrycie category1-items
        });
    });

    // Dodajemy nas³uchiwanie na klikniêcia dla wszystkich category2
    category2Elements.forEach(function (element) {
        element.addEventListener('click', function () {
            document.getElementById('category-objects').style.display = 'none'; // Ukrycie category-objects
            document.getElementById('category2-items').style.display = 'block'; // Odkrycie category2-items
            document.getElementById('back-to-category').style.display = 'block'; // Odkrycie category1-items
            document.getElementById('category2-items').style.float = 'left'; // Odkrycie category2-items
        });
    });

    // Dodajemy nas³uchiwanie na klikniêcia dla wszystkich category2
    back2category.forEach(function (element) {
        element.addEventListener('click', function () {
            document.getElementById('category-objects').style.display = 'block'; // Odkrycie category-objects
            document.getElementById('category1-items').style.display = 'none'; // Ukrycie category1-items
            document.getElementById('category2-items').style.display = 'none'; // Ukrycie category2-items
            document.getElementById('back-to-category').style.display = 'none'; // Ukrycie przycisku
        });
    });
});