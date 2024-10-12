from django.db import models


class Order(models.Model):
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('shipped', 'Shipped'),
		('delivered', 'Delivered'),
		('canceled', 'Canceled'),
	]
	user_id = models.IntegerField()
	product_name = models.CharField(max_length=255)
	quantity = models.PositiveIntegerField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Order #{self.id} by {self.user_id} - {self.status}"


class OrderHistory(models.Model):
	order = models.ForeignKey(Order, related_name='history', on_delete=models.CASCADE)
	status = models.CharField(max_length=20)
	changed_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Order #{self.order.id} status changed to '{self.status}' at {self.changed_at}"
