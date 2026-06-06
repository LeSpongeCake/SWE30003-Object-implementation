# base_csv_repository.py
import csv
from abc import ABC, abstractmethod

class Repository(ABC):

	def __init__(self, path: str):
		self.path = path
		self._data: dict[int, object] = {}
		self._load()

	def _load(self):
		try:
			with open(self.path, "r", newline="", encoding="utf-8") as f:
				for row in csv.DictReader(f):
					item = self._row_to_item(row)
					self._data[self._get_id(item)] = item
		except FileNotFoundError:
			self._save_all()

	def _save_all(self):
		with open(self.path, "w", newline="", encoding="utf-8") as f:
			writer = csv.DictWriter(f, fieldnames=self._fieldnames)
			writer.writeheader()
			for item in self._data.values():
				writer.writerow(self._item_to_row(item))

	def get_by_id(self, id: int):
		return self._data.get(id)

	def get_all(self) -> list:
		return list(self._data.values())

	def save(self, item):
		self._data[self._get_id(item)] = item
		self._save_all()

	def delete(self, id: int):
		self._data.pop(id, None)
		self._save_all()

	@property
	@abstractmethod
	def _fieldnames(self) -> list[str]:
		pass

	@abstractmethod
	def _row_to_item(self, row: dict):
		pass

	@abstractmethod
	def _item_to_row(self, item) -> dict: 
		pass

	@abstractmethod
	def _get_id(self, item) -> int:
		pass