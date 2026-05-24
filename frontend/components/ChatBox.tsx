"use client"

import { useState } from "react"
import ReactMarkdown from "react-markdown"
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter"
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism"

import { API_BASE_URL } from "@/lib/api"

type ChatMessage = {
  role: "user" | "assistant"
  content: string
  sources?: string[]
}

export default function ChatBox() {
  const [question, setQuestion] = useState("")
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [error, setError] = useState<string | null>(null)

  async function askQuestion() {
    if (!question.trim() || loading) return

    const currentQuestion = question.trim()

    try {
      setLoading(true)
      setError(null)

      const userMessage: ChatMessage = {
        role: "user",
        content: currentQuestion,
      }

      setMessages((prev) => [...prev, userMessage])

      const response = await fetch(`${API_BASE_URL}/chat/stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: currentQuestion,
        }),
      })

      if (!response.ok) {
        const data = await response.json().catch(() => ({}))
        setError(
          typeof data.detail === "string"
            ? data.detail
            : "Failed to get a response from the assistant"
        )
        return
      }

      const reader = response.body?.getReader()

      if (!reader) {
        setError("Streaming is not supported in this browser response.")
        return
      }

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: "",
        sources: [],
      }

      setMessages((prev) => [...prev, assistantMessage])

      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()

        if (done) break

        assistantMessage.content += decoder.decode(value)

        setMessages((prev) => {
          const updated = [...prev]
          updated[updated.length - 1] = { ...assistantMessage }
          return updated
        })
      }

      setQuestion("")
    } catch (err) {
      console.error(err)
      setError("Could not reach the chat API. Is the backend running?")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mt-10 max-w-4xl">
      <h2 className="text-2xl font-semibold mb-4">AI Repository Chat</h2>

      <div className="space-y-4 mb-6 min-h-[200px]">
        {messages.length === 0 && (
          <p className="text-zinc-500 text-sm">
            Ask questions about the indexed codebase.
          </p>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`p-4 rounded-xl ${
              message.role === "user" ? "bg-blue-600" : "bg-zinc-900"
            }`}
          >
            <ReactMarkdown
              components={{
                code({ className, children }) {
                  const match = /language-(\w+)/.exec(className || "")

                  return match ? (
                    <SyntaxHighlighter
                      style={oneDark}
                      language={match[1]}
                      PreTag="div"
                    >
                      {String(children).replace(/\n$/, "")}
                    </SyntaxHighlighter>
                  ) : (
                    <code className="bg-zinc-800 px-1 py-0.5 rounded">
                      {children}
                    </code>
                  )
                },
              }}
            >
              {message.content}
            </ReactMarkdown>

            {message.sources && message.sources.length > 0 && (
              <div className="mt-3">
                <p className="text-sm text-zinc-400 mb-2">Sources</p>
                <ul className="text-xs text-zinc-500 space-y-1">
                  {message.sources.map((source, i) => (
                    <li key={i}>{source}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>

      {error && <p className="mb-4 text-red-400 text-sm">{error}</p>}

      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Ask repository questions..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") askQuestion()
          }}
          className="flex-1 p-4 rounded-xl bg-zinc-900 border border-zinc-700"
        />

        <button
          onClick={askQuestion}
          disabled={loading}
          className="px-6 py-4 rounded-xl bg-white text-black font-semibold disabled:opacity-50"
        >
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>
    </div>
  )
}
