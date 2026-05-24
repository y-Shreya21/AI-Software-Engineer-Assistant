"use client"

import { useState } from "react"

import RepoIndexer from "@/components/RepoIndexer"
import ChatBox from "@/components/ChatBox"
import RepositorySidebar from "@/components/RepositorySidebar"

export default function HomePage() {

  const [repository, setRepository] = useState("")
  const [totalFiles, setTotalFiles] = useState(0)
  const [totalChunks, setTotalChunks] = useState(0)
  const [files, setFiles] = useState<string[]>([])

  return (

    <main className="flex bg-black text-white min-h-screen">

      <RepositorySidebar
        repository={repository}
        totalFiles={totalFiles}
        totalChunks={totalChunks}
        files={files}
      />

      <div className="flex-1 p-10">

        <h1 className="text-5xl font-bold">
          AI Software Engineer Assistant
        </h1>

        <p className="mt-4 text-zinc-400 text-lg">
          AI-powered codebase understanding platform.
        </p>

        <RepoIndexer
          setRepository={setRepository}
          setTotalFiles={setTotalFiles}
          setTotalChunks={setTotalChunks}
          setFiles={setFiles}
        />

        <ChatBox />

      </div>

    </main>
  )
}