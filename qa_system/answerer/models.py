from django.db import models



class Document(models.Model):
	content_txt = models.TextField()
	link = models.CharField(max_length=512)
	to_result = models.ForeignKey('Results', on_delete=models.CASCADE)
	automatic_ranking = models.IntegerField()
	supervised_ranking = models.IntegerField()

	def __unicode__(self):  # Python 3: def __str__(self):
		return str(self.link) + "|" + str(self.supervised_ranking)

	

class Results(models.Model):
	question = models.TextField()
	training_algorithm = models.CharField(max_length=2)
	supervised_answer = models.IntegerField()
	expanded_vocabulary = models.BooleanField()
	iterations = models.IntegerField()
	to_success_answer = models.ForeignKey('Document', blank=True, null=True)
	preprocessing_time = models.DecimalField(max_digits=5, decimal_places=2)
	retrieval_time = models.DecimalField(max_digits=5, decimal_places=2)
	training_time = models.DecimalField(max_digits=5, decimal_places=2)
	recall_time = models.DecimalField(max_digits=5, decimal_places=2)

	def __unicode__(self):  # Python 3: def __str__(self):
		return self.question

