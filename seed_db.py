from src.models.db import init_db, get_session, Book as DBBook
from seed_data import BOOKS


def seed():
    """Initialize DB and upsert the books defined in seed_data.BOOKS."""
    init_db()
    session = get_session()

    try:
        # Existing book_ids in DB
        existing_ids = {row[0] for row in session.query(DBBook.book_id).all()}

        to_add = []
        updated = 0
        for data in BOOKS:
            bid = data.get('book_id')
            # Prevent unique-ISBN conflicts: if another record already has this ISBN, avoid overwriting
            isbn_val = data.get('isbn')
            if isbn_val:
                conflict = session.query(DBBook).filter(DBBook.isbn == isbn_val, DBBook.book_id != bid).first()
                if conflict:
                    # clear isbn in incoming data to avoid UNIQUE constraint failure
                    data['isbn'] = None

            if bid in existing_ids:
                # update existing
                obj = session.query(DBBook).filter_by(book_id=bid).first()
                if obj:
                    for k, v in data.items():
                        setattr(obj, k, v)
                    session.add(obj)
                    updated += 1
            else:
                to_add.append(DBBook(**data))

        if to_add:
            session.add_all(to_add)

        session.commit()
        print(f"Inserted {len(to_add)} new books, updated {updated} existing books.")
    finally:
        session.close()


if __name__ == '__main__':
    seed()
