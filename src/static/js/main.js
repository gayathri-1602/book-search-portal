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
                    
                    // Book cover
                    if (b.cover_url) {
                        const coverDiv = document.createElement('div');
                        coverDiv.className = 'book-cover';
                        const img = document.createElement('img');
                        img.src = b.cover_url;
                        img.alt = `Cover of ${escapeHtml(b.title)}`;
                        img.onerror = function() { this.src = 'https://via.placeholder.com/180x270?text=No+Cover'; };
                        coverDiv.appendChild(img);
                        card.appendChild(coverDiv);
                    }
                    
                    // Book header
                    const header = document.createElement('div');
                    header.className = 'book-card-header';
                    header.textContent = b.title;
                    card.appendChild(header);
                    
                    // Book body
                    const body = document.createElement('div');
                    body.className = 'book-card-body';
                    
                    // Author
                    const authorP = document.createElement('p');
                    authorP.innerHTML = `<strong>Author:</strong> <span style="font-size: 1.1rem; color: var(--primary-color); font-weight: 600;">${escapeHtml(b.author)}</span>`;
                    body.appendChild(authorP);
                    
                    // Meta grid
                    const metaGrid = document.createElement('div');
                    metaGrid.className = 'book-meta-grid';
                    
                    if (b.genre) {
                        const genreDiv = document.createElement('div');
                        genreDiv.innerHTML = `<strong>Genre:</strong> <span class="book-detail-badge badge-genre">${escapeHtml(b.genre)}</span>`;
                        metaGrid.appendChild(genreDiv);
                    }
                    
                    if (b.publication_year) {
                        const yearDiv = document.createElement('div');
                        yearDiv.innerHTML = `<strong>Published:</strong> <span class="book-detail-badge badge-year">${b.publication_year}</span>`;
                        metaGrid.appendChild(yearDiv);
                    }
                    
                    if (b.language) {
                        const langDiv = document.createElement('div');
                        langDiv.innerHTML = `<strong>Language:</strong> <span class="book-detail-badge badge-language">${escapeHtml(b.language)}</span>`;
                        metaGrid.appendChild(langDiv);
                    }
                    
                    if (b.page_count) {
                        const pagesDiv = document.createElement('div');
                        pagesDiv.innerHTML = `<strong>Pages:</strong> ${b.page_count} pages`;
                        metaGrid.appendChild(pagesDiv);
                    }
                    
                    if (metaGrid.children.length > 0) {
                        body.appendChild(metaGrid);
                    }
                    
                    // Additional details
                    const detailsDiv = document.createElement('div');
                    detailsDiv.style.marginTop = '10px';
                    
                    if (b.isbn) {
                        const isbnP = document.createElement('p');
                        isbnP.innerHTML = `<strong>ISBN:</strong> <code style="background: #f0f0f0; padding: 2px 6px; border-radius: 4px;">${escapeHtml(b.isbn)}</code>`;
                        detailsDiv.appendChild(isbnP);
                    }
                    
                    if (b.publisher) {
                        const pubP = document.createElement('p');
                        pubP.innerHTML = `<strong>Publisher:</strong> ${escapeHtml(b.publisher)}`;
                        detailsDiv.appendChild(pubP);
                    }
                    
                    const bookIdP = document.createElement('p');
                    bookIdP.innerHTML = `<strong>Book ID:</strong> #${b.book_id}`;
                    detailsDiv.appendChild(bookIdP);
                    
                    body.appendChild(detailsDiv);
                    
                    // Description
                    if (b.description) {
                        const descDiv = document.createElement('div');
                        descDiv.className = 'book-description';
                        descDiv.innerHTML = `<strong style="display: block; margin-bottom: 8px; color: var(--primary-color);">📖 Description:</strong>${escapeHtml(b.description)}`;
                        body.appendChild(descDiv);
                    }
                    
                    // Source
                    const sourceP = document.createElement('p');
                    sourceP.style.marginTop = '10px';
                    sourceP.style.fontSize = '0.85rem';
                    sourceP.style.color = 'var(--text-secondary)';
                    sourceP.innerHTML = `<strong>Source:</strong> ${escapeHtml(b.source || 'Database')}`;
                    body.appendChild(sourceP);
                    
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
