import os
import tempfile
from git import Repo

def clone_repository(github_url: str) -> str:
    """
    Clone repository into temporary directory.
    Returns local path.
    """

    temp_dir = tempfile.mkdtemp()

    Repo.clone_from(
        github_url,
        temp_dir
    )

    return temp_dir