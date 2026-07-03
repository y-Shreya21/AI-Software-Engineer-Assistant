"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { API_BASE_URL } from "@/lib/api"

export default function LoginPage() {
  const router = useRouter()
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    if (!username.trim() || !password.trim()) {
      setError("Please fill in all fields.")
      return
    }

    try {
      setLoading(true)
      setError(null)

      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      })

      const data = await response.json()

      if (!response.ok) {
        setError(data.detail || "Authentication failed. Incorrect username or password.")
        return
      }

      // Store tokens
      localStorage.setItem("access_token", data.access_token)
      localStorage.setItem("refresh_token", data.refresh_token)
      localStorage.setItem("username", username)

      // Redirect to main workspace
      router.push("/")
    } catch (err) {
      console.error(err)
      setError("Unable to connect to the authentication server.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex items-center justify-center bg-black min-h-screen p-4 text-white">
      <div className="w-full max-w-md p-8 rounded-2xl border border-zinc-800 bg-zinc-950/40 backdrop-blur-md shadow-2xl">
        <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-white via-zinc-300 to-zinc-600 bg-clip-text text-transparent">
          Welcome back
        </h1>
        <p className="mt-2 text-zinc-400 text-sm">
          Sign in to your AI Software Engineering Workspace
        </p>

        <form onSubmit={handleLogin} className="mt-8 space-y-6">
          <div className="space-y-1">
            <label className="text-zinc-300 text-xs font-semibold uppercase tracking-wider">
              Username
            </label>
            <input
              type="text"
              placeholder="shreya_yadav"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full p-4 rounded-xl bg-zinc-900 border border-zinc-800 focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500 outline-none transition text-sm"
            />
          </div>

          <div className="space-y-1">
            <label className="text-zinc-300 text-xs font-semibold uppercase tracking-wider">
              Password
            </label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-4 rounded-xl bg-zinc-900 border border-zinc-800 focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500 outline-none transition text-sm"
            />
          </div>

          {error && <p className="text-red-400 text-xs mt-2">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 rounded-xl bg-white text-black font-semibold text-sm hover:bg-zinc-200 disabled:opacity-50 transition duration-200"
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <div className="mt-6 text-center text-xs text-zinc-500">
          Don't have an account?{" "}
          <Link href="/register" className="text-white hover:underline">
            Create account
          </Link>
        </div>
      </div>
    </main>
  )
}
