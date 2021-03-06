from django.db import models
from django.contrib import admin

from django.contrib.auth.models import User

# Create your models here.
class Card(models.Model):
	qualities = (
		(0, 'Обычная карта'),
		(1, 'Коллекционная карта'),
		(2, 'Уникальная карта'),
		(3, 'Золотая карта'),		
		(4, 'Памятная карта'),		
	)

	title = models.CharField('Название карточки', max_length = 32)
	icon = models.ImageField(upload_to='cards/', verbose_name='Обложка карточки')
	description = models.TextField('Описание карточки', blank = True)
	quality = models.IntegerField('Качество карточки', choices = qualities, default = 0)

	def __str__(self):
		name = self.title
		if self.quality == 3:
			name += " ★"
		return name

class CardAdmin(admin.ModelAdmin):
	list_display = ('title', 'quality', 'description')

class Booster(models.Model):
	title = models.CharField('Название бустера', max_length = 32)
	icon = models.ImageField(upload_to='boosters/', verbose_name='Название бустера', blank = True)
	cards = models.ManyToManyField(Card, verbose_name = 'Карточки')

	def __str__(self):
		return self.title

class BoosterAdmin(admin.ModelAdmin):
	filter_horizontal = ('cards', )
		
class Smile(models.Model):
	title = models.CharField('Название смайлика', max_length = 64)
	symbol = models.CharField('Обозначение смайлика', max_length = 32)
	icon = models.ImageField(upload_to='smiles/%Y/%m/%d/', verbose_name='Иконка смайлика', default='img/2015/08/04/ufo.jpg')

	def __str__(self):
		return self.title

class SmileCollection(models.Model):
	title = models.CharField('Название коллекции', max_length = 128)
	price_low = models.IntegerField('Цена за барахло')
	price_med = models.IntegerField('Цена за качественную вещь')
	price_high = models.IntegerField('Цена за дорогую вещь')
	smiles = models.ManyToManyField(Smile)
	icon = models.ImageField(upload_to='smiles/%Y/%m/%d/', verbose_name='Иконка набора смайликов', default='img/2015/08/04/ufo.jpg')

	def __str__(self):
		return self.title

class Background(models.Model):
	qualities = (
		(1, 'Стандартный фон'),
		(2, 'Редкий фон'),
		(3, 'Коллекционный фон')
	)

	title = models.CharField('Название фона', max_length = 128)
	background = models.ImageField(upload_to='background/%Y/%m/%d/', verbose_name='Фон', default='img/2015/08/04/ufo.jpg')
	quality = models.IntegerField('Частота', choices = qualities, default = 1)
	description = models.TextField('Описание фона', default = "Пусто")

	def __str__(self):
		return self.title

class BackgroundAdmin(admin.ModelAdmin):
	list_display = ('title', 'quality')

class Item(models.Model):
	title = models.CharField('Название фона', max_length = 128)
	icon = models.ImageField(upload_to='background/%Y/%m/%d/', verbose_name='Фон', default='img/2015/08/04/ufo.jpg')
	price_low = models.IntegerField('Цена за барахло')
	price_med = models.IntegerField('Цена за качественную вещь')
	price_high = models.IntegerField('Цена за дорогую вещь')
	no_sold = models.BooleanField('Не для продажи', default = False)

	def __str__(self):
		return self.title

class ItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'price_low', 'price_med', 'price_high')	

class ItemCollection(models.Model):
	title = models.CharField('Название коллекции', max_length = 64)
	items = models.ManyToManyField(Item)

	def __str__(self):
		return self.title

class UserInventoryItem(models.Model):
	types = (
		(1, 'Обычный предмет'),
		(2, 'Фон профиля'),
		(3, 'Набор смайликов'),
		)
	qualities = (
		(1, 'Низкое качество'),
		(2, 'Хорошее качество'),
		(3, 'Эксклюзивная вещь'),
		(4, 'Легендарное качество'),
		)

	user = models.ForeignKey(User)
	type = models.IntegerField('Тип предмета', choices = types)
	item_id = models.IntegerField('Идентификатор предмета')
	quality = models.IntegerField('Качество предмета', choices = qualities)
	get_date = models.DateTimeField('Дата получения предмета', auto_now = True)
	price = models.IntegerField('Цена за предмет')
	stolen = models.BooleanField('Вещь уже продана', default = False)
	#no_stolen = models.BooleanField('Вещь нельзя продавать', default = False, blank = True)

	def __str__(self):
		return '%s %s (%s / %s)' % (self.user, self.item_id, self.type, self.quality)

class UserInventoryItemAdmin(admin.ModelAdmin):
	list_display = ('type', 'item_id', 'user', 'quality', 'price', 'stolen')	

class Catapult(models.Model):
	from_user = models.ForeignKey(User, null=True, related_name='sender')
	to_user = models.ForeignKey(User, null=True, related_name='getter')
	item = models.ForeignKey(UserInventoryItem)
	view = models.BooleanField('Просмотрено', default = False)

class CatapultAdmin(admin.ModelAdmin):
	list_display = ('item', 'from_user', 'to_user')	

class Distribution(models.Model):
	title = models.CharField('Название раздачи', max_length = 64)
	user = models.ForeignKey(User)
	items = models.ManyToManyField(UserInventoryItem)
	view = models.BooleanField('Получено', default = False)