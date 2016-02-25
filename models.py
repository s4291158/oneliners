from django.db import models


class Session(models.Model):
    key = models.CharField(max_length=40)

    def __str__(self):
        return str(self.id)


class Quote(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    context = models.CharField(max_length=255, blank=True, null=True)
    valid = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Like(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
