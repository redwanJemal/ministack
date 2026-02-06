# 🚀 MiniStack

**Production-ready Telegram Mini App scaffold with React + FastAPI**

Clone → Configure → Deploy → Ship 🎉

---

## Features

- ⚡ **Vite + React 18** - Lightning fast frontend
- 🔐 **Telegram Auth** - Seamless login via initData
- 🎨 **Telegram Theme** - Auto dark/light mode
- 🐍 **FastAPI Backend** - Async Python API
- 🗃️ **PostgreSQL** - Production database
- 🔴 **Redis** - Sessions & caching
- 🐳 **Docker** - One-command deployment
- 📱 **Mobile-first** - Optimized for Telegram

---

## Quick Start

### 1. Clone & Configure

```bash
git clone https://github.com/yourusername/ministack.git my-mini-app
cd my-mini-app

# Copy environment files
cp .env.example .env
cp frontend/.env.example frontend/.env

# Edit .env with your bot token
nano .env
```

### 2. Create Telegram Bot

1. Message [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow prompts
3. Copy the bot token to `.env`
4. Send `/mybots` → Select bot → Bot Settings → Configure Mini App
5. Set Mini App URL to your domain

### 3. Run Locally

```bash
# Start all services
docker compose up -d

# Frontend dev server (hot reload)
cd frontend && npm install && npm run dev
```

Open: http://localhost:5173

### 4. Deploy to Production

```bash
# Build and deploy
docker compose -f docker-compose.prod.yml up -d --build
```

---

## Project Structure

```
ministack/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   │   ├── deps.py     # Dependencies (auth, db)
│   │   │   └── v1/         # API v1 routes
│   │   ├── core/           # Config, security
│   │   ├── models/         # SQLAlchemy models
│   │   └── services/       # Business logic
│   ├── alembic/            # DB migrations
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/               # React Mini App
│   ├── src/
│   │   ├── components/     # Reusable UI
│   │   ├── hooks/          # Custom hooks
│   │   ├── lib/            # Utilities
│   │   │   ├── telegram.ts # Telegram SDK
│   │   │   └── api.ts      # API client
│   │   ├── pages/          # App pages
│   │   └── App.tsx
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml      # Development
├── docker-compose.prod.yml # Production
└── .env.example
```

---

## Configuration

### Environment Variables

```bash
# .env
BOT_TOKEN=your_bot_token_here
BOT_USERNAME=YourBotUsername

# Database
DATABASE_URL=postgresql+asyncpg://ministack:secret@db:5432/ministack
POSTGRES_USER=ministack
POSTGRES_PASSWORD=secret
POSTGRES_DB=ministack

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET=your-jwt-secret-change-in-production

# App
APP_NAME=MiniStack
APP_URL=https://your-domain.com
DEBUG=false
```

---

## Telegram Mini App Features

### Authentication

Users are automatically authenticated via Telegram's `initData`. No login forms needed!

```typescript
// Frontend - get current user
import { useTelegram } from '@/hooks/useTelegram';

function Profile() {
  const { user, isReady } = useTelegram();
  
  if (!isReady) return <Loading />;
  
  return <div>Hello, {user.firstName}!</div>;
}
```

```python
# Backend - validate & get user
from app.api.deps import get_current_user

@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return user
```

### Theme Integration

Automatically matches Telegram's theme:

```typescript
// Colors from Telegram
const { themeParams } = useTelegram();

// Use in Tailwind
<div className="bg-tg-bg text-tg-text">
  Themed content
</div>
```

### Haptic Feedback

```typescript
const { haptic } = useTelegram();

<button onClick={() => {
  haptic.impact('medium');
  doSomething();
}}>
  Click me
</button>
```

### Back Button

```typescript
const { backButton } = useTelegram();

useEffect(() => {
  backButton.show();
  backButton.onClick(() => navigate(-1));
  return () => backButton.hide();
}, []);
```

---

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Development

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build
```

### Database Migrations

```bash
cd backend

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Deployment

### With Coolify

1. Create new Service → Docker Compose
2. Point to your repo
3. Set environment variables
4. Deploy!

### Manual Docker

```bash
# Production build
docker compose -f docker-compose.prod.yml up -d --build

# View logs
docker compose logs -f

# Restart
docker compose restart
```

---

## Best Practices Included

✅ Server-side initData validation  
✅ JWT tokens for API auth  
✅ Telegram theme colors in Tailwind  
✅ Proper back button handling  
✅ Safe area insets for fullscreen  
✅ Haptic feedback utilities  
✅ Error boundaries  
✅ Loading states  
✅ API request caching  
✅ Docker multi-stage builds  
✅ Database migrations  
✅ CORS configuration  
✅ Rate limiting ready  

---

## License

MIT - Use it for anything!

---

## Credits

Built with ❤️ for the Telegram developer community.

**Links:**
- [Telegram Mini Apps Docs](https://core.telegram.org/bots/webapps)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [@BotFather](https://t.me/botfather)
