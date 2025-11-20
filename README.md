# Virtual Co-working Space

A minimal viable SaaS web application for remote teams to collaborate, communicate, and stay productive.

## Tech Stack

### Backend
- Python + Django + Django Channels (WebSockets for real-time features)
- PostgreSQL (free-tier) or SQLite
- Django REST Framework for API
- Django Channels for real-time chat

### Frontend
- React + Next.js
- Tailwind CSS for styling
- TypeScript

### Features
1. Team creation & role management
2. Real-time chat & small group video calls (MVP: text chat first)
3. Task tracking & Kanban boards
4. Focus timer (Pomodoro-style)
5. Analytics: basic team and individual productivity dashboard
6. File sharing & notes

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (if not already created):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend/virtual-coworking
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Project Structure

```
virtualcoworking/
├── backend/           # Django backend application
│   ├── accounts/      # User authentication and profiles
│   ├── analytics/     # Productivity analytics
│   ├── chat/          # Real-time chat functionality
│   ├── files/         # File sharing and notes
│   ├── tasks/         # Task management and Kanban boards
│   ├── teams/         # Team creation and management
│   ├── timer/         # Pomodoro-style focus timer
│   ├── virtualcoworking/  # Main Django project settings
│   ├── manage.py      # Django management script
│   ├── requirements.txt   # Python dependencies
│   └── venv/          # Python virtual environment
└── frontend/          # Next.js frontend application
    └── virtual-coworking/
        ├── src/
        │   ├── app/     # Next.js app directory
        │   └── components/ # Reusable React components
        ├── public/      # Static assets
        └── package.json # Node.js dependencies
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/current-user/` - Get current user info
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update user profile

### Teams
- `GET /api/teams/` - List user's teams
- `POST /api/teams/create/` - Create a new team
- `GET /api/teams/<team_id>/` - Get team details
- `PUT /api/teams/<team_id>/update/` - Update team
- `DELETE /api/teams/<team_id>/delete/` - Delete team
- `GET /api/teams/<team_id>/members/` - List team members
- `POST /api/teams/<team_id>/members/add/` - Add member to team
- `DELETE /api/teams/<team_id>/members/<user_id>/remove/` - Remove member from team
- `PUT /api/teams/<team_id>/members/<user_id>/role/` - Update member role

### Tasks
- `GET /api/tasks/boards/` - List user's task boards
- `POST /api/tasks/boards/create/` - Create a new task board
- `GET /api/tasks/boards/<board_id>/` - Get board details
- `PUT /api/tasks/boards/<board_id>/update/` - Update board
- `DELETE /api/tasks/boards/<board_id>/delete/` - Delete board
- `GET /api/tasks/columns/<column_id>/tasks/` - List tasks in a column
- `GET /api/tasks/` - List user's tasks
- `POST /api/tasks/create/` - Create a new task
- `GET /api/tasks/<task_id>/` - Get task details
- `PUT /api/tasks/<task_id>/update/` - Update task
- `DELETE /api/tasks/<task_id>/delete/` - Delete task
- `PUT /api/tasks/<task_id>/move/` - Move task to another column
- `PUT /api/tasks/<task_id>/assign/` - Assign task to user

### Timer
- `GET /api/timer/sessions/` - List user's timer sessions
- `POST /api/timer/sessions/start/` - Start a new timer session
- `POST /api/timer/sessions/<session_id>/stop/` - Stop a timer session
- `DELETE /api/timer/sessions/<session_id>/delete/` - Delete a timer session
- `GET /api/timer/stats/` - Get user's timer statistics

### Analytics
- `GET /api/analytics/team/<team_id>/` - Get team analytics
- `GET /api/analytics/user/` - Get user analytics
- `GET /api/analytics/team/<team_id>/productivity/` - Get team productivity report

### Files
- `GET /api/files/files/` - List team files
- `POST /api/files/files/upload/` - Upload a file
- `GET /api/files/files/<file_id>/download/` - Download a file
- `DELETE /api/files/files/<file_id>/delete/` - Delete a file
- `GET /api/files/notes/` - List team notes
- `POST /api/files/notes/create/` - Create a note
- `GET /api/files/notes/<note_id>/` - Get note details
- `PUT /api/files/notes/<note_id>/update/` - Update a note
- `DELETE /api/files/notes/<note_id>/delete/` - Delete a note

## Deployment

### Backend
The backend can be deployed to Heroku or Render free-tier.

### Frontend
The frontend can be deployed to Vercel.

## Future Enhancements

1. Video call integration
2. Advanced analytics and reporting
3. Mobile app development
4. Integration with third-party tools (Google Drive, Slack, etc.)
5. Advanced task management features (subtasks, dependencies, etc.)
6. Customizable dashboards
7. Advanced team collaboration features

## License

This project is licensed under the MIT License.