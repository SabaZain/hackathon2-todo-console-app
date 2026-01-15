# Fix for missing globals.css import in layout.tsx

## Date
2026-01-12

## Issue
The layout.tsx file was trying to import globals.css from './globals.css' but the file actually exists in '@/styles/globals.css'

## Solution
Updated the import in frontend/app/layout.tsx from:
```javascript
import './globals.css'
```
to:
```javascript
import '@/styles/globals.css'
```

## Files Modified
- frontend/app/layout.tsx: Updated import path to correctly reference the globals.css file in the styles directory

## Verification
The globals.css file in frontend/styles/ already contained the required Tailwind directives:
- @tailwind base;
- @tailwind components;
- @tailwind utilities;

After this fix, the Next.js application should build successfully without 'Module not found' errors for globals.css.