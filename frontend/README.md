# Code Reviewer Frontend

A modern React-based frontend application for code review functionality, built with a focus on clean architecture and user experience.

## Tech Stack

### Core Framework

- **React 19** - Modern React with latest features
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and development server

### UI & Styling

- **Tailwind CSS 4** - Utility-first CSS framework
- **shadcn/ui** - High-quality, accessible UI components built on Radix UI
- **Lucide React** - Beautiful & consistent icon toolkit

### State Management & Data Fetching

- **TanStack Query (React Query)** - Powerful data synchronization for React
- **Zustand** - Lightweight state management with persistence
- **Zod** - TypeScript-first schema validation



### Installation

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
# or
pnpm install
```

### Development

Start the development server:

```bash
npm run dev
# or
pnpm dev
```

The application will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
# or
pnpm build
```

### Preview Production Build

```bash
npm run preview
# or
pnpm preview
```

## Deployment

### GitHub Pages

The application is configured for deployment on GitHub Pages with automatic CI/CD:

- **Automatic deployment**: Pushes to the `main` branch trigger automatic deployment
- **GitHub Actions workflow**: Located in `.github/workflows/front_deploy.yml`
- **Production URL**: https://GenaroVogelius.github.io/analyzer
