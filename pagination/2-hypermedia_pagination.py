#!/usr/bin/env python3
"""Hypermedia pagination module.

This module provides a Server class that paginates a dataset of
popular baby names and returns hypermedia metadata alongside each
page of results.
"""
import csv
import math
from typing import Dict, List, Tuple


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


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the server with no dataset loaded yet."""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Return the cached dataset, loading it from disk if needed.

        Returns:
            A list of rows (each a list of strings) from the CSV
            file, excluding the header row.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Return a page of the dataset for given pagination params.

        Args:
            page: the 1-indexed page number to return (default 1).
            page_size: the number of items per page (default 10).

        Returns:
            The list of rows in the dataset corresponding to the
            requested page, or an empty list if the page and
            page_size are out of range for the dataset.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Return a page of the dataset with hypermedia metadata.

        Args:
            page: the 1-indexed page number to return (default 1).
            page_size: the number of items per page (default 10).

        Returns:
            A dictionary with keys page_size (the length of the
            returned page), page (the current page number), data
            (the page of the dataset), next_page (the next page
            number, or None if there isn't one), prev_page (the
            previous page number, or None if there isn't one), and
            total_pages (the total number of pages in the dataset).
        """
        data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)

        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages,
        }
