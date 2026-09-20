#!/usr/bin/env python3
"""Simple helper function module.

This module provides a helper for computing pagination index
ranges from page number and page size parameters.
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Compute the start and end indexes for a page of results.

    Args:
        page: the 1-indexed page number to return.
        page_size: the number of items per page.

    Returns:
        A tuple (start_index, end_index) representing the range of
        indexes in a dataset that correspond to the given page and
        page_size, suitable for use as list slice bounds.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)
