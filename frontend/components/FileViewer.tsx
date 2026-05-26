"use client"

import { useState } from "react"
import ReactMarkdown from "react-markdown"
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter"
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism"
import { API_BASE_URL } from "@/lib/api"

type Props = {
  selectedFile: string
  fileContent: string
}

export default function FileViewer({
  selectedFile,
  fileContent
}: Props) {
  const [generatedTests, setGeneratedTests] = useState("")
  const [review, setReview] =
  useState("")
  async function generateTests() {

    try {
  
      const response = await fetch(
        `${API_BASE_URL}/tests/generate`,
        {
          method: "POST",
  
          headers: {
            "Content-Type": "application/json"
          },
  
          body: JSON.stringify({
            code: fileContent
          })
        }
      )
  
      const data = await response.json()
  
      setGeneratedTests(data.tests)
  
    } catch (error) {
  
      console.error(error)
    }
  }
  <button
  onClick={analyzeCode}
  className="mb-6 ml-4 px-4 py-2 rounded-lg bg-red-500 text-white font-semibold"
>

  Analyze Code

</button>
  async function analyzeCode() {

    try {
  
      const response = await fetch(
        "http://127.0.0.1:8000/review/analyze",
        {
          method: "POST",
  
          headers: {
            "Content-Type": "application/json"
          },
  
          body: JSON.stringify({
            code: fileContent
          })
        }
      )
  
      const data = await response.json()
  
      setReview(data.review)
  
    } catch (error) {
  
      console.error(error)
    }
  }

  if (!selectedFile) {

    return (

      <div className="flex-1 flex items-center justify-center text-zinc-500">

        Select a source file

      </div>
    )
  }

  return (

    <div className="flex-1 overflow-auto p-6">

      <button
        onClick={generateTests}
        className="mb-6 px-4 py-2 rounded-lg bg-white text-black font-semibold"
      >
        Generate Tests
      </button>

      <h2 className="text-xl font-bold mb-4 break-all">
        {selectedFile}
      </h2>

      <SyntaxHighlighter
        language="python"
        style={oneDark}
      >

        {fileContent}

      </SyntaxHighlighter>

      {generatedTests && (
        <div className="mt-6 rounded-xl bg-zinc-900 p-4">
          <h3 className="mb-3 text-lg font-semibold">Generated Tests</h3>
          <ReactMarkdown>{generatedTests}</ReactMarkdown>
        </div>
      )}
      {review && (

<div className="mt-10">

  <h2 className="text-2xl font-bold mb-4">

    AI Code Review

  </h2>

  <div className="bg-zinc-900 rounded-2xl p-6 overflow-auto">

    <ReactMarkdown>

      {review}

    </ReactMarkdown>

  </div>

</div>
)}

    </div>
  )
}