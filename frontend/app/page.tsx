"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"

import RepoIndexer from "@/components/RepoIndexer"
import ChatBox from "@/components/ChatBox"
import RepositorySidebar from "@/components/RepositorySidebar"
import FileViewer from "@/components/FileViewer"
import ArchitectureDiagram from "@/components/ArchitectureDiagram"
import { API_BASE_URL } from "@/lib/api"
import SemanticSearch from "@/components/SemanticSearch"

export default function HomePage() {
  const router = useRouter()
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [repository, setRepository] = useState("")
  const [totalFiles, setTotalFiles] = useState(0)
  const [totalChunks, setTotalChunks] = useState(0)
  const [files, setFiles] = useState<string[]>([])
  const [selectedFile, setSelectedFile] = useState("")
  const [fileContent, setFileContent] = useState("")
  const [diagram, setDiagram] = useState("")

  useEffect(() => {
    const token = localStorage.getItem("access_token")
    if (!token) {
      router.push("/login")
    } else {
      setIsAuthenticated(true)
    }
  }, [router])

  async function handleFileSelect(filePath: string) {
    setSelectedFile(filePath)
    setFileContent("")

    try {
      const token = localStorage.getItem("access_token")
      const response = await fetch(
        `${API_BASE_URL}/repos/file?path=${encodeURIComponent(filePath)}`,
        {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        }
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

  async function loadArchitecture() {
    try {
      const token = localStorage.getItem("access_token")
      const response = await fetch(`${API_BASE_URL}/architecture/graph`, {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      })
      const data = await response.json()
      setDiagram(data.diagram)
    } catch (error) {
      console.error(error)
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="bg-black min-h-screen flex items-center justify-center text-zinc-500 text-sm">
        Verifying session...
      </div>
    )
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

        <button
          onClick={() => loadArchitecture()}
          className="mt-6 px-6 py-3 rounded-xl bg-white text-black font-semibold"
        >
          Generate Architecture Diagram
        </button>

        <RepoIndexer
          setRepository={setRepository}
          setTotalFiles={setTotalFiles}
          setTotalChunks={setTotalChunks}
          setFiles={setFiles}
        />

        <ChatBox />
        <SemanticSearch
          onFileSelect={handleFileSelect}
        />

        {diagram && (
          <div className="mt-10">
            <h2 className="text-2xl font-bold mb-4">
              Architecture Diagram
            </h2>
            <ArchitectureDiagram chart={diagram} />
          </div>
        )}
      </div>
    </main>
  )
}
