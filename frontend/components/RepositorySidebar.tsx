import FileTree from "./FileTree"
import { buildFileTree } from "@/lib/buildFileTree"

type Props = {
  repository: string
  totalFiles: number
  totalChunks: number
  files: string[]
  selectedFile: string
  onFileSelect: (filePath: string) => void
}



export default function RepositorySidebar({
  repository,
  totalFiles,
  totalChunks,
  files,
  selectedFile,
  onFileSelect,
}: Props) {
  const tree = buildFileTree(files)
  return (
    <aside className="w-80 shrink-0 h-screen bg-zinc-950 border-r border-zinc-800 p-5 overflow-y-auto">
      <h2 className="text-2xl font-bold mb-6">Repository</h2>

      <div className="mb-6">
        <p className="text-zinc-400 text-sm">Active Repository</p>
        <p className="font-semibold break-all mt-1">
          {repository || "No repository indexed"}
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-8">
        <div className="bg-zinc-900 p-4 rounded-xl">
          <p className="text-zinc-400 text-sm">Files</p>
          <p className="text-2xl font-bold mt-2">{totalFiles}</p>
        </div>

        <div className="bg-zinc-900 p-4 rounded-xl">
          <p className="text-zinc-400 text-sm">Chunks</p>
          <p className="text-2xl font-bold mt-2">{totalChunks}</p>
        </div>
      </div>
      <FileTree
        tree={tree}
        openFile={onFileSelect}
        selectedFile={selectedFile}
      />
    </aside>
  )
}
