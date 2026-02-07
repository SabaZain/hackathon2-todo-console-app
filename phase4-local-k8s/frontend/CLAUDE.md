# frontend Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-12

## Active Technologies

- Next.js 16+
- TypeScript
- Tailwind CSS
- React Server Components (App Router)

## Project Structure

```text
frontend/
├── app/              # Pages & layouts (Next.js App Router)
├── components/       # Reusable UI components
├── lib/              # API clients and helpers
├── public/           # Static assets
├── styles/           # Tailwind CSS and global styles
├── types/            # TypeScript type definitions
└── package.json      # Dependencies and scripts
```

## Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linting
- `npm run format` - Run code formatting

## Code Style

- Use TypeScript for all components
- Follow Next.js App Router conventions
- Use Tailwind CSS for styling (no inline styles)
- Component names should be PascalCase
- File names should be kebab-case
- Use functional components with TypeScript interfaces
- Follow accessibility best practices (aria labels, semantic HTML)

## Recent Changes

- Initial setup with Next.js 16+ and TypeScript
- Tailwind CSS configuration
- Basic component structure
- API client stubs for backend integration
- Enhanced UI with professional gradient background
- Improved responsive design with mobile-first approach
- Modern card-based UI with shadows, rounded corners, and hover effects
- Consistent Navbar and Footer placement across all pages
- Enhanced styling for buttons, inputs, and task items
- Added animations and transitions for better user experience
- Improved accessibility and visual hierarchy
- Widened Navbar with increased horizontal padding for professional look
- Attractive gradient background on welcome page with semi-transparent content card
- Modern slate/gray background on welcome page card for contemporary design
- Updated welcome page card to dark background with light text for high contrast
- Added Logout functionality with authentication token clearing and proper routing