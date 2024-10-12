from datetime import timedelta

import jwt
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

	is_deleted = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	class Meta:
		abstract = True


class UserManager(BaseUserManager):
	def create_user(self, **kwargs):
		if not kwargs.get('email', None):
			raise ValueError('Email must be specified!')

		with transaction.atomic():
			user = self.model(
				email=self.normalize_email(kwargs['email']),
			)
			user.set_password(kwargs['password'])
			user.is_active = True
			user.save()
		return user

	def create_superuser(self, email: str, password: str):
		if not email:
			raise ValueError('Email must be specified!')

		user = self.model(
			email=self.normalize_email(email),
		)
		user.is_superuser = True
		user.is_staff = True
		user.is_active = True
		user.set_password(password)
		user.save()
		return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
	"""Custom user model"""
	email = models.EmailField(
		verbose_name='Email address',
		max_length=255,
		unique=True,
	)
	first_name = models.CharField(max_length=255, blank=True, null=True)
	last_name = models.CharField(max_length=255, blank=True, null=True)
	password = models.CharField(max_length=255)
	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'

	objects = UserManager()

	def __str__(self):
		return self.email

	def token(self, secret_key):
		return self._generate_jwt_token(secret_key=secret_key)

	def _generate_jwt_token(self, secret_key):
		iat_dt = timezone.now()
		exp_dt = iat_dt + timedelta(days=30)
		token = jwt.encode({
			'user_id': self.id,
			'exp': exp_dt.timestamp(),
			'iat': iat_dt.timestamp(),
		}, secret_key, algorithm='HS256')
		return token

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['email'], name='unique_email'),
		]
