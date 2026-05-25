"use client"

import mermaid from "mermaid"
import { useEffect, useId, useRef } from "react"

type Props = {
  chart: string
}

export default function ArchitectureDiagram({ chart }: Props) {
  const ref = useRef<HTMLDivElement>(null)
  const renderId = useId().replace(/:/g, "")

  useEffect(() => {
    if (!chart || !ref.current) return

    let cancelled = false

    mermaid.initialize({
      startOnLoad: false,
      theme: "dark",
    })

    mermaid
      .render(`mermaid-${renderId}-${Date.now()}`, chart)
      .then(({ svg }) => {
        if (!cancelled && ref.current) {
          ref.current.innerHTML = svg
        }
      })
      .catch((error) => {
        console.error(error)
        if (!cancelled && ref.current) {
          ref.current.innerHTML =
            '<p class="text-red-400 text-sm">Failed to render diagram.</p>'
        }
      })

    return () => {
      cancelled = true
    }
  }, [chart, renderId])

  return (
    <div
      ref={ref}
      className="bg-zinc-950 p-6 rounded-2xl overflow-auto min-h-[400px]"
    />
  )
}
