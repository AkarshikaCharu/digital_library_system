# digital_library_system
A high-performance, Role-Based Access Control (RBAC) web application built with Streamlit and SQLite. This system is designed to provide a seamless digital interface for managing library inventories with a focus on security and user experience.


Key Features
Dynamic UI Rendering: Unique dashboards for Faculty (Admin Tools & Analytics) and Students (Catalog & Borrowing).
Secure Authentication: User passwords protected using SHA-256 Hashing.
Smart Inventory: Pre-seeded with 50+ technical titles and real-world ISBN-13 data.
Live Search: Instant filtering by Title, Author, or ISBN for high-speed navigation.
Responsive Design: Customized Lavender & Black High-Contrast UI for a professional enterprise feel.
Data Integrity: Implemented Regex Validation for academic identifiers (Roll Numbers).

Tech Stack
Frontend: Streamlit (Python-based Web Framework)
Backend: Python 3.x
Database: SQLite3 (Relational Database)
Styling: Custom CSS Injection for Enterprise UI/UX

Project Structure
app.py: Main entry point, UI Layout, and Analytics Dashboard.
login.py: Authentication logic and Role-Based view handling.
database_manager.py: SQL Schema management and Automated Data Seeding.
requirements.txt: Environment dependencies.
