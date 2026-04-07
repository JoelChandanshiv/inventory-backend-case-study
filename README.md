# StockFlow Backend Case Study

This repository contains my solution for the StockFlow Backend Case Study.

Document Link: https://docs.google.com/document/d/1UgzjUm148FzmPGcTvDkxa2miIgS4keKrmugx29tuI88/edit?usp=sharing

## 📌 Overview

The case study is divided into three parts:

1. Code Review & Debugging
2. Database Design
3. API Implementation (Low Stock Alerts)

---

## 🛠 Tech Stack

- Python (Flask)
- SQL (PostgreSQL-style schema)
- SQLAlchemy (ORM assumptions)
- AWS concepts (deployment understanding)

---

## 📂 Project Structure

- `part1_debugging/` → Improved product creation API with fixes
- `part2_database/` → Database schema design (SQL DDL)
- `part3_api/` → Low stock alerts API implementation

---

## ⚙️ Key Highlights

- Ensured transaction safety and input validation in API design
- Designed a normalized and scalable database schema
- Implemented business rules like low stock alerts and recent sales filtering
- Considered real-world concerns like performance, scalability, and edge cases

---

## 🤔 Assumptions

- Low stock threshold is defined per product
- Recent sales activity is within the last 30 days
- A `sales` table exists for tracking product sales

---

## 🚀 Improvements (Future Scope)

- Optimize queries to avoid N+1 problem
- Add caching (Redis) for faster responses
- Move alert computation to background jobs
- Add pagination and rate limiting

---

## 👨‍💻 Author

Joel Chandanshiv
