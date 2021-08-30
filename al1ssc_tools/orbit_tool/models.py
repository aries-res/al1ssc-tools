from django.db import models


class Body(models.Model):
    name = models.CharField(max_length=200, unique=True)
    body_id = models.IntegerField()
    color = models.CharField(max_length=200)
    plot_by_default = models.BooleanField(default=True)
    # TODO: Add a sort field (whose default value is pk)

    def __str__(self):
        """Show a meaningful represtation of model"""
        return self.name

    class Meta:
        verbose_name_plural = "bodies"
