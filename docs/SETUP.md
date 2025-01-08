# NAVADA Development Setup

## Prerequisites
- Node.js (Latest LTS version)
- npm (Included with Node.js)
- Git

## Environment Setup

1. Clone the repository:
```bash
gh repo clone leeakpareva/NAvadaOpportunities
cd NAvadaOpportunities
```

2. Install dependencies:
```bash
npm install
```

3. Create a .env file:
```
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

4. Start the development server:
```bash
npm run dev
```

## Database Setup

1. Install Supabase CLI
2. Run migrations:
```bash
cd supabase
supabase migration up
```

## Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run lint`: Run ESLint
- `npm run preview`: Preview production build

## Code Style

- Follow TypeScript best practices
- Use ESLint for code linting
- Follow shadcn/ui component patterns
- Use Tailwind CSS for styling

## Git Workflow

1. Create feature branch
2. Make changes
3. Run linting
4. Create pull request
5. Wait for review
