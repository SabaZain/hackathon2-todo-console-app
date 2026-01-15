# Next.js App Router Skill

This skill encapsulates knowledge of Next.js App Router and provides guidance for implementing modern Next.js applications using the app directory structure.

## Core Concepts

### File-Based Routing
Next.js App Router uses a file-based routing system where the file structure in the `app` directory determines the application's routes.

**Route Segments:**
- Each folder in the `app` directory represents a route segment
- Route segments are mapped to a specific URL based on their folder name
- Nested folders create nested routes (e.g., `/dashboard/settings`)

### Server Components by Default
- All components in the App Router are server components by default
- Server components render on the server and send HTML to the client
- They have direct access to backend resources and can eliminate unnecessary JavaScript
- Server components are the recommended default for better performance

### Client Components When Required
- Use the `"use client"` directive to define client components
- Client components run on the server during initial render, then hydrated on the client
- Use client components only when you need:
  - Event handlers (onClick, onChange, etc.)
  - State management (useState, useReducer, etc.)
  - Browser APIs (localStorage, geolocation, etc.)
  - Effects (useEffect, etc.)
  - Custom hooks that use client-side features

## Key Features

### Layouts
- Layout components wrap multiple pages and persist across route changes
- Created with the `layout.js` file in a route segment
- Can be nested by creating layout files in nested folders
- Must accept a `children` prop to render nested layouts and pages

### Pages
- Pages represent unique routes and are defined by the `page.js` file
- Each page is a server component by default
- Pages are always the leaf of a route segment

### Loading States
- Loading UI can be implemented with `loading.js` files
- Loading components are automatically wrapped with Suspense
- Provide better user experience during data fetching

### Error Handling
- Error boundaries can be implemented with `error.js` files
- Automatically wrap route segments in error boundaries
- Use `error` prop and `reset` function for error recovery

### Data Fetching Patterns

**Server-Side Data Fetching:**
- Fetch data directly in server components
- Data is fetched at build time or request time
- Can use `async`/`await` directly in components
- Caching strategies can be implemented with `fetch` options

**Streaming:**
- Combine Server Components with Suspense to stream UI updates
- Allows showing parts of the UI as they're ready
- Improves perceived performance

**Parallel Data Fetching:**
- Multiple server components can fetch data in parallel
- Each component fetches data independently
- No waterfall effect when components are nested

## Best Practices

1. **Server Components First**: Use server components by default and only add `"use client"` when necessary
2. **Route Segments**: Organize routes logically using folders and route groups
3. **Shared Layouts**: Use layout files to share UI across routes
4. **Loading States**: Implement loading.js files for better UX
5. **Error Boundaries**: Use error.js files for graceful error handling
6. **Data Fetching**: Fetch data in server components rather than client components when possible
7. **Code Splitting**: Leverage automatic code splitting by route segments

## File Structure Conventions

```
app/
├── layout.js          # Root layout
├── page.js            # Home page
├── loading.js         # Root loading UI
├── error.js           # Root error boundary
├── dashboard/
│   ├── layout.js      # Dashboard layout
│   ├── page.js        # Dashboard page
│   └── settings/
│       ├── page.js    # Settings page
│       └── loading.js # Settings loading UI
└── api/
    └── route.js       # API endpoints
```

## Integration with Frontend Agents

This skill is used by frontend agents to ensure:
- Correct implementation of Next.js App Router patterns
- Proper use of server vs client components
- Optimal data fetching strategies
- Modern Next.js architecture principles
- Consistent file structure and routing
- Performance optimization through server components
- Proper handling of loading and error states