# Quickstart Guide: Phase II Frontend Development

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Claude CLI installed and configured

## Setup Instructions

### 1. Initialize the Project
```bash
cd fullstackwebapp
mkdir frontend
cd frontend
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

### 2. Install Additional Dependencies
```bash
npm install @types/react-modal react-modal
```

### 3. Project Structure
After setup, your project should have the following structure:
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── signin/
│   │   └── signup/
│   ├── dashboard/
│   ├── globals.css
│   └── layout.tsx
├── components/
│   ├── ui/
│   │   ├── Input.tsx
│   │   ├── Button.tsx
│   │   └── TaskModal.tsx
│   ├── Navbar.tsx
│   └── Footer.tsx
├── lib/
│   └── api-stubs.ts
└── src/
    └── app/
```

### 4. Environment Configuration
Create a `.env.local` file in the frontend directory:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:3000
```

## Development Workflow

### Create Components
Use Claude CLI to generate components:
```bash
# Generate reusable components
claude generate component Input
claude generate component Button
claude generate component TaskModal
```

### Create Pages
Use Claude CLI to generate pages:
```bash
# Generate auth pages
claude generate page signin
claude generate page signup

# Generate dashboard
claude generate page dashboard
```

### Run the Application
```bash
npm run dev
```

Visit http://localhost:3000 to see your application.

## API Integration
All API calls should use the stub implementations defined in the API contract. The frontend assumes JWT-based authentication but does not implement the actual authentication logic.

## Styling Guidelines
- Use Tailwind CSS classes exclusively
- Follow the design system defined in frontend/CLAUDE.md
- Maintain consistent spacing, typography, and color palette
- Ensure responsive design for mobile, tablet, and desktop

## Testing
Verify components meet the acceptance criteria defined in the specification:
- All components render correctly
- Responsive layout works on all screen sizes
- Validation messages appear for invalid input
- Buttons are interactive
- API stubs exist for backend calls