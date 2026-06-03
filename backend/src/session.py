import random
import string

from .shopping_cart import ShoppingCart

class Session:

	def __init__(self, account):
		# Session ID is a string of 8 random characters
		chars = string.ascii_letters + string.digits
		self.session_id = ''.join(random.choices(chars, k=8))

		self.account = account
		self.cart = ShoppingCart()
		self.active = True
	
	def logout(self):
		self.active = False

	def get_account(self):
		return self.account
	
	def get_cart(self):
		return self.get_cart
