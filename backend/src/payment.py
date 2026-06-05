from enum import Enum


class ShippingMethod(Enum):
	POST = "post"
	PICKUP = "pickup"


class Payment:
	def __init__(
			self, 
			id: int,
			order_id: int,
			full_name: str,
			email: str,
			address: str,
			shipping_method: ShippingMethod,
			payment_method: str
		):
		self.id = id
		self.order_id = order_id

		self.full_name = full_name
		self.email = email
		self.address = address
		try:
			self.shipping_method = ShippingMethod(shipping_method)
		except ValueError:
			raise ValueError("Invalid shipping method")
		self.payment_method = payment_method 

	@classmethod
	def from_dict(cls, data):
		return cls(
			id=int(data["id"]),
			order_id=int(data["order_id"]),
			full_name=data["full_name"],
			email=data["email"],
			address=data["address"],
			shipping_method=ShippingMethod(data["shipping_method"]),
			payment_method=data["payment_method"],
		)

	def to_dict(self):
		return {
			"id": self.id,
			"order_id": self.order_id,
			"full_name": self.full_name,
			"email": self.email,
			"address": self.address,
			"shipping_method": self.shipping_method.value,
			"payment_method": self.payment_method,
		}