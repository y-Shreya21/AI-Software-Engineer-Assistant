"use client"

import type { FileTreeNode } from "@/lib/buildFileTree"

type Props = {
  tree: FileTreeNode
  openFile: (path: string) => void
  selectedFile?: string
}

export default function FileTree({
  tree,
  openFile,
  selectedFile = "",
}: Props) {
  return (
    <div className="ml-3">
      {Object.keys(tree).map((key) => {
        const node = tree[key]
        const isFile = typeof node === "string"

        return (
          <div key={isFile ? node : key} className="mt-1">
            {isFile ? (
              <div
                onClick={() => openFile(node)}
                className={`cursor-pointer text-sm hover:text-white ${
                  selectedFile === node
                    ? "text-white font-semibold"
                    : "text-zinc-300"
                }`}
              >
                📄 {key}
              </div>
            ) : (
              <div>
                <div className="text-sm font-semibold text-zinc-400">
                  📁 {key}
                </div>
                <FileTree
                  tree={node}
                  openFile={openFile}
                  selectedFile={selectedFile}
                />
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
