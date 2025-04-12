# Parent Input UI

A modern React-based web application for parents to record and track observations about their child's well-being. This application provides an intuitive interface for parents to document their observations and view historical entries.

## Features

- Modern, responsive user interface
- Real-time observation recording
- Historical observation viewing
- Date and time tracking
- Error handling and loading states

## Prerequisites

- Node.js (v14.0.0 or higher)
- npm (v6.0.0 or higher)
- Python backend server (see backend setup)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd parent-input
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## Project Structure

```
parent-input/
├── src/
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   ├── App.css
│   ├── index.tsx
│   └── index.css
├── package.json
└── README.md
```

## Backend Integration

This frontend application is designed to work with a Python backend server. The backend should provide the following API endpoints:

- `GET /api/observations` - Retrieve all observations
- `POST /api/observations` - Create a new observation

## Ian startup instructions???

```
cd parent_input
pip install -r requirements.txt
cd ..
python parent_input_ui.py
```

and also

```
cd parents_dashboard/parent-input
npm install
npm start
```

## Development

To start the development server:

```bash
npm start
```

The application will automatically reload when you make changes.

## Building for Production

To create a production build:

```bash
npm run build
```

This will create an optimized build in the `build` directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 