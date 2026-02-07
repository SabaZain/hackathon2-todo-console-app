# Todo App Frontend

This is the frontend for the Todo App built with Next.js 16+, TypeScript, and Tailwind CSS.

## Features

- User authentication (Sign In/Sign Up)
- Task management (Create, Read, Update, Delete)
- Task status tracking (Pending, In Progress, Completed)
- Responsive design
- Clean, modern UI

## Tech Stack

- Next.js 16+ with App Router
- TypeScript
- Tailwind CSS
- React Server Components

## Getting Started

First, install the dependencies:

```bash
npm install
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linting
- `npm run format` - Run code formatting

## Project Structure

```
frontend/
├── app/              # Pages & layouts (Next.js App Router)
├── components/       # Reusable UI components
├── lib/              # API clients and helpers
├── public/           # Static assets
├── styles/           # Tailwind CSS and global styles
├── types/            # TypeScript type definitions
└── package.json      # Dependencies and scripts
```

## API Integration

The frontend connects to API endpoints through the stub implementations in `lib/api.ts`. These simulate backend functionality for demonstration purposes.

## Styling

We use Tailwind CSS for styling. The global styles are in `styles/globals.css` which imports Tailwind directives.

## Components

Reusable components are organized in the `components/` directory:

- `components/ui/` - Basic UI elements (Input, Button)
- `components/layout/` - Layout components (Navbar, Footer)
- `components/task/` - Task-specific components (TaskItem, TaskModal)