let books = [];

async function loadBooks() {
    const response = await fetch('books.json');
    books = await response.json();
    displayBooks();
}

function createBookElement(book) {
    const bookCol = document.createElement('div');
    bookCol.className = 'col-lg-2 col-md-3 col-sm-6 mb-4';
    bookCol.innerHTML = `
        <div class="card h-100">
            <img src="${book.ImageLink}" class="card-img-top book-cover" alt="${book.Title}">
            <div class="card-body">
                <h5 class="card-title book-title">${book.Title}</h5>
                <p class="card-text">Rating: ${'★'.repeat(book.Rating)}${'☆'.repeat(5 - book.Rating)}</p>
            </div>
        </div>
    `;
    bookCol.addEventListener('click', () => showBookDetails(book));
    return bookCol;
}

function showBookDetails(book) {
    const modal = new bootstrap.Modal(document.getElementById('bookModal'));
    const modalTitle = document.querySelector('#bookModal .modal-title');
    const modalBody = document.querySelector('#bookModal .modal-body');

    modalTitle.textContent = book.Title;
    modalBody.innerHTML = `
        <img src="${book.ImageLink}" class="img-fluid mb-3" alt="${book.Title}">
        <p><strong>Date Published:</strong> ${book['Date Published']}</p>
        <p><strong>Date Read:</strong> ${book['Date Read']}</p>
        <p><strong>Tags:</strong> ${book.Tags.join(', ')}</p>
        <p><strong>Goodreads:</strong> <a href="${book['GoodReads Link']}" target="_blank">Link</a></p>
        <p><strong>Rating:</strong> ${'★'.repeat(book.Rating)}${'☆'.repeat(5 - book.Rating)}</p>
        <h6>Review:</h6>
        <div>${book.Review}</div>
    `;

    modal.show();
}

function displayBooks() {
    const bookshelf = document.getElementById('bookshelf');
    bookshelf.innerHTML = ''; // Clear existing books
    books.forEach(book => {
        bookshelf.appendChild(createBookElement(book));
    });
}

document.addEventListener('DOMContentLoaded', loadBooks);