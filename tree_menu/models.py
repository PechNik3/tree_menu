from django.db import models
from django.urls import reverse, NoReverseMatch


class MenuItem(models.Model):
    menu_name = models.CharField(max_length=100, db_index=True)
    title = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.CASCADE
    )
    explicit_url = models.CharField(
        max_length=500, blank=True, help_text='Прямой URL, например /about/'
    )
    named_url = models.CharField(
        max_length=200, blank=True, help_text='Имя url (reverse name), например app:detail'
    )
    order = models.IntegerField(default=0, db_index=True)

    class Meta:
        unique_together = ('menu_name', 'title', 'parent')
        ordering = ('order', 'id')

    def __str__(self):
        return f'{self.menu_name} — {self.title}'

    @property
    def resolved_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return None
        if self.explicit_url:
            return self.explicit_url
        return None
