from django.core.exceptions import ObjectDoesNotExist
from .models import *
from timetable.utils import sendNotification
import random
import math

class Empire():
	PLAIN = "plain"
	SAND = "sand"
	SEA = "sea"
	MOUNTAIN = "mountain"

	RESOURCE_STONE = "stone";
	RESOURCE_WOOD = "wood";
	RESOURCE_SANDS = "sands";
	RESOURCE_IRON = "iron";
	RESOURCE_CARBON = "carbon";
	RESOURCE_OIL = "oil";
	RESOURCE_URAN = "uran";
	RESOURCE_CHANCE = 0.25

	RESOURCE_WHEAT = "wheat";
	RESOURCE_GRAPES = "grapes";
	RESOURCE_CITRUS = "citrus";
	RESOURCE_PLANT_CHANCE = [0.26, 0.32]

	RESOURCE_FISH = "fish";

	BUILDING_CASTLE1 = "castle1";
	BUILDING_HOMES = [27, 35]

	DOGMAT_1_TOURISMGOLD = 1
	DOGMAT_1_HOUSE = 2
	DOGMAT_1_GRANARY = 3
	DOGMAT_1_SILVERGOLD = 4
	DOGMAT_1_FAITHTOURISM = 5
	DOGMAT_1_RANDOMWONDER = 6
	DOGMAT_1_CULTURETOURISM = 7
	DOGMAT_1_WOODOIL = 8
	
	DOGMAT_2_WONDERPRODUCTION = 9
	DOGMAT_2_PLANTATIONGOLD = 10
	DOGMAT_2_CASTLEUPGRADE = 11
	DOGMAT_2_SCIENCE = 12
	DOGMAT_2_RESOURCEPRODUCTION = 13
	DOGMAT_2_HAPPINESS = 14
	DOGMAT_2_MARKETRADIO = 15
	
	DOGMAT_3_TOURISTS = 16
	DOGMAT_3_PLANTATIONFOOD = 17
	DOGMAT_3_CASTLEPRODUCTION = 18
	DOGMAT_3_FAITHSANDS = 19
	DOGMAT_3_GOLD25 = 20
	DOGMAT_3_WONDERCULTURE = 21

	STONE_RESOURCE_CHANCE = {
		"from": 0,
		"to": 0.2
	}

	SAND_RESOURCE_CHANCE = {
		"from": 0.2,
		"to": 0.38
	}

	WOOD_RESOURCE_CHANCE = {
		"from": 0.38,
		"to": 0.54
	}

	IRON_RESOURCE_CHANCE = {
		"from": 0.54,
		"to": 0.67
	}

	CARBON_RESOURCE_CHANCE = {
		"from": 0.67,
		"to": 0.78
	}

	ALUMINIUM_RESOURCE_CHANCE = {
		"from": 0.78,
		"to": 0.87
	}

	OIL_RESOURCE_CHANCE = {
		"from": 0.87,
		"to": 0.95
	}

	URAN_RESOURCE_CHANCE = {
		"from": 0.95,
		"to": 1
	}

	GRAPES_RESOURCE_CHANCE = {
		"from": 0,
		"to": 0.15
	}

	CITRUS_RESOURCE_CHANCE = {
		"from": 0.15,
		"to": 0.31
	}

	BANANES_RESOURCE_CHANCE = {
		"from": 0.31,
		"to": 0.62
	}

	COTTON_RESOURCE_CHANCE = {
		"from": 0.62,
		"to": 0.8
	}

	WHEAT_RESOURCE_CHANCE = {
		"from": 0.8,
		"to": 1
	}

	RUSSIA = 1
	USA = 2
	CHINA = 3
	JAPAN = 4
	ITALY = 5
	FRANCE = 6
	UK = 7
	THAILAND = 8
	INDIA = 9
	BRAZIL = 10
	GERMANY = 11
	SWEDEN = 12
	SPAIN = 13
	ISRAEL = 14
	AUSTRALIA = 15

	#Спецспособности стран
	
	# Россия:
	# +25% к добыче всех ресурсов
	RUSSIA_POWER = 1.25

	# США:
	# +10% к науке
	# +1 к науке за ратушу, стоящую рядом с горой
	USA_POWER = 1.1
	USA_CASTLE_SC_BONUS = 1

	# Китай:
	# +10% к производству
	# Шанс в 50% после строительства здания получить 1-2 очка веры, производства или науки
	CHINA_POWER = 1.1
	CHINA_BONUS_CHANCE = 0.5

	# Франция
	# Шанс в 40%, что возместит 50% стоимости здания золотом
	FRANCE_POWER_CHANCE = 0.4
	FRANCE_POWER_BONUS = 0.5

	# Япония:
	# +10% к культуре
	JAPAN_BONUS = 1.1

	# Бразилия
	# 7 клеток при новом уровне культуры
	BRAZIL_BONUS = 7

	# Таиланд
	# +1 золота за каждого туриста
	# +5% туристического влияния на страны
	THAILAND_BONUS = 1
	THAILAND_BASE_TOURISM_BONUS = 5

	# Швеция
	SWEDEN_CULTURE_CITIZENS = 1

	# Германия
	GERMANY_BONUS = 0.25

	# Индия
	INDIA_BONUS = 0.2

	# Уникальные здания
	BUILDING_CASTLE = Building.objects.get(name = "Ратуша")
	BUILDING_SCHOOL = Building.objects.get(name = "Школа")
	BUILDING_GRANARY = Building.objects.get(name = "Амбар")
	BUILDING_FORGE = Building.objects.get(name = "Кузница")
	BUILDING_WORKSHOP = Building.objects.get(name = "Мастерская")
	BUILDING_FACTORY = Building.objects.get(name = "Фабрика")
	BUILDING_WORKS = Building.objects.get(name = "Завод")
	BUILDING_COINHOUSE = Building.objects.get(name = "Монетный двор")
	
	BUILDING_FARM = Building.objects.get(name = "Ферма")
	BUILDING_PLANTATION = Building.objects.get(name = "Плантация")
	BUILDING_MINE = Building.objects.get(name = "Рудник")
	BUILDING_BOAT = Building.objects.get(name = "Лодка")


class Map():
	cells = [[0 for x in range(32)] for y in range(32)]
	width = 32
	height = 32
	cell_append = 5

	def __init__(self, nation):
		if nation:
			self.nation = nation

	def get(self, game):
		self.cells = eval(game.gmap)
		return self.cells

	def new_territories(self, game):
		if game.nation.id == Empire.BRAZIL:
			self.cell_append = Empire.BRAZIL_BONUS
		cells = self.get(game)
		bounds = self.get_bounds(game)
		
		# Если дырок нет, или их мало, то увеличивает радиус поиска
		holes = self.terr_holes(bounds, cells)
		print('holes', holes)
		print(bounds)
		while holes < self.cell_append:
			if bounds['x1'] > 0: bounds['x1'] -= 1
			if bounds['y1'] > 0: bounds['y1'] -= 1
			if bounds['x2'] < 32: bounds['x2'] += 1
			if bounds['y2'] < 32: bounds['y2'] += 1		
			holes =	self.terr_holes(bounds, cells)
			print(bounds)
			print('holes', holes)
		print('final', bounds)
		cells = self.open_holes(bounds, cells, self.cell_append)
		return cells

	def open_holes(self, bounds, cells, count):
		for hole in range(0, count):
			i = bounds['y1']
			j = bounds['x1']
			while cells[i][j]['visible']:
				i = random.choice(range(bounds['y1'], bounds['y2']))
				j = random.choice(range(bounds['x1'], bounds['x2']))
			cells[i][j]['visible'] = True
			print(i, j)
		return cells


	def terr_holes(self, bounds, cells):
		x = bounds['x1']
		y = bounds['y1']
		width = bounds['x2'] - bounds['x1']
		height = bounds['y2'] - bounds['y1']
		holes = 0
		for i in range(y, y + height):
			for j in range(x, x + width):
				if cells[i][j]['visible'] == False:
					holes += 1
		return holes

	def get_bounds(self, game):
		cells = eval(game.gmap)

		visible_bounds = {
			'x1': 32,
			'y1': 32,
			'x2': 0,
			'y2': 0,
		}

		for i in range(0, 32):
			for j in range(0, 32):
				if cells[i][j]['visible']:
					if j < visible_bounds['x1']:
						visible_bounds['x1'] = j
					if i < visible_bounds['y1']:
						visible_bounds['y1'] = i
					if j > visible_bounds['x2']:
						visible_bounds['x2'] = j
					if i > visible_bounds['y2']:
						visible_bounds['y2'] = i

		return visible_bounds

		# for i in range(0, 32):
		# 	for j in range(0, 32):
		# 		if cells[i][j]['visible']:
		# 			visible_bounds['y1'] = i
		# 			break
		# 	if visible_bounds['y1']:
		# 		break

		# for j in range(0, 32):
		# 	for i in range(visible_bounds['y1'], 32):
		# 		if cells[i][j]['visible']:
		# 			visible_bounds['x1'] = j
		# 			break
		# 	if visible_bounds['x1']:
		# 		break		

		# # Ищем ширину
		# visible_bounds['x2'] = visible_bounds['x1']
		# for i in range(visible_bounds['y1'], 32):
		# 	for j in range(visible_bounds['x1'], 32):
		# 		if cells[i][j]['visible']:
		# 			if j > visible_bounds['x2']:
		# 				visible_bounds['y1'] = i

		# visible_bounds['y2'] = visible_bounds['y1']
		# for i in range(visible_bounds['y1'], 32):
		# 	hasCells = False
		# 	for j in range(visible_bounds['x1'], 32):
		# 		if cells[i][j]['visible']:
		# 			hasCells = True
		# 			break
		# 	if hasCells and i > visible_bounds['y2']:
		# 		visible_bounds['y2'] = i

		return visible_bounds


	def generate(self):
		import random
		cells = self.cells

		for i in range(0, self.height):
			for j in range(0, self.width):
				type, sprite = "", ""

				if i == 0 and j == 0:
					type = self.getRandomCell()
				else:
					if i == 0:
						rnd = random.random()
						if (rnd <= 0.15): type = cells[i][j-1]["type"]
						else: type = self.getRandomCell()
					else:
						if (j == 0):
							if (cells[i-1][j]["type"] == cells[i-1][j+1]["type"]):
								rnd = random.random()
								if (rnd <= 0.3): type = cells[i-1][j]["type"]
								else: type = self.getRandomCell();
							else:
								rnd = random.random();
								if (rnd <= 0.15): type = cells[i-1][j]["type"];
								elif (rnd > 0.15 and rnd <= 0.3): type = cells[i-1][j+1]["type"];
								else: type = self.getRandomCell();
						elif (j == self.width - 1):
							if (cells[i][j-1]["type"] == cells[i-1][j-1]["type"] == cells[i-1][j]["type"]):
								rnd = random.random()
								if (rnd <= 0.45): type = cells[i-1][j]["type"]
								else: type = self.getRandomCell()
							elif ((cells[i][j-1]["type"] == cells[i-1][j-1]["type"]) != cells[i-1][j]["type"]):
								rnd = random.random()
								if (rnd <= 0.3): type = cells[i][j-1]["type"]
								elif (rnd > 0.3 and rnd <= 0.45): type = cells[i-1][j]["type"]
								else: type = self.getRandomCell()
							elif (cells[i][j-1]["type"] != (cells[i-1][j-1]["type"] == cells[i-1][j]["type"])):
								rnd = random.random()
								if (rnd <= 0.3): type = cells[i-1][j-1]["type"]
								elif (rnd > 0.3 and rnd <= 0.45): type = cells[i][j-1]["type"]
								else: type = self.getRandomCell()
							elif (cells[i-1][j-1]["type"] != (cells[i][j-1]["type"] == cells[i-1][j]["type"])):
								rnd = random.random()
								if (rnd <= 0.3): type = cells[i-1][j]["type"]
								elif (rnd > 0.3 and rnd <= 0.45): type = cells[i-1][j-1]["type"]
								else: type = self.getRandomCell()
							else:
								rnd = random.random();
								if (rnd <= 0.15): type = cells[i][j-1]["type"];
								elif (rnd > 0.15 and rnd <= 0.3): type = cells[i-1][j-1]["type"]
								elif (rnd > 0.3 and rnd <= 0.45): type = cells[i-1][j]["type"]
								else: type = self.getRandomCell()							
						else: 
							if (cells[i][j-1]["type"] == cells[i-1][j-1]["type"] == cells[i-1][j]["type"] == cells[i-1][j+1]["type"]): 
								rnd = random.random()
								if (rnd <= 0.6): type = cells[i-1][j]["type"]
								else: type = self.getRandomCell()
							elif ((cells[i-1][j-1]["type"] == cells[i][j-1]["type"] == cells[i-1][j]["type"]) != cells[i-1][j+1]["type"]): 
								rnd = random.random()
								if (rnd <= 0.45): type = cells[i-1][j]["type"]
								elif (rnd > 0.45 and rnd <= 0.6): type = cells[i-1][j+1]["type"]
								else: type = self.getRandomCell()
							elif ((cells[i][j-1]["type"] == cells[i-1][j+1]["type"] == cells[i-1][j]["type"]) != cells[i-1][j-1]["type"]): 
								rnd = random.random()
								if (rnd <= 0.45): type = cells[i-1][j]["type"]
								elif (rnd > 0.45 and rnd <= 0.6): type = cells[i-1][j-1]["type"]
								else: type = self.getRandomCell()
							elif ((cells[i-1][j-1]["type"] == cells[i-1][j+1]["type"] == cells[i-1][j]["type"]) != cells[i][j-1]["type"]): 
								rnd = random.random()
								if (rnd <= 0.45): type = cells[i-1][j]["type"]
								elif (rnd > 0.45 and rnd <= 0.6): type = cells[i][j-1]["type"]
								else: type = self.getRandomCell()
							elif ((cells[i-1][j-1]["type"] == cells[i-1][j+1]["type"] == cells[i][j-1]["type"]) != cells[i-1][j]["type"]): 
								rnd = random.random()
								if (rnd <= 0.45): type = cells[i-1][j-1]["type"]
								elif (rnd > 0.45 and rnd <= 0.6): type = cells[i-1][j]["type"]
								else: type = self.getRandomCell();
							elif ((cells[i-1][j]["type"] == cells[i-1][j+1]["type"]) != cells[i][j-1]["type"] != cells[i-1][j-1]["type"]): 
								rnd = random.random()
								if (rnd <= 0.3): type = cells[i-1][j+1]["type"]
								elif (rnd > 0.3 and rnd <= 0.45): type = cells[i][j-1]["type"]
								elif (rnd > 0.45 and rnd <= 0.6): type = cells[i-1][j-1]["type"]
								else: type = self.getRandomCell()
							elif ((cells[i][j-1]["type"] == cells[i-1][j-1]["type"]) != cells[i-1][j]["type"] != cells[i-1][j+1]["type"]): 
								rnd = random.random()
								if (rnd <= 0.3): type = cells[i-1][j-1]["type"]
								elif (rnd > 0.3 and rnd <= 0.45): type = cells[i-1][j]["type"]
								elif (rnd > 0.45 and rnd <= 0.6): type = cells[i-1][j+1]["type"]
								else: type = self.getRandomCell()
							elif ((cells[i-1][j-1]["type"] == cells[i-1][j]["type"]) != cells[i][j-1]["type"] != cells[i-1][j+1]["type"]): 
								rnd = random.random()
								if (rnd <= 0.3): type = cells[i-1][j-1]["type"]
								elif (rnd > 0.3 and rnd <= 0.45): type = cells[i][j-1]["type"]
								elif (rnd > 0.45 and rnd <= 0.6): type = cells[i-1][j+1]["type"]
								else: type = self.getRandomCell()
							elif ((cells[i][j-1]["type"] == cells[i-1][j+1]["type"]) != cells[i-1][j-1]["type"] != cells[i-1][j]["type"]): 
								rnd = random.random()
								if (rnd <= 0.3): type = cells[i-1][j+1]["type"]
								elif (rnd > 0.3 and rnd <= 0.45): type = cells[i-1][j-1]["type"]
								elif (rnd > 0.45 and rnd <= 0.6): type = cells[i-1][j]["type"]
								else: type = self.getRandomCell()
							else: 
								rnd = random.random()
								if (rnd <= 0.15): type = cells[i][j-1]["type"]
								elif (rnd > 0.15 and rnd <= 0.3): type = cells[i-1][j-1]["type"]
								elif (rnd > 0.3 and rnd <= 0.45): type = cells[i-1][j]["type"]
								elif (rnd > 0.45 and rnd <= 0.6): type = cells[i-1][j+1]["type"]
								else: type = self.getRandomCell()	

				food = 0
				production = 0
				culture = 0
				faith = 0
				science = 0
				tourism = 0
				happiness = 0
				gold = 0

				sprite = type

				if type == Empire.PLAIN:
					food += 1

				if type == Empire.SAND:
					faith += 1

				if type == Empire.SEA:
					food += 1

				if type == Empire.MOUNTAIN:
					production += 1
					science += 1

				# Назначаем ресурсы
				# Вероятность стратегического ресурса - 17%
				# Редкого (рудник) - 8% и плантации - 9%
				hasResource = random.random()
				resource = ""

				resourceChance = Empire.RESOURCE_CHANCE

				if game.nation.id == Empire.AUSTRALIA:
					resourceChance += 0.1

				if hasResource <= 0.25:
					resourceQuality = random.random()
					if resourceQuality <= 0.65:
						# Шансы появления ресурсов:
						# Камень	20%
						# Песок		18%
						# Лес		16%
						# Железо 	13%
						# Уголь		11%
						# Алюминий 	9%
						# Нефть		8%
						# Уран		5%
						resourceRnd = random.random()
						if resourceRnd > Empire.STONE_RESOURCE_CHANCE["from"] and resourceRnd <= Empire.STONE_RESOURCE_CHANCE["to"]:
							if type in (Empire.PLAIN, Empire.SAND):
								resource = Empire.RESOURCE_STONE
								production += 1
								faith = 0
								food = 0
						elif resourceRnd > Empire.WOOD_RESOURCE_CHANCE["from"] and resourceRnd <= Empire.WOOD_RESOURCE_CHANCE["to"]:
							if type in (Empire.PLAIN,):
								resource = Empire.RESOURCE_WOOD
								production += 1
								faith = 0
								food = 1
						elif resourceRnd > Empire.IRON_RESOURCE_CHANCE["from"] and resourceRnd <= Empire.IRON_RESOURCE_CHANCE["to"]:
							if type in (Empire.PLAIN, Empire.SAND):
								resource = Empire.RESOURCE_IRON
								production += 1
								faith = 0
								food = 0
						elif resourceRnd > Empire.CARBON_RESOURCE_CHANCE["from"] and resourceRnd <= Empire.CARBON_RESOURCE_CHANCE["to"]:
							if type in (Empire.PLAIN,):
								resource = Empire.RESOURCE_CARBON
								production += 1
								faith = 0
								food = 0
						elif resourceRnd > Empire.OIL_RESOURCE_CHANCE["from"] and resourceRnd <= Empire.OIL_RESOURCE_CHANCE["to"]:
							if type in (Empire.PLAIN, Empire.SEA):
								resource = Empire.RESOURCE_OIL
								production += 1
								faith = 0
								food = 0
						elif resourceRnd > Empire.URAN_RESOURCE_CHANCE["from"] and resourceRnd <= Empire.URAN_RESOURCE_CHANCE["to"]:
							if type in (Empire.PLAIN, Empire.SAND):
								resource = Empire.RESOURCE_URAN
								production += 1
								faith = 0
								food = 0
						elif resourceRnd > Empire.SAND_RESOURCE_CHANCE["from"] and resourceRnd <= Empire.SAND_RESOURCE_CHANCE["to"]:
							if type in (Empire.SAND,):
								resource = Empire.RESOURCE_SANDS
								production += 1
								faith = 0
								food = 0
					else:
						resourceRnd = random.random()
						if resourceRnd > Empire.WHEAT_RESOURCE_CHANCE["from"] and resourceRnd <= Empire.WHEAT_RESOURCE_CHANCE["to"]:
							if type in (Empire.PLAIN,):
								resource = Empire.RESOURCE_WHEAT
								production = 0
								food = 2
						elif resourceRnd > Empire.GRAPES_RESOURCE_CHANCE["from"] and resourceRnd <= Empire.GRAPES_RESOURCE_CHANCE["to"]:
							if type in (Empire.PLAIN,):
								resource = Empire.RESOURCE_GRAPES
								production = 0
								food = 2
						elif resourceRnd > Empire.CITRUS_RESOURCE_CHANCE["from"] and resourceRnd <= Empire.CITRUS_RESOURCE_CHANCE["to"]:
							if type in (Empire.PLAIN,):
								resource = Empire.RESOURCE_CITRUS
								production = 0
								food = 2

				
				cells[i][j] = {
					'type': type,
					'sprite': sprite,
					'resource': resource,
					'building': '',
					'visible': False,
					'values': {
						'food': food,
						'production': production,
						'culture': culture,
						'faith': faith,
						'science': science,
						'tourism': tourism,
						'happiness': happiness,
						'gold': gold,
					},
					'position': {
						'x': j,
						'y': i,
					}
				}

		# Определяем стартовую позицию (карта 5х5)
		start_x, start_y = (random.choice(range(5, 25)), random.choice(range(5, 25)))
		while cells[start_y][start_x]["type"] in (Empire.SEA, Empire.MOUNTAIN):
			start_x, start_y = (random.choice(range(5, 25)), random.choice(range(5, 25)))

		for i in range(start_y - 3, start_y + 2):
			for j in range(start_x - 3, start_x + 2):
				cells[i][j]["visible"] = True
		self.cells = cells
		return self.cells

	def getRandomCell(self):
		import random
		rnd = random.random()
		if rnd <= 0.5: return Empire.PLAIN
		elif rnd > 0.5 and rnd <= 0.7: return Empire.SAND
		elif rnd > 0.75 and rnd <= 0.93: return Empire.SEA
		else: return Empire.MOUNTAIN

	def getNeighbour(self, x, y):
		cells = self.cells
		nbs = []
		coords = []

		if x == 0 and y == 0:
			coords = [[0, 1], [1, 0], [1, 1]]
		elif x == 31 and y == 31:
			coords = [[30, 30], [30, 31], [31, 30]]
		elif x == 31 and y == 0:
			coords = [[0, 30], [1, 30], [1, 31]]
		elif x == 0 and y == 31:
			coords = [[30, 0], [30, 1], [31, 1]]
		else:
			if x == 0:
				coords = [[y-1, x], [y-1, x+1], [y, x+1], [y+1, x], [y+1, x+1]]
			elif x == 31:
				coords = [[y-1, x-1], [y-1, x], [y, x-1], [y+1, x-1], [y+1, x]]
			elif y == 0:
				coords = [[y, x-1], [y, x+1], [y+1, x-1], [y+1, x], [y+1, x+1]]
			elif y == 31:
				coords = [[y-1, x-1], [y-1, x], [y-1, x+1], [y, x-1], [y, x+1]]
			else:
				coords = [[y-1, x-1], [y-1, x], [y-1, x+1], [y, x-1], [y, x+1], [y+1, x-1], [y+1, x], [y+1, x+1]]

		for c in coords:
			if cells[c[0]][c[1]]['type'] in (Empire.MOUNTAIN, Empire.SEA):
				nbs.append(cells[c[0]][c[1]]['type'])
		return nbs

class GameManager():
	def __init__(self):
		pass

	def check(self):
		from datetime import datetime, timezone
		from django.utils import timezone
		from timetable.utils import utc_to_local
		now = utc_to_local(timezone.now())

		actives_games = Game.objects.all().filter(is_completed = False)
		for game in actives_games:
			last_step = Step.objects.filter(game = game).latest('id')
			print(now, last_step.date)
			step_time = last_step.date
			time_delta = now - step_time
			print(time_delta)
			print(time_delta.seconds)

			delta_hours = math.floor(time_delta.seconds / 3600)
			print(delta_hours)
			if (delta_hours >= 1):
				for i in range(0, delta_hours):
					print('шаг #', i)
					self.step(game)

	def get_stats(self, game):
		science_pt = 0
		production_pt = 0
		faith_pt = 0
		gold_pt = 0
		food_pt = 0
		culture_pt = 0
		tourism_pt = 0
		happiness_pt = 0

		# Получаем список всех принятых догматов
		dogmats_list = UserDogmat.objects.all().filter(game = game)
		dogmats = [d.dogmat.id for d in dogmats_list]

		castle = UserBuild.objects.get(game = game, building__name = "Ратуша")
		mapManager = Map(game.nation)
		gmap = mapManager.get(game)
		castle_near = mapManager.getNeighbour(castle.x, castle.y)
		castle_cell = gmap[castle.y][castle.x]

		castle_production = 1 * game.castle_level
		castle_food = 2 + 1 * game.castle_level
		castle_science = 1 * game.castle_level
		castle_culture = 1 * game.castle_level
		castle_gold = 5 * game.castle_level
		castle_faith = 1 * game.castle_level

		# Догмат на +1 к показателям ратуши
		if Empire.DOGMAT_2_CASTLEUPGRADE in dogmats:
			castle_production += 1
			castle_food += 1
			castle_science += 1
			castle_culture += 1
			castle_faith += 1

		# Догмат на +1 pp/sp/fp/cp для каждого чуда света
		if Empire.DOGMAT_1_RANDOMWONDER in dogmats:
			user_wonders = UserBuild.objects.filter(game = game, completed = True, building__wonder = True).count()
			for i in range(0, user_wonders):
				rnd = random.random()
				if rnd <= 0.25:
					production_pt += 1
				elif rnd > 0.25 and rnd <= 0.5:
					science_pt += 1
				elif rnd > 0.55 and rnd <= 0.75:
					faith_pt += 1
				elif rnd > 0.75:
					culture_pt += 1

		if Empire.SEA in castle_near:
			castle_food += 1
		if Empire.MOUNTAIN in castle_near:
			castle_production += 1
		if castle_cell['type'] == Empire.PLAIN:
			castle_food += 1
		if castle_cell['type'] == Empire.SAND:
			castle_faith += 1
		if castle_cell['resource'] != '':
			castle_production += 1
			castle_food += 1

		if game.nation.id == Empire.SPAIN:
			castle_production *= 2
			castle_food *= 2
			castle_science *= 2
			castle_culture *= 2
			castle_gold *= 2
			castle_faith *= 2

		# +1 к производству для Австралии
		if game.nation.id == Empire.AUSTRALIA:
			castle_production += 1

		# +1 к культуре для Японии
		if game.nation.id == Empire.JAPAN:
			castle_culture += 1

		# +1 к науке для США
		if game.nation.id == Empire.JAPAN:
			castle_science += 1

		production_pt += castle_production
		science_pt += castle_science
		faith_pt += castle_faith
		gold_pt += castle_gold
		food_pt += castle_food
		culture_pt += castle_culture		

		# Получаем список жителей и координаты их работы
		citizens_count = Citizen.objects.filter(game = game).count()
		citizens_list = Citizen.objects.all().filter(game = game, free = False)
		citizens = [[c.x, c.y] for c in citizens_list]

		buildings_list = UserBuild.objects.filter(game = game, completed = True)
		buildings = []
		for b in buildings_list:
			coord = [b.x, b.y]
			if coord in citizens:
				buildings.append(b.building)

		# Россия: если обрабатывается клетка с ресурсом, то +1 к золоту
		if game.nation.id == Empire.RUSSIA:
			for c in citizens:
				if gmap[c[1]][c[0]]["resource"]:
					gold_pt += 1

		# ---------------------------
		#Считаем очки производства
		prod_bonuses = BuildingBonus.objects.filter(type = 2, building__in = buildings)

		for p in prod_bonuses:
			production_pt += p.value

		prod_mods = BuildingBonusModificator.objects.filter(type = 2, building__in = buildings)
		for p in prod_mods:
			production_pt *= 1 + p.value / 100
		if game.nation.id == Empire.CHINA:
			production_pt *= Empire.CHINA_POWER

		
		# ---------------------------
		#Считаем очки веры
		faith_bonuses = BuildingBonus.objects.filter(type = 4, building__in = buildings)

		for f in faith_bonuses:
			faith_pt += f.value
		faith_mods = BuildingBonusModificator.objects.filter(type = 4, building__in = buildings)
		for f in faith_mods:
			faith_pt *= 1 + f.value / 100
		
		# ---------------------------
		#Считаем очки золота
		gold_bonuses = BuildingBonus.objects.filter(type = 8, building__in = buildings)

		# +1-5 к золоту Израилю (за уровень ратуши)
		if game.nation.id == Empire.ISRAEL:
			gold_pt += game.castle_level

		for g in gold_bonuses:
			gold_pt += g.value
		gold_mods = BuildingBonusModificator.objects.filter(type = 8, building__in = buildings)
		for g in gold_mods:
			gold_pt *= 1 + g.value / 100

		
		# ---------------------------
		#Считаем очки науки
		science_bonuses = BuildingBonus.objects.filter(type = 5, building__in = buildings)
		for s in science_bonuses:
			science_pt += s.value

		if Empire.BUILDING_SCHOOL in buildings:
			science_pt += math.floor(1.0 * citizens_count / 10)

		if game.nation.id == Empire.USA:
			if Empire.MOUNTAIN in castle_near:
				science_pt += 1
		science_mods = BuildingBonusModificator.objects.filter(type = 5, building__in = buildings)
		for s in science_mods:
			science_pt *= 1 + s.value / 100

		# США: +10% к науке
		if game.nation.id == Empire.USA:
			science_pt *= Empire.USA_POWER

		
		# ---------------------------
		#Считаем очки культуры
		culture_bonuses = BuildingBonus.objects.filter(type = 3, building__in = buildings)

		for c in culture_bonuses:
			culture_pt += c.value
			if game.nation.id == Empire.JAPAN:
				happiness_pt += 1
		culture_mods = BuildingBonusModificator.objects.filter(type = 3, building__in = buildings)
		for c in culture_mods:
			culture_pt *= 1 + c.value / 100

		# Япония: +10% к культуре
		if game.nation.id == Empire.JAPAN:
			culture_pt *= Empire.JAPAN_BONUS	

		
		# ---------------------------
		# Считаем очки туризма
		tourism_bonuses = BuildingBonus.objects.filter(type = 7, building__in = buildings)
		for t in tourism_bonuses:
			tourism_pt += t.value

		# ---------------------------
		# Считаем очки настроения
		happiness_bonuses = BuildingBonus.objects.filter(type = 6, building__in = buildings)
		for h in happiness_bonuses:
			happiness_pt += h.value

		citizens = Citizen.objects.filter(game = game, free = False)
		free_citizens_count = Citizen.objects.filter(game = game, free = True).count()
		# Безработные граждане уменьшают настроение
		user_building = UserBuild.objects.filter(game = game, completed = True)
		happiness_pt -= free_citizens_count 
		for citizen in citizens:
			bad_buildings = [Empire.BUILDING_FORGE.id, Empire.BUILDING_WORKSHOP.id, Empire.BUILDING_FACTORY.id, Empire.BUILDING_WORKS.id]
			x = citizen.x
			y = citizen.y
			print(gmap[y][x])
			current = gmap[y][x]
			print(bad_buildings)
			if user_building.filter(x = x, y = y).exists():
				building = UserBuild.objects.get(game = game, completed = True, x = x, y = y)
				print(building.id)
				if building.building.id in bad_buildings:
					happiness_pt -= 1
					print('bad building')					
				else:
					happiness_pt += 1
					print('good building')
			else:
				if current["resource"]:
					happiness_pt -= 1
					print('bad resource')
				else:
					happiness_pt += 0
					print('neutral')

		# ---------------------------
		# Количество мест для жителей
		citizens_places = 3 + (game.castle_level - 1) * 2
		homes = UserBuild.objects.filter(id__in = Empire.BUILDING_HOMES)
		for home in homes:
			if home.id == Empire.BUILDING_HOMES[0]:
				citizens_places += 3
				if game.nation.id == Empire.INDIA:
					citizens_places += 2
			elif home.id == Empire.BUILDING_HOMES[1]:
				citizens_places += 15


		# ---------------------------
		# Пробегаемся по всем зданиям и вычитаем расходы на содержание
		user_build_list = UserBuild.objects.filter(game = game, completed = True)
		user_buildings_obj = [b.building for b in user_build_list]
		for build in user_buildings_obj:
			cost = build.cost
			if game.nation.id == Empire.ISRAEL:
				if cost > 0:
					cost -= 1
			gold_pt -= cost


		return {
			'production': production_pt,
			'faith': faith_pt,
			'gold': gold_pt,
			'science': science_pt,
			'food': food_pt,
			'culture': culture_pt,
			'tourism': tourism_pt,
			'places': citizens_places,
			'happiness': happiness_pt,
		}

	def step(self, game):
		import datetime
		print('Start step')
		last_step = Step.objects.filter(game = game).latest('id')
		
		# Полчаем список всех принятых догматов
		dogmats_list = UserDogmat.objects.all().filter(game = game)
		dogmats = [d.dogmat.id for d in dogmats_list]
		
		stats = self.get_stats(game)
		production_pt = stats['production']
		faith_pt = stats['faith']
		gold_pt = stats['gold']
		science_pt = stats['science']
		culture_pt = stats['culture']
		food_pt = stats['food']
		tourism_pt = stats['tourism']
		happiness_pt = stats['happiness']
		citizens_places = stats['places']		

		step = Step()
		step.game = game
		step.date = datetime.datetime.today()
		step.step = last_step.step + 1

		# step.science = science_pt
		# step.faith = faith_pt
		# step.production = production_pt

		game.faith += step.faith

		# Германия: +1 ед производства/науки от каждого безработного
		if game.nation.id == Empire.GERMANY:
			free_citizens = Citizen.objects.filter(game = game, free = True).count()
			for i in range(0, free_citizens):
				rnd = random.random()
				if rnd <= 0.5:
					production_pt += 1
				else:
					science_pt += 1

		# Швеция: +1 к культуре за каждых 10 жителей
		if game.nation.id == Empire.SWEDEN:
			citizens_count = Citizen.objects.filter(game = game).count()
			sweden_culture_bonus = 1 + citizens_count / Empire.SWEDEN_CULTURE_CITIZENS
			culture_pt += sweden_culture_bonus

		# Изучаем технологии
		try:
			current_tech = UserTeach.objects.all().filter(game = game, completed = False).latest('id')
		except ObjectDoesNotExist:
			current_tech = None

		if current_tech:
			current_sp = current_tech.progress + science_pt
			
			if current_sp >= current_tech.technology.sp:	
				from timetable.utils import sendNotification
				current_tech.progress = current_tech.technology.sp
				current_sp -= current_tech.technology.sp
				game.science = current_sp
				current_tech.completed = True

				game.user.userprofile.exp += 1
				game.user.save()

				sendNotification({
					"user": game.user,
					"title": "Технология изучена",
					"type": 1,
					"text": "Вы изучили технологию \"" + current_tech.technology.name + "\""
				})

			else:
				current_tech.progress = current_sp
				game.science = current_sp
				step.science = science_pt
			current_tech.save()
			game.save()
		

		#Строительство
		try:
			current_build = UserBuild.objects.all().filter(game = game, completed = False).latest('id')
		except ObjectDoesNotExist:
			current_build = None

		if game.nation.id == Empire.UK and current_build in [Empire.BUILDING_FARM, Empire.BUILDING_PLANTATION, Empire.BUILDING_MINE, Empire.BUILDING_BOAT]:
			current_build.completed = True
			current_build.save()

			game.user.userprofile.exp += 1
			game.user.save()

			sendNotification({
				"user": game.user,
				"title": "Здание построено",
				"type": 1,
				"text": "Завершено строительство здания \"" + current_build.building.name + "\""
			})
		else:	
			if current_build:
				current_prod = current_build.progress + production_pt
				
				if current_prod >= current_build.building.pp:
					from timetable.utils import sendNotification

					current_build.progress = current_build.building.pp
					current_prod -= current_build.building.pp
					game.production = current_prod
					current_build.completed = True

					#Если игрок - Китай, то получает 1-2 ед веры, производства или науки
					if game.nation.id == Empire.CHINA:
						rnd = random.random()
						if rnd < Empire.CHINA_BONUS_CHANCE:
							value = random.choice([1, 2])
							param = random.choice(('prod', 'science', 'faith'))
							if param == 'prod':
								game.production += value
								step.production += value
							elif param == 'science':
								game.science += value
								step.science += value
							elif param == 'faith':
								game.faith += value
								step.faith += value

					if game.nation.id == Empire.FRANCE:
						rnd = random.random()
						if rnd <= Empire.FRANCE_POWER_CHANCE:
							bonus_gold = current_build.pp * Empire.FRANCE_POWER_BONUS
							game.gold += bonus_gold
							step.gold += bonus_gold

					game.user.userprofile.exp += 1
					game.user.save()

					sendNotification({
						"user": game.user,
						"title": "Здание построено",
						"type": 1,
						"text": "Завершено строительство здания \"" + current_build.building.name + "\""
					})

				else:
					current_build.progress = current_prod
					game.production = current_prod
					step.production = production_pt
				current_build.save()
				game.save()

		# Считает культуру
		culture_level = game.culture_level
		culture_limit = culture_level * 15
		game.culture += culture_pt
		print('culture:', culture_limit)

		if game.culture >= culture_limit:
			from timetable.utils import sendNotification
			game.culture_level += 1
			game.culture -= culture_limit
			gmap = Map(game.nation)
			cells = gmap.new_territories(game)
			game.gmap = str(cells)

			if game.nation.id == Empire.JAPAN:
				gold_pt += 50

			sendNotification({
				"user": game.user,
				"title": "Новые территории",
				"type": 1,
				"text": "Ваша культура перешла на новый уровень и вы получили дополнительные территории"
			})
		step.culture += culture_pt

		# Подсчитываем количество еды и настроения
		citizens_count = Citizen.objects.filter(game = game).count()

		# Подсчитываем количество доступных мест для жителей
		citizens_base = 0.1 + 0.01 * happiness_pt
		if game.nation.id == Empire.INDIA:
			citizens_base += Empire.INDIA_BONUS
		if citizens_count < food_pt and citizens_count <= citizens_places:
			citizen_rnd = random.random()
			if citizen_rnd <= citizens_base:
				citizen = Citizen()
				citizen.game = game
				citizen.save()
				citizens_count += 1
		elif citizens_count > food_pt or citizens_count > citizens_places:
			last_citizen = Citizen.objects.all().filter(game = game).latest('id')
			last_citizen.delete()
			citizens_count -= 1
		step.citizens = citizens_count

		# Германия: все жители платят налог в размере 0,25 золота
		if game.nation.id == Empire.GERMANY:
			gold_pt += citizens_count * Empire.GERMANY_BONUS


		# Механика туризма
		base_tourism = 10
		if game.nation.id == Empire.THAILAND:
			base_tourism += Empire.THAILAND_BASE_TOURISM_BONUS
		base_tourism += tourism_pt
		tourist_count = 0
		all_empires = Game.objects.all().filter(is_completed = False).exclude(id = game.id)
		for empire in all_empires:
			# Получаем последнее количество культуры на ходу
			last_step = Step.objects.all().filter(game = empire).latest('id')
			empire_culture = last_step.culture
			diff = (base_tourism - empire_culture) * 0.01
			if diff > 0:
				# Получаем количество жителей
				citizen_count = Citizen.objects.filter(game = empire).count()
				for c in range(0, citizens_count):
					rnd = random.random()
					if rnd <= diff:
						tourist_count += 1

		# Догмат на то, что туристы иногда могут приносить очки fp/cp/sp
		if Empire.DOGMAT_3_TOURISTS in dogmats:
			for i in range(0, tourist_count):
				can_take = random.random()
				if can_take <= 0.5:		
					if rnd <= 0.33:
						faith_pt += 1
					elif rnd > 0.33 and rnd <= 0.66:
						culture_pt += 1
					elif rnd > 0.66:
						science_pt += 1

		if game.nation.id == Empire.THAILAND:
			gold_pt += (1 + Empire.THAILAND_BONUS) * tourist_count
		else:
			gold_pt += tourist_count

		step.tourism = tourism_pt
		step.tourist_count = tourist_count

		game.gold += gold_pt
		game.user.userprofile.gold += gold_pt
		game.user.save()
		game.save()

		step.gold += gold_pt
		step.save()