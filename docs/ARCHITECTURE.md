# NAVADA System Architecture

## Overview
NAVADA is a job search and tracking platform designed to help users find and manage tech-artistic career opportunities. The system combines modern frontend technologies with a robust Supabase backend to provide a seamless job search experience.

## Core Components

### 1. User Management
- Profile management with tech and artistic preferences
- Document storage for CVs and portfolios
- Notification settings and preferences

### 2. Job Search Engine
- Tech-artistic scoring system
- Automated job discovery
- CV-based matching algorithm
- Manual application tracking

### 3. Database Schema

#### Profiles Table
- User information and preferences
- Tech and artistic preferences as JSONB
- Location preferences
- Notification settings

#### Jobs Table
- Job listings with tech and artistic scores
- Company information
- Salary ranges
- Requirements as JSONB

#### Applications Table
- Application status tracking
- Notes and updates
- Timeline of interactions

#### Documents Table
- CV and portfolio storage
- Document metadata
- Version tracking

### 4. Security
- Row Level Security (RLS) enabled on all tables
- User-specific policies for data access
- Secure document storage
- Authentication via Supabase

## Frontend Architecture

### Component Structure
- UI components using shadcn/ui
- Responsive dashboard layout
- Real-time updates via Supabase subscriptions
- Form handling with validation

### State Management
- React hooks for local state
- Supabase real-time subscriptions for remote state
- Form state via React Hook Form

## Backend Architecture

### Database Design
- PostgreSQL with Supabase extensions
- JSONB for flexible data storage
- Triggers for timestamp management
- Indexed search capabilities

### API Layer
- Supabase Client SDK
- Real-time subscriptions
- Row Level Security policies
- Storage bucket management

## Security Considerations
- All database access through RLS policies
- Authenticated API endpoints
- Secure document storage
- Environment variable management
