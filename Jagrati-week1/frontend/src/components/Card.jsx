/**
 * Card — displays a single post.
 * Highlights query matches in the title.
 */
export default function Card({ post, query }) {
  const { id, userId, title, body } = post

  // Build highlighted title
  function highlight(text, term) {
    if (!term.trim()) return text
    const regex = new RegExp(`(${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
    const parts = text.split(regex)
    return parts.map((part, i) =>
      regex.test(part) ? <mark key={i}>{part}</mark> : part
    )
  }

  return (
    <article
      className="card"
      style={{ animationDelay: `${(id % 20) * 18}ms` }}
      aria-label={`Post ${id}`}
    >
      <div className="card__meta">
        <span className="card__id">#{String(id).padStart(3, '0')}</span>
        <span className="card__user-badge">user {userId}</span>
      </div>

      <h2 className="card__title">
        {highlight(title, query)}
      </h2>

      <p className="card__body">{body}</p>
    </article>
  )
}
