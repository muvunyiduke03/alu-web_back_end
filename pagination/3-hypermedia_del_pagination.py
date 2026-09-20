#!/usr/bin/env python3
"""Deletion-resilient hypermedia pagination.

This module provides a Server class that paginates a dataset of
popular baby names in a way that stays consistent even if rows are
deleted from the dataset between requests.
"""
import csv
import math
from typing import Dict, List


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the server with no dataset loaded yet."""
        self.__dataset = None
        self.__indexed_dataset = None

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

    def indexed_dataset(self) -> Dict[int, List]:
        """Return the dataset indexed by its original sort position.

        Returns:
            A dictionary mapping each row's original position
            (starting at 0) to that row. Deleting an entry from
            this dictionary simulates a row being removed from the
            dataset without shifting the positions of other rows.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None,
                         page_size: int = 10) -> Dict:
        """Return a deletion-resilient page of the indexed dataset.

        Args:
            index: the start index of the page to return.
            page_size: the number of items to include in the page.

        Returns:
            A dictionary with keys index (the requested start
            index), next_index (the index to request for the
            following page), page_size (the actual number of items
            returned), and data (the list of rows for this page).

        Walking forward from index and skipping any indexes that
        are no longer present in the indexed dataset (because their
        rows were deleted) ensures that a user paging through the
        dataset never misses a row, even if rows were removed
        between two requests.
        """
        data = self.indexed_dataset()
        max_index = max(data.keys())

        assert index is not None and 0 <= index <= max_index

        page_data = []
        current_index = index

        while len(page_data) < page_size and current_index <= max_index:
            if current_index in data:
                page_data.append(data[current_index])
            current_index += 1

        return {
            "index": index,
            "next_index": current_index,
            "page_size": len(page_data),
            "data": page_data,
        }
