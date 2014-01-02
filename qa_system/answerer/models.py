from django.db import models



class Document(models.Model):
	content_txt = models.TextField()
	link = models.CharField(max_length=512)
	to_result = models.ForeignKey('Results')

	def __unicode__(self):  # Python 3: def __str__(self):
		return self.link

	

class Results(models.Model):
	question = models.TextField()
	preprocessing_time = models.DecimalField(max_digits=5, decimal_places=2)
	retrieval_time = models.DecimalField(max_digits=5, decimal_places=2)
	training_time = models.DecimalField(max_digits=5, decimal_places=2)
	recall_time = models.DecimalField(max_digits=5, decimal_places=2)

	def __unicode__(self):  # Python 3: def __str__(self):
		return self.question


