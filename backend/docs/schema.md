Table: users
Columns:
 - id           : int, primary key, not null, auto-increment, unique
 - email        : text, not null, unique
 - password_hash: text, not null
 - created_at    : timestampz, not null, default: now
Constraints:


Table: books
Columns:
 - id           : int, primary key, not null, auto-increment, unique
 - user_id      : int, foreign key, not null
 - title        : text, not null
 - author       : text, not null
 - rating       : int, nullable, check (rating between 1 and 5)
 - note         : text, nullable
 - created_at    : timestampz, not null, default: now
Constraints:
 - Foreign key  : user_id references users(id) ON DELETE CASCADE

Note that:
 - I chose not to use `UUID` because it typically meant for global items in distributed database or high-security environment. Generating, indexing, and processing UUIDs takes more time, and those characteristics are not necessary for this book log database. Security is not a concern even if someone guesses the user and book id. Instead, sequential ID allows faster processing and easier management.
 - `TIMESTAMPZ` is used instead of `TIMESTAMP` to ensure the time is converted into UTC regardless of the user's timezone.
 - The reason I use `ON DELETE CASCADE` is that when a user is deleted, it automatically deletes all their books as well.
 - The "Rating between 1 and 5" rule is enforced by `CHECK` constraint. This enforcement should be applied to both the database layer and the application layer