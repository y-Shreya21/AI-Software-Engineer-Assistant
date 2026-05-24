import ReactMarkdown from "react-markdown"

import { Prism as SyntaxHighlighter }
from "react-syntax-highlighter"

import { oneDark }
from "react-syntax-highlighter/dist/esm/styles/prism"

type Props = {
  selectedFile: string
  fileContent: string
}

export default function FileViewer({
  selectedFile,
  fileContent
}: Props) {

  if (!selectedFile) {

    return (

      <div className="flex-1 flex items-center justify-center text-zinc-500">

        Select a source file

      </div>
    )
  }

  return (

    <div className="flex-1 overflow-auto p-6">

      <h2 className="text-xl font-bold mb-4 break-all">
        {selectedFile}
      </h2>

      <SyntaxHighlighter
        language="python"
        style={oneDark}
      >

        {fileContent}

      </SyntaxHighlighter>

    </div>
  )
}