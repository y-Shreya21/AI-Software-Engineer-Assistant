type Props = {
  repository: string
  totalFiles: number
  totalChunks: number
  files: string[]
}

function fileLabel(path: string) {
  const parts = path.split("/")
  return parts[parts.length - 1] || path
}

export default function RepositorySidebar({
  repository,
  totalFiles,
  totalChunks,
  files,
}: Props) {
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

      <div>
        <h3 className="text-lg font-semibold mb-3">Indexed Files</h3>

        {files.length === 0 ? (
          <p className="text-sm text-zinc-500">
            Index a repository to see scanned files here.
          </p>
        ) : (
          <ul className="space-y-2">
            {files.map((file) => (
              <li
                key={file}
                title={file}
                className="bg-zinc-900 p-3 rounded-lg text-sm text-zinc-300 break-all"
              >
                {fileLabel(file)}
              </li>
            ))}
          </ul>
        )}
      </div>
    </aside>
  )
}
