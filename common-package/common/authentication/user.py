class CustomUser:
	def __init__(self, data):
		self.id = data.get('user_id')
		self.email = data.get('email')
		self.mobile_phone = data.get('mobile_phone')
		self.user_type = data.get('user_type')
		self.first_name = data.get('first_name')
		self.last_name = data.get('last_name')
		self.image_url = data.get('image_url')
		self.token = data.get('token')
		self.name = f"{self.first_name} {self.last_name}"

	@staticmethod
	def is_authenticated():
		return True

	def __str__(self):
		return f"{self.id} ({self.user_type})"
