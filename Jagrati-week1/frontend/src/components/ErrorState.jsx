export default function ErrorState({ message, onRetry }) {
  return (
    <div className="state state--error" role="alert">
      <span className="state__icon" aria-hidden="true">⚠</span>
      <p className="state__title">Something went wrong</p>
      <p className="state__msg">{message}</p>
      <button className="btn-retry" onClick={onRetry}>
        ↺ Retry
      </button>
    </div>
  )
}
