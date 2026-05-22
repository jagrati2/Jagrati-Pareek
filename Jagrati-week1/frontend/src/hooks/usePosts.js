import { useState, useEffect, useCallback } from 'react'

const API_URL = '/api/posts'

/**
 * usePosts — fetches post data from the backend.
 * Returns { posts, loading, error, refetch }.
 */
export function usePosts() {
  const [posts, setPosts]     = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState(null)

  const fetchPosts = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const res = await fetch(API_URL)

      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body.detail ?? `HTTP ${res.status}`)
      }

      const data = await res.json()
      setPosts(data.posts ?? [])
    } catch (err) {
      if (err.name === 'AbortError') return
      setError(
        err.message === 'Failed to fetch'
          ? 'Cannot reach the backend. Make sure it is running on port 8000.'
          : err.message
      )
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchPosts()
  }, [fetchPosts])

  return { posts, loading, error, refetch: fetchPosts }
}
