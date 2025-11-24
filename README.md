# VirtualCoworking

A fully production-ready, scalable, secure, enterprise-grade SaaS platform for virtual co-working spaces.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Development Setup](#development-setup)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Overview

VirtualCoworking is a comprehensive platform that enables remote teams to collaborate effectively through virtual co-working spaces. It provides tools for team management, real-time communication, task tracking, focus sessions, and productivity analytics.

## Features

### User & Authentication
- User registration with email verification
- JWT-based authentication with refresh token rotation
- Role-based access control (Owner, Admin, Member)
- User profiles with avatar, bio, timezone, and company information

### Team Management
- Team creation and management
- Role-based permissions
- Member invitation system
- Team analytics and productivity metrics

### Real-Time Communication
- WebSocket-based chat rooms per team
- Typing indicators
- Read receipts
- Online/offline presence status

### Task Management (Kanban)
- Boards, columns, and task organization
- Task priorities, labels, and assignees
- Due dates and reminders
- Subtasks and comments
- File attachments with S3 storage

### Focus Timer
- Pomodoro-style focus sessions
- Custom and deep work sessions
- Session tracking and statistics
- Daily and weekly focus goals

### Calendar & Scheduling
- Team and personal event management
- Meeting scheduling
- Reminders and notifications
- Google Calendar integration

### Video Conferencing
- WebRTC-based video calls
- Meeting room management
- Participant tracking
- Recording capabilities

### Analytics & Reporting
- Team productivity dashboards
- Task completion rates
- Focus metrics and heatmaps
- Work-hour analytics

### Notifications
- Real-time in-app notifications
- Email notifications
- Notification preferences

### File Sharing
- Secure file upload and storage
- Team and personal file organization
- File versioning
- Access controls

### Integrations
- Google Workspace integration
- Slack integration
- GitHub/Notion integration (planned)

## Architecture

```
┌─────────────────┐    ┌──────────────────┐
│   Frontend      │    │   Load Balancer  │
│   (Next.js)     │◄──►│   (Nginx)        │
└─────────────────┘    └──────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Backend       │    │   PostgreSQL     │    │   Redis         │
│   (Django)      │◄──►│   (Database)     │    │   (Cache/WS)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                       │                       │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Celery        │    │   S3 Storage     │    │   SMTP Server   │
│   (Workers)     │    │   (Files)        │    │   (Email)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Backend Architecture
- **Django Monolith** with modular apps
- **PostgreSQL** for primary data storage
- **Redis** for caching, WebSocket layers, and rate limiting
- **Celery** with Redis for asynchronous task processing
- **JWT** for stateless authentication
- **Django Channels** for WebSocket communication
- **AWS S3** for file storage

### Frontend Architecture
- **Next.js 14** with App Router
- **TypeScript** for type safety
- **React Query** for server state management
- **Zustand** for client state management
- **TailwindCSS** with shadcn/ui for styling
- **WebSockets** for real-time features

## Tech Stack

### Backend
- Python 3.12
- Django 5.2
- Django REST Framework
- Django Channels
- PostgreSQL
- Redis
- Celery
- JWT Authentication
- AWS S3

### Frontend
- Next.js 14
- TypeScript
- React Query
- Zustand
- TailwindCSS
- shadcn/ui
- WebSockets

### Infrastructure
- Docker & Docker Compose
- Nginx (Reverse Proxy)
- Let's Encrypt (SSL)
- GitHub Actions (CI/CD)

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL (for local development)
- Redis (for local development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/virtualcoworking.git
   cd virtualcoworking
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

### Development Setup

1. Start the backend services:
   ```bash
   # In backend directory
   python manage.py runserver
   ```

2. Start the frontend:
   ```bash
   # In frontend directory
   npm run dev
   ```

3. For full development environment with Docker:
   ```bash
   cd infrastructure
   docker-compose up -d
   ```

## API Documentation

API documentation is available through Swagger/OpenAPI:

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

See [API Specification](docs/api-spec.yaml) for detailed API documentation.

## Deployment

See [Deployment Instructions](docs/deployment-instructions.md) for detailed deployment guidelines.

### Quick Deployment with Docker

```bash
cd infrastructure
docker-compose up -d
```

## Testing

### Backend Tests

```bash
cd backend
python manage.py test
```

### Frontend Tests

```bash
cd frontend
npm run test
```

### Load Testing

```bash
# Install k6
# Run load tests
k6 run tests/load-testing.js
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**VirtualCoworking** - Bringing remote teams together, one virtual workspace at a time.