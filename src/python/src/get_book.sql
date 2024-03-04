### HOW TO USE IN TERMINAL
# Get-Content "<path to this script>" | mysql -u <username> -p <db_name>



SELECT
    b.book_id,
    b.book_url,
    b.title AS book_title,
    GROUP_CONCAT(DISTINCT c.category SEPARATOR ', ') AS categories,
    GROUP_CONCAT(DISTINCT ba.author_name SEPARATOR ', ') AS authors,
    b.description AS book_description,
    b.publication_date AS book_published_date,
    b.publisher AS book_publisher,
    b.epub_isbn AS book_isbn_13,
    b.paper_isbn AS book_isbn_10,
    b.language AS book_language,
    b.page_count,
    b.format_ebook AS book_format,
    b.ebook_size AS book_file_size,
    b.protection AS book_protection,
    b.price AS book_price,
    b.currency,
    b.image_link AS book_cover_url
FROM
    books b
LEFT JOIN
    books_category bc ON b.book_id = bc.book_id
LEFT JOIN
    categories c ON bc.category = c.category
LEFT JOIN
    books_author ba ON b.book_id = ba.book_id
GROUP BY
    b.book_id;
