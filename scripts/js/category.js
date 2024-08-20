document.addEventListener('DOMContentLoaded', function () {
    let category1Elements = document.querySelectorAll('.category1');
    let category2Elements = document.querySelectorAll('.category2');
    let back2category = document.querySelectorAll('.back-to-category');

    category1Elements.forEach(function (element) {
        element.addEventListener('click', function () {
            document.getElementById('category-objects').style.display = 'none';
            document.getElementById('category1-items').style.display = 'block';
            document.getElementById('back-to-category').style.display = 'block';
        });
    });

    category2Elements.forEach(function (element) {
        element.addEventListener('click', function () {
            document.getElementById('category-objects').style.display = 'none';
            document.getElementById('category2-items').style.display = 'block';
            document.getElementById('back-to-category').style.display = 'block';

            // Ustawienie float: left dla elementów w category2
            let category2Items = document.querySelectorAll('#category2-items .category');
            category2Items.forEach(function (item) {
                item.style.float = 'left';
            });
        });
    });

    back2category.forEach(function (element) {
        element.addEventListener('click', function () {
            document.getElementById('category-objects').style.display = 'block';
            document.getElementById('category1-items').style.display = 'none';
            document.getElementById('category2-items').style.display = 'none';
            document.getElementById('back-to-category').style.display = 'none';
        });
    });
});

function loadSign(signName) {
    window.location.href = `Edu-progress.php?sign=${encodeURIComponent(signName)}`;
}
