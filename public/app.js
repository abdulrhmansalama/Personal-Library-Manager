document.addEventListener('DOMContentLoaded', () => {
    const bookForm = document.getElementById('bookForm');
    const booksContainer = document.getElementById('booksContainer');

    // تحميل الكتب عند فتح الصفحة
    fetchBooks();

    // إضافة كتاب جديد
    bookForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const newBook = {
            title: document.getElementById('title').value,
            author: document.getElementById('author').value,
            genre: document.getElementById('genre').value,
            publication_year: document.getElementById('year').value
        };

        await addBook(newBook);
        bookForm.reset();
        fetchBooks();
    });

    // وظيفة جلب الكتب
    async function fetchBooks() {
        try {
            const response = await fetch('/api/books');
            const books = await response.json();
            displayBooks(books);
        } catch (error) {
            console.error('Error fetching books:', error);
        }
    }

    // وظيفة إضافة كتاب
    async function addBook(book) {
        try {
            await fetch('/api/books', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(book),
            });
        } catch (error) {
            console.error('Error adding book:', error);
        }
    }

    // وظيفة عرض الكتب
    function displayBooks(books) {
        booksContainer.innerHTML = '';
        
        if (books.length === 0) {
            booksContainer.innerHTML = '<p>لا توجد كتب في المكتبة بعد.</p>';
            return;
        }

        books.forEach(book => {
            const bookElement = document.createElement('div');
            bookElement.className = 'book-card';
            bookElement.innerHTML = `
                <h3>${book.title}</h3>
                <p><strong>المؤلف:</strong> ${book.author}</p>
                <p><strong>النوع:</strong> ${book.genre}</p>
                <p><strong>سنة النشر:</strong> ${book.publication_year}</p>
                <button onclick="deleteBook('${book.title}')">حذف</button>
            `;
            booksContainer.appendChild(bookElement);
        });
    }

    // وظيفة حذف كتاب
    window.deleteBook = async function(title) {
        try {
            await fetch(`/api/books/${encodeURIComponent(title)}`, {
                method: 'DELETE'
            });
            fetchBooks();
        } catch (error) {
            console.error('Error deleting book:', error);
        }
    };
});
