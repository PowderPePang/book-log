# Book Log CRUD

## Tech Stack
- Backend: FastAPI (Python)
- Frontend: React
- Database: PostgreSQL (managed, free tier)
- Deployment: TBD by mentor (likely Render/Railway/Fly.io free tier)
- Auth: Session-based or JWT — to be decided in early session

## Scope

A web application where an authenticated user can:
1. Sign up with email + password
2. Log in (session persists across page refresh)
3. Log out
4. Add a book (title, author, optional rating 1-5, optional notes, 
   auto-recorded date)
5. View only their own books
6. Edit their own books
7. Delete their own books
8. Cannot see or modify other users' books

Out of scope: cover images, search, pagination, password reset, 
email verification, OAuth, dark mode, animations, mobile app, 
social features.

## Non-functional requirements
- Deployed to public HTTPS URL (free tier)
- Passwords hashed (never plaintext)
- Data persists across deployments (managed PostgreSQL, not SQLite)
- Code in public GitHub repository with README
- Hour-tracking spreadsheet maintained by me