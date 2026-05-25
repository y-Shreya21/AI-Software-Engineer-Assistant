
from fastapi import APIRouter

from app.services.file_service import scan_repository

from app.services.architecture_service import (
    analyze_dependencies,
    generate_mermaid
)

router = APIRouter()


@router.get("/graph")
async def architecture_graph():

    files = scan_repository(".")

    graph = analyze_dependencies(files)

    return {
        "graph": graph,
        "diagram": generate_mermaid(graph)
    }