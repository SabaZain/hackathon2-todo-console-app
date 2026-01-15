# Data Model: Phase II Frontend

## Task Entity
- **id**: string (unique identifier)
- **title**: string (required, max 255 characters)
- **description**: string (optional, max 1000 characters)
- **status**: string (enum: 'pending', 'completed', 'in-progress')
- **createdDate**: Date (timestamp when task was created)
- **validationRules**:
  - title is required
  - title length between 1-255 characters
  - description length maximum 1000 characters

## User Entity
- **id**: string (unique identifier)
- **name**: string (required, max 100 characters)
- **email**: string (required, valid email format)
- **password**: string (required, min 8 characters with strength requirements)
- **validationRules**:
  - name is required and 1-100 characters
  - email is required and valid email format
  - password is required and minimum 8 characters
  - password meets strength requirements (uppercase, lowercase, number, special character)

## Component Prop Types

### Input Component
- **label**: string (optional)
- **placeholder**: string (optional)
- **type**: string (default: 'text', options: 'text', 'email', 'password', 'textarea')
- **value**: string (controlled component)
- **onChange**: function (event handler)

### Button Component
- **label**: string (required)
- **onClick**: function (event handler)
- **type**: string (default: 'primary', options: 'primary', 'secondary')

### Task Modal Props
- **isOpen**: boolean (controls modal visibility)
- **onClose**: function (callback to close modal)
- **onSave**: function (callback to save task)
- **taskData**: object (existing task data for editing)
- **initialFocusRef**: ref (element to focus when modal opens)