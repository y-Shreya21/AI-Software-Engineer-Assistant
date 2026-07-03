"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { API_BASE_URL } from "@/lib/api"

export default function RegisterPage() {
  const router = useRouter()
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault()
    if (!username.trim() || !email.trim() || !password.trim()) {
      setError("Please fill in all fields.")
      return
    }

    try {
      setLoading(true)
      setError(null)

      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      })

      const data = await response.json()

      if (!response.ok) {
        setError(data.detail || "Registration failed. Username or email may already be taken.")
        return
      }

      // Automatically sign in or redirect to login page
      router.push("/login")
    } catch (err) {
      console.error(err)
      setError("Unable to connect to the registration server.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex items-center justify-center bg-black min-h-screen p-4 text-white">
      <div className="w-full max-w-md p-8 rounded-2xl border border-zinc-800 bg-zinc-950/40 backdrop-blur-md shadow-2xl">
        <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-white via-zinc-300 to-zinc-600 bg-clip-text text-transparent">
          Create account
        </h1>
        <p className="mt-2 text-zinc-400 text-sm">
          Get started with your AI Software Engineering Workspace
        </p>

        <form onSubmit={handleRegister} className="mt-8 space-y-6">
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
              Email Address
            </label>
            <input
              type="email"
              placeholder="shreya@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
            {loading ? "Creating account..." : "Sign Up"}
          </button>
        </form>

        <div className="mt-6 text-center text-xs text-zinc-500">
          Already have an account?{" "}
          <Link href="/login" className="text-white hover:underline">
            Sign in
          </Link>
        </div>
      </div>
    </main>
  )
}
