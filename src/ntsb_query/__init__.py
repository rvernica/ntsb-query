"""
NTSB Query Tool Package
Provides tools for querying the NTSB CAROL database.
"""

from .query import NTSBSearchModel, NTSBSearchTool

__all__ = ["NTSBSearchTool", "NTSBSearchModel"]
