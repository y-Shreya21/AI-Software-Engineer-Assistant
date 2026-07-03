"use client"

import { useState } from "react"

import { API_BASE_URL } from "@/lib/api"

type Props = {
  setRepository: (repository: string) => void
  setTotalFiles: (totalFiles: number) => void
  setTotalChunks: (totalChunks: number) => void
  setFiles: (files: string[]) => void
}

type IndexResponse = {
  status: string
  repository?: string
  total_files: number
  total_chunks: number
  files?: string[]
  detail?: string
}

export default function RepoIndexer({
  setRepository,
  setTotalFiles,
  setTotalChunks,
  setFiles,
}: Props) {
  const [githubUrl, setGithubUrl] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  async function handleIndexRepository() {
    if (!githubUrl.trim()) {
      setError("Enter a GitHub repository URL.")
      return
    }

    try {
      setLoading(true)
      setError(null)
      setSuccess(null)

      const token = localStorage.getItem("access_token")
      const response = await fetch(`${API_BASE_URL}/repos/index`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({
          github_url: githubUrl.trim(),
        }),
      })

      const data: IndexResponse = await response.json()

      if (!response.ok) {
        setError(
          typeof data.detail === "string"
            ? data.detail
            : "Failed to index repository"
        )
        return
      }

      setRepository(data.repository ?? githubUrl.trim())
      setTotalFiles(data.total_files)
      setTotalChunks(data.total_chunks)
      setFiles(data.files ?? [])
      setSuccess(
        `Indexed ${data.total_files} files (${data.total_chunks} chunks).`
      )
    } catch (err) {
      console.error(err)
      setError(
        "Could not reach the backend. Start it with: cd backend && python -m uvicorn app.main:app"
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mt-10 max-w-2xl">
      <h2 className="text-2xl font-semibold mb-4">Index GitHub Repository</h2>

      <input
        type="text"
        placeholder="https://github.com/owner/repo"
        value={githubUrl}
        onChange={(e) => setGithubUrl(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") handleIndexRepository()
        }}
        className="w-full p-4 rounded-lg bg-zinc-900 border border-zinc-700"
      />

      <button
        onClick={handleIndexRepository}
        disabled={loading}
        className="mt-4 px-6 py-3 rounded-lg bg-white text-black font-semibold disabled:opacity-50"
      >
        {loading ? "Indexing..." : "Index Repository"}
      </button>

      {error && <p className="mt-4 text-red-400 text-sm">{error}</p>}
      {success && <p className="mt-4 text-green-400 text-sm">{success}</p>}
    </div>
  )
}
