import pandas as pd

from .payment import Payment
from .payment_method import PaymentMethod, CardPayment, ApplePay, GooglePay

class PaymentManager:
	def __init__(self):
		# payment_id -> payment
		self.payments: dict[int, Payment] = {}
		# order_id -> payment
		self.payments_by_order: dict[id, id] = {}
		self.payment_methods: dict[str, PaymentMethod] = {
			"card": CardPayment(),
			"apple": ApplePay(),
			"google": GooglePay()
		}

	def add_payment(self, payment: Payment):
		self.payments[payment.id] = payment
		self.payments_by_order[payment.order_id] = payment.id

	def remove_payment(self, payment_id: int):
		payment = self.payments.pop(payment_id, None)
		if payment is not None:
			self.payments_by_order.pop(payment.order_id)

	def get_payments(self) -> list[Payment]:
		return list(self.payments.values())
	
	def get_payment_by_id(self, id: int) -> Payment | None:
		return self.payments.get(id)
	
	def get_payment_by_order_id(self, order_id: int) -> Payment | None:
		payment_id = self.payments_by_order.get(order_id)
		return self.payments.get(payment_id)
	
	def pay(
			self,
			order_id: int, 
			full_name: str,
			email: str,
			address: str,
			shipping_method: str,
			payment_method: str
		) -> str:
		if self.payment_methods.get(payment_method) is None:
			return "Not a valid payment method."
		msg = self.payment_methods[payment_method].pay()
		id = self.generate_payment_id()
		payment = Payment(id, order_id, full_name, email, address, shipping_method, payment_method)
		self.add_payment(payment)
		return msg

	def generate_payment_id(self) -> int:
		if not self.payments:
			return 1
		return max(self.payments.keys()) + 1 
	
	def load_csv(self, path: str):
		df = pd.read_csv(path)
		payments = [
			Payment.from_dict(record)
			for record in df.to_dict("records")
		]
		for payment in payments:
			self.add_payment(payment)

	def export_csv(self, path: str):
		df = pd.DataFrame(
			[payment.to_dict() for payment in self.payments.values()]
		)
		df.to_csv(path, index=False)