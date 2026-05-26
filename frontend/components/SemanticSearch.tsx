"use client"

import { useState } from "react"

import { API_BASE_URL }
from "@/lib/api"

type Props = {
  onFileSelect: (path: string) => void
}

export default function SemanticSearch({
  onFileSelect
}: Props) {

  const [query, setQuery] = useState("")

  const [results, setResults] = useState<any[]>([])

  async function searchCode() {

    if (!query) return

    try {

      const response = await fetch(
        `${API_BASE_URL}/search`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            query
          })
        }
      )

      const data = await response.json()

      setResults(data.results)

    } catch (error) {

      console.error(error)
    }
  }

  return (

    <div className="mt-10">

      <h2 className="text-2xl font-bold mb-4">

        Semantic Code Search

      </h2>

      <div className="flex gap-4">

        <input
          value={query}

          onChange={(e) =>
            setQuery(e.target.value)
          }

          placeholder="Search code semantically..."

          className="flex-1 p-4 rounded-xl bg-zinc-900 border border-zinc-700"
        />

        <button
          onClick={searchCode}

          className="px-6 py-4 rounded-xl bg-white text-black font-semibold"
        >

          Search

        </button>

      </div>

      <div className="mt-6 space-y-4">

        {results.map((result, index) => (

          <div
            key={index}

            onClick={() =>
              onFileSelect(result.path)
            }

            className="bg-zinc-900 p-4 rounded-xl cursor-pointer hover:bg-zinc-800"
          >

            <p className="font-semibold">

              {result.path}

            </p>

            <p className="text-sm text-zinc-400 mt-2 line-clamp-4">

              {result.content}

            </p>

          </div>
        ))}

      </div>

    </div>
  )
}