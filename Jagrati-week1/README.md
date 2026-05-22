# Public-API Explorer

A full-stack app that fetches posts from [JSONPlaceholder](https://jsonplaceholder.typicode.com), validates them with **Pydantic**, and displays them in a searchable card grid built with **React + Vite**.

```
public-api-explorer/
├── backend/          # FastAPI + Pydantic + python-dotenv
│   ├── main.py
│   ├── requirements.txt
│   ├── .env          # copied from .env.example
│   └── .env.example
└── frontend/         # React + Vite
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── App.jsx
        ├── index.css
        ├── main.jsx
        ├── hooks/
        │   └── usePosts.js       # data-fetching hook (useState + useEffect)
        └── components/
            ├── Card.jsx          # reusable card rendered via .map()
            ├── LoadingState.jsx
            └── ErrorState.jsx
```

---

## Backend setup

```bash
cd backend
cp .env.example .env          # edit if you have an API key
pip install -r requirements.txt
uvicorn main:app --reload
```

> API available at **http://localhost:8000/api/posts**  
> Interactive docs at **http://localhost:8000/docs**

**Environment variables (`.env`)**

| Variable            | Default                                  | Notes                                  |
|---------------------|------------------------------------------|----------------------------------------|
| `API_BASE_URL`      | `https://jsonplaceholder.typicode.com`   | Base URL for the upstream REST API     |
| `API_KEY`           | *(empty)*                                | Sent as `Authorization: Bearer <key>` if set |
| `USE_MOCK_FALLBACK` | `false`                                  | Set `true` to always serve mock data   |

If the upstream API is unreachable the server **never crashes** — it automatically falls back to 20 built-in mock posts and logs a warning.

---

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

> App available at **http://localhost:5173**

Vite proxies `/api/*` → `http://localhost:8000`, so the frontend only needs the backend running — no CORS issues, no extra config.

---

## Features

| Layer     | Feature                                                              |
|-----------|----------------------------------------------------------------------|
| Backend   | FastAPI endpoint · Pydantic model validation · `python-dotenv` config · graceful error handling with automatic mock fallback |
| Frontend  | `useState` + `useEffect` data fetching · live search/filter with match highlighting · Loading / Error / Empty states · reusable `<Card />` component · staggered card animations |

---

## Tech stack

- **Backend**: Python 3.11+, FastAPI, Uvicorn, Requests, Pydantic v2, python-dotenv  
- **Frontend**: React 18, Vite 5, vanilla CSS (no framework)  
- **API**: [JSONPlaceholder](https://jsonplaceholder.typicode.com) (free, no key required)
