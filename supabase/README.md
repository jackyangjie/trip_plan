# Supabase Development Environment

## Setup

```bash
# Initialize Supabase
npx supabase init

# Start local Supabase
npx supabase start

# Stop local Supabase
npx supabase stop
```

## Access

- Studio: http://localhost:54323
- API: http://localhost:54321
- Database: postgresql://postgres:postgres@localhost:54322/postgres

## Migrations

```bash
# Create new migration
npx supabase db diff -f new_migration.sql

# Apply migrations
npx supabase db push

# Reset database
npx supabase db reset
```
