export default function LoadingState() {
  return (
    <div className="state" role="status" aria-live="polite">
      <div className="spinner" aria-hidden="true" />
      <p className="state__title">Fetching posts…</p>
      <p className="state__msg">Connecting to the API and validating data.</p>
    </div>
  )
}
