from .models import User


class CustomAuthBackend:
	def authenticate(self, **kwargs):
		try:
			user = User.objects.get(email=kwargs['email'])
		except User.DoesNotExist:
			return None
		if user.check_password(kwargs['password']) and self.user_can_authenticate(user):
			return user

	@staticmethod
	def user_can_authenticate(user):
		is_active = getattr(user, 'is_active', None)
		return is_active and user.is_active
