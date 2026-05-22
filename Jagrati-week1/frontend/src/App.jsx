import { useState, useMemo } from 'react'
import Card from './components/Card.jsx'
import LoadingState from './components/LoadingState.jsx'
import ErrorState from './components/ErrorState.jsx'
import { usePosts } from './hooks/usePosts.js'

export default function App() {
  const { posts, loading, error, refetch } = usePosts()
  const [query, setQuery] = useState('')

  // Filter posts by title or body, case-insensitive
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return posts
    return posts.filter(
      (p) =>
        p.title.toLowerCase().includes(q) ||
        p.body.toLowerCase().includes(q)
    )
  }, [posts, query])

  return (
    <div className="app">
      {/* ── Header ───────────────────────────────────── */}
      <header className="header">
        <p className="header__eyebrow">JSONPlaceholder · REST</p>
        <h1 className="header__title">
          Public<span>-API</span> Explorer
        </h1>
        <p className="header__subtitle">
          Browse and search 100 posts fetched live from the backend,
          validated with Pydantic.
        </p>
      </header>

      {/* ── Search ───────────────────────────────────── */}
      <div className="search-wrap">
        <i className="search-wrap__icon" aria-hidden="true">⌕</i>
        <input
          className="search-input"
          type="search"
          placeholder="Filter by title or body…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          aria-label="Search posts"
          disabled={loading || !!error}
        />
      </div>

      {/* ── States / Content ─────────────────────────── */}
      {loading && <LoadingState />}

      {!loading && error && (
        <ErrorState message={error} onRetry={refetch} />
      )}

      {!loading && !error && (
        <>
          {/* Stats */}
          <div className="stats" aria-live="polite">
            <span>
              <span className="stats__count">{filtered.length}</span>{' '}
              {filtered.length === 1 ? 'post' : 'posts'}
              {query && ` matching "${query}"`}
            </span>
            {query && filtered.length !== posts.length && (
              <>
                <div className="stats__divider" />
                <span>{posts.length} total</span>
              </>
            )}
          </div>

          {/* Grid of cards */}
          {filtered.length > 0 ? (
            <main className="grid">
              {filtered.map((post) => (
                <Card key={post.id} post={post} query={query} />
              ))}
            </main>
          ) : (
            <div className="state state--empty">
              <span className="state__icon" aria-hidden="true">🔍</span>
              <p className="state__title">No results</p>
              <p className="state__msg">
                No posts match &ldquo;{query}&rdquo;. Try a different term.
              </p>
            </div>
          )}
        </>
      )}
    </div>
  )
}
