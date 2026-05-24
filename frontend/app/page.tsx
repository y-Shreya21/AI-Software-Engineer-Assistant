"use client"

import { useState } from "react"

import RepoIndexer from "@/components/RepoIndexer"
import ChatBox from "@/components/ChatBox"
import RepositorySidebar from "@/components/RepositorySidebar"
import FileViewer from "@/components/FileViewer"
import { API_BASE_URL } from "@/lib/api"

export default function HomePage() {
  const [repository, setRepository] = useState("")
  const [totalFiles, setTotalFiles] = useState(0)
  const [totalChunks, setTotalChunks] = useState(0)
  const [files, setFiles] = useState<string[]>([])
  const [selectedFile, setSelectedFile] = useState("")
  const [fileContent, setFileContent] = useState("")

  async function handleFileSelect(filePath: string) {
    setSelectedFile(filePath)
    setFileContent("")

    try {
      const response = await fetch(
        `${API_BASE_URL}/repos/file?path=${encodeURIComponent(filePath)}`
      )

      if (!response.ok) {
        const data = await response.json().catch(() => ({}))
        setFileContent(
          typeof data.detail === "string"
            ? data.detail
            : "Failed to load file"
        )
        return
      }

      const data = await response.json()
      setSelectedFile(data.path)
      setFileContent(data.content)
    } catch (error) {
      console.error(error)
      setFileContent("Failed to load file")
    }
  }

  return (
    <main className="flex bg-black text-white min-h-screen">
      <RepositorySidebar
        repository={repository}
        totalFiles={totalFiles}
        totalChunks={totalChunks}
        files={files}
        selectedFile={selectedFile}
        onFileSelect={handleFileSelect}
      />

      <FileViewer
        selectedFile={selectedFile}
        fileContent={fileContent}
      />

      <div className="flex-1 p-10 overflow-y-auto">
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
