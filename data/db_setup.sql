CREATE TABLE IF NOT EXISTS tasks(
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority INT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATE DEFAULT CURRENT_DATE,
    due_date DATE
)