document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('search-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const q = document.getElementById('query').value;
        if (!q) return;

        // read method and sort from UI
        const method = document.getElementById('method') ? document.getElementById('method').value : 'binary';
        const sort = document.getElementById('sort') ? document.getElementById('sort').value : 'title';

        // show spinner
        const spinner = document.getElementById('spinner');
        if (spinner) spinner.style.display = 'block';

        // Prefer JSON API for partial updates
        fetch(`/api/search?query=${encodeURIComponent(q)}&method=${encodeURIComponent(method)}&sort=${encodeURIComponent(sort)}`)
            .then(resp => resp.json())
            .then(data => {
                const container = document.getElementById('results-placeholder');
                container.innerHTML = '';
                if (!data.books || data.books.length === 0) {
                    container.innerHTML = '<p>No results found.</p>';
                    return;
                }
                // Render results as cards to match server HTML
                const grid = document.createElement('div');
                grid.className = 'results-grid';
                data.books.forEach(b => {
                    const card = document.createElement('article');
                    card.className = 'book-card';
                    const header = document.createElement('div');
                    header.className = 'book-card-header';
                    header.textContent = b.title;
                    const body = document.createElement('div');
                    body.className = 'book-card-body';
                    body.innerHTML = `\n                        <p><strong>Author:</strong> ${escapeHtml(b.author)}</p>\n                        <p><strong>Book ID:</strong> ${b.book_id}</p>\n                        <p><strong>Source:</strong> ${escapeHtml(b.source || 'Database')}</p>`;
                    card.appendChild(header);
                    card.appendChild(body);
                    grid.appendChild(card);
                });
                container.appendChild(grid);
            })
            .catch(err => {
                console.error('Search request failed', err);
            })
            .finally(() => {
                if (spinner) spinner.style.display = 'none';
            });
    });

    function escapeHtml(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }
});
