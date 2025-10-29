# Portfolio Analyzer

A modern web application for analyzing trading portfolio operations. Users can upload CSV files containing trading operations, and the application processes them to display all operations made and a detailed table of closed positions.

- **Front-end Production URL**: http://analyzer-front-simv.site
- **Backend Production URL**: https://analyzer.simv.site

You can go to the frontend page, type anything and log in, authentication was not implemented, then upload the csv file of the dataset and search from year-date 2023.

## Architecture

### Backend

The backend is built with **FastAPI** using **clean architecture** principles, ensuring separation of concerns, testability, and maintainability. The architecture separates:

- **Domain Layer**: Core business entities and use cases
- **Infrastructure Layer**: External concerns like database, API routes, parsers, and analyzers
- **Interfaces**: Contracts between layers for dependency inversion

The backend uses:

- PostgreSQL database for data persistence
- Tortoise ORM with Aerich for database migrations

### Frontend

The frontend is built with **React** and modern web technologies:

#### Core Framework

- **React 19** - Modern React with latest features
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and development server

#### UI & Styling

- **Tailwind CSS 4** - Utility-first CSS framework
- **shadcn/ui** - High-quality, accessible UI components built on Radix UI
- **Lucide React** - Beautiful & consistent icon toolkit

#### State Management & Data Fetching

- **TanStack Query (React Query)** - Powerful data synchronization for React
- **Zustand** - Lightweight state management with persistence

## Features

- **CSV Upload**: Upload trading operations in CSV format
- **Operations Dashboard**: View all operations made in your portfolio
- **Closed Positions Table**: Analyze closed positions with detailed information about matched buy/sell operations

## Running Locally

This application consists of two components that need to be running simultaneously:

- **Backend API**: FastAPI server typically runs on `http://localhost:8000`
- **Frontend**: React development server typically runs on `http://localhost:5173`

### Prerequisites

- **Docker** and **Docker Compose** (for backend quick start)
- **Node.js** and **npm** or **pnpm** (for frontend)
- **Python 3.11+** (if running backend without Docker)

### Quick Start

1. **Start the Backend**:

   Navigate to the backend directory and start with Docker Compose:

   ```bash
   cd backend
   docker-compose -f .devcontainer/docker-compose.local.yml up -d --no-recreate
   ```

   or

   ```bash
   cd backend
   control + shift + p --> rebuild in container
   ```

   This will start:

   - PostgreSQL database on port `5432`
   - FastAPI backend application on `http://localhost:8000` (with hot reload enabled)

   The backend will automatically run database migrations on startup.

2. **Start the Frontend**:

   Navigate to the frontend directory and install dependencies:

   ```bash
   cd frontend
   npm install  # or pnpm install
   ```

   Start the development server:

   ```bash
   npm run dev  # or pnpm dev
   ```

   The frontend will be available at `http://localhost:5173`

### Production

- **Automatic deployment**: Pushes to the `main` branch trigger automatic deployment

### Dataset

A sample historical portfolio dataset is available at `dataset/historical_portfolio.csv`.
