# NAVADA Job Finder System

A sophisticated job search and tracking platform designed to help users find and manage tech-artistic career opportunities.

## Project Structure
- `/frontend` - React + TypeScript frontend with Supabase integration
- `/backend` - Python-based CV parsing and job matching system
- `/docs` - Project documentation and technical specifications

## Quick Start

### Backend Setup
```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Documentation
- [Setup Guide](docs/SETUP.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [Tech Stack Details](docs/TECH_STACK.md)

## Features
- CV-based job matching
- Tech-artistic scoring system
- Manual application tracking
- Document management
- Real-time notifications

