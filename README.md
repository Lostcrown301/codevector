# Product Catalog API

A backend service built using FastAPI and PostgreSQL that manages a large product catalog and provides efficient product listing with category filtering and cursor-based pagination.

## Features

- Store and manage 200,000+ products
- Category-based filtering
- Cursor-based pagination
- Stable pagination under concurrent inserts
- Bulk data seeding
- PostgreSQL indexing for query performance
- FastAPI REST API

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL (Supabase)
- Faker

---

## Database Schema

### Product

Field| Type
id| String (UUID)
name| String
category| String
price| Float
created_at| DateTime
updated_at| DateTime

---
## Project Structure
```
.
├── app.py
├── database.py
├── models.py
├── seed.py
├── create_indexes.py
├── .env.example
├── assignment_check.py
├── check.txt
├── .gitignore
├── requirements.txt
└── README.md
```
---

## Setup

1. ``` Install Dependencies
   pip install -r requirements.txt ```

2. Configure Environment Variables

3. ``` Create a ".env" file:
   DATABASE_URL=your_supabase_postgres_connection_string ```

4. ``` Run API
   uvicorn app:app --reload
   Server runs on:
   http://127.0.0.1:8000 ```

---

## Seeding Data

The seed script generates 200,000 products and inserts them in batches of 5,000 records.

Run:

``` python seed.py ```
### Features:

- UUID based identifiers
- Random categories
- Random prices
- Random timestamps
- Batch insertion for improved performance

---

## API Endpoints

Get Products

GET /products

### Query Parameters

Parameter| Description
limit| Number of products to return
category| Filter by category
cursor_created_at| Cursor timestamp
cursor_id| Cursor product id

Example

GET /products?limit=20

Filter by category:

GET /products?limit=20&category=Electronics

Fetch next page:

GET /products?limit=20&cursor_created_at=2026-06-23T11:14:21.536879&cursor_id=340b183c-d68e-4088-b60a-e1302cbc659d

---

## Pagination Strategy

### Why Not Offset Pagination?

Offset pagination:

``` LIMIT 20 OFFSET 20 ```
can produce duplicate or missing products when new products are inserted while users browse.

Example:

1. User views page 1.
2. New products are inserted.
3. User requests page 2.
4. Records shift due to new inserts.
5. Duplicate or skipped products may occur.

---

## Cursor Pagination

Products are sorted by:

ORDER BY created_at DESC, id DESC

The last product from the current page generates a cursor:

``` {
  "created_at": "2026-06-23T11:14:21.536879",
  "id": "340b183c-d68e-4088-b60a-e1302cbc659d"
}
```
Subsequent requests fetch products older than the cursor.

### Benefits:

- No duplicate records
- No skipped records
- Consistent pagination
- Efficient for large datasets

---

## Indexing Strategy

Feed Index

(created_at DESC, id DESC)

Used for:

- Product listing
- Cursor pagination

Category Feed Index

(category, created_at DESC, id DESC)

Used for:

- Category filtering
- Cursor pagination

These indexes match the query patterns used by the API and reduce scanning and sorting overhead.

---

## Concurrent Insert Test

The assignment required ensuring users do not see duplicate or missing products while browsing if new products are added.

Test performed:

1. Retrieved page 1 and saved the cursor.
2. Inserted 50 new products.
3. Retrieved page 2 using the saved cursor.
4. Compared product IDs across both pages.

Result

- No duplicate products
- No skipped products
- Newly inserted products did not affect pagination consistency

This confirms that the cursor-based pagination implementation satisfies the assignment requirement.
