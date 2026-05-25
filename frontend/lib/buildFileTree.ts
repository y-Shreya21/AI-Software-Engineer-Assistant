export type FileTreeNode = {
  [name: string]: string | FileTreeNode
}

export function buildFileTree(paths: string[]): FileTreeNode {
  const tree: FileTreeNode = {}

  for (const originalPath of paths) {
    const normalizedPath = originalPath.startsWith("/")
      ? originalPath.slice(1)
      : originalPath

    const parts = normalizedPath.split("/")
    let current = tree

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i]
      const isLast = i === parts.length - 1

      if (isLast) {
        current[part] = originalPath
      } else {
        const next = current[part]
        if (typeof next !== "object") {
          current[part] = {}
        }
        current = current[part] as FileTreeNode
      }
    }
  }

  return tree
}
