# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
import math
import json
import random

from game.models import *
from game.classes import *
from game.serializers import *

class TechnologiesList(APIView):
	def get(self, request, format = None):
		data = request.GET
		method = data.get("m", False)
		game = Game.objects.all().filter(user = request.user, is_completed = False).latest('id')

		if method == 'available_list':			
			available_techs = []
			completed_branches_list = UserTeach.objects.filter(game = game, completed = True)
			completed_branches = [t.technology for t in completed_branches_list]
			for branch in Technology.branches:
				branch_id = branch[0]
				current_tech = None
				for t in Technology.objects.all().filter(branch = branch_id):
					if not t in completed_branches:
						current_tech = t
						break
				if current_tech:
					available_techs.append(current_tech)		

			serializer = TechnologySerializer(available_techs, many = True)

			#Текущее исследование
			current = False
			try:
				current_tech = UserTeach.objects.filter(game = game, completed = False).latest('id')
				current = TechnologySerializer(current_tech.technology, many = False)
				current = current.data
				current["progress"] = 100 * game.science / current_tech.technology.sp
			except ObjectDoesNotExist:
				pass

			return Response({
				'available': serializer.data,
				'current': current,				
			})
		elif method == 'start':
			id = data.get("id", False)
			if id:
				technology = Technology.objects.get(pk = int(id))
				game = Game.objects.filter(user = request.user, is_completed = False).latest('id')
				userteach = UserTeach()
				userteach.login = request.user
				userteach.game = game
				userteach.technology = technology
				userteach.date_start = datetime.datetime.now()
				userteach.save()
				return Response("ok");
		return Response("failed")


class BuildingsList(APIView):
	def get(self, request, format = None):
		data = request.GET
		method = data.get("m", False)
		game = Game.objects.all().filter(user = request.user, is_completed = False).latest('id')
		nation = game.nation
		print(nation)

		if method == 'available_list':
			buildings = []
			# Каждый игрок может построить дом в любых количествах
			home_building = Building.objects.get(name = 'Дом')
			buildings.append(home_building)


			completed_branches_list = UserTeach.objects.filter(game = game, completed = True)
			builded = UserBuild.objects.filter(game = game, completed = True)
			completed_buildings = [b.building for b in builded]
			teached_buildings = []
			for branch in completed_branches_list:
				print(branch.technology.buildings.all())
				for build in branch.technology.buildings.all():
					if not build in completed_buildings and not build == home_building:
						#Если здание является общим или эксклюзивным для данной страны, то добавляем его в список
						if build.nations_id:
							if build.nations_id == nation.id:
								buildings.append(build)
						else:
							buildings.append(build)	

			serializer = BuildingSerializer(buildings, many = True)
			serializer_data = serializer.data

			# Получаем сведения о текущем проекте
			current = False
			try:
				current_build = UserBuild.objects.filter(game = game, completed = False).latest('id')
				current = BuildingSerializer(current_build.building, many = False)
				current = current.data
				current["progress"] = 100 * game.production / current_build.building.pp
			except ObjectDoesNotExist:
				pass

			# Если ратушу можно улучшить
			if self.canCastleUpgrade(game):
				castle = {}
				castle['id'] = Empire.BUILDING_CASTLE.id
				castle['name'] = "Ратуша (Улучшение до " + str(game.castle_level + 1) + "-го уровня)"
				castle['pp'] = (game.castle_level) * 100
				castle['icon'] = '/media/game/buildings/castle_' + str(game.castle_level + 1) + '.png'
				castle['bonus'] = [
					{
	                    "value": 1,
	                    "type": "culture"
	                },
	                {
	                    "value": 1,
	                    "type": "faith"
	                },
	                {
	                    "value": 1,
	                    "type": "science"
	                },
	                {
	                    "value": 1,
	                    "type": "production"
	                },
	                {
	                    "value": 1,
	                    "type": "food"
	                },
	                {
	                    "value": 5,
	                    "type": "gold"
	                }
				]
				serializer_data.insert(0, castle)

			return Response({
				"available": serializer_data,
				"current": current,			
			})
		elif method == 'build':
			building_id = data.get('id', False)
			game = Game.objects.all().filter(user = request.user, is_completed = False).latest('id')
			if building_id:
				building = Building.objects.get(pk = int(building_id))
				x = data.get('x', False)
				y = data.get('y', False)
				userbuild = UserBuild()
				userbuild.login = request.user
				userbuild.game = game
				userbuild.building = building
				userbuild.date_start = datetime.datetime.now()
				userbuild.x = x
				userbuild.y = y
				userbuild.save()

				return Response('ok')
			return Response('failed')
		return Response('failed')


	def getBuildingInfo(self, building):
		bonuses = []
		for bonus in BuildingBonus.objects.filter(building = building):
			bonuses.append({
				"value": bonus.value,
				"type": self.getBonusName(bonus.type)
			})
		for bonus in BuildingBonusModificator.objects.filter(building = building):
			bonuses.append({
				"value": bonus.value + "%",
				"type": self.getBonusName(bonus.type)
			})
		return {
			"title": building.name,
			"cost": building.pp,
			# "icon": building.icon,
			"bonus": bonuses,
		}

	def getBonusName(self, type):
		types = ["food", "production", "culture", "faith", "science", "happiness", "tourism", "gold"]
		return types[type - 1]

	def canCastleUpgrade(self, game):
		technologies_bonuses_list = TechnologyBonus.objects.all().filter(bonus = 'Улучшение ратуши')
		technologies = [t.technology for t in technologies_bonuses_list]

		max_castle_level = 1

		my_technologies = UserTeach.objects.all().filter(game = game, completed = True)
		for t in my_technologies:
			if t.technology in technologies:
				max_castle_level += 1
		if max_castle_level > game.castle_level:
			return True
		return False



class DogmatAPI(APIView):
	def get(self, request, format = None):
		data = request.GET
		method = data.get("m", False)
		game = Game.objects.all().filter(user = request.user, is_completed = False).latest('id')
		my_dogmats = UserDogmat.objects.all().filter(game = game)
		if method == "list":
			level = int(data.get("level", 0))
			limit = 5 - level

			my_dogmats_list = UserDogmat.objects.filter(game = game)
			my_dogmats = [d.dogmat.id for d in my_dogmats_list]
			print(my_dogmats)

			dogmats_list = Dogma.objects.all().filter(level = level).exclude(id__in = my_dogmats).order_by('?')[:limit]
			serializer = DogmatSerializer(dogmats_list, many = True)
			return Response(serializer.data)

		elif method == "my_dogmats":
			dogmats = [{
				"level": 1,
				"class": "first",
				"price": 300,
				"dogmats": []
			}, {
				"level": 2,
				"class": "second",
				"price": 700,
				"dogmats": []
			}, {
				"level": 3,
				"class": "third",
				"price": 1500,
				"dogmats": []
			}]
			dogmats_list = UserDogmat.objects.filter(game = game)
			for d in dogmats_list:
				dogmat = d.dogmat
				dogmats[dogmat.level - 1]["dogmats"].append({
					"content": dogmat.content,
					"level": dogmat.level,
				})

			for i in range(0, 3):
				delta = (6 - i) - len(dogmats[i]["dogmats"])
				for j in range(0, delta):
					dogmats[i]["dogmats"].append({
						"locked": True,
					})
			return Response(dogmats)
		return Response('failed')

class MapAPI(APIView):
	def get(self, request, format = None):
		from game.classes import Map

		data = request.GET
		method = data.get("m", False)

		if method == "generate":			
			gamemap = Map("RU")		
			game = Game.objects.get(user = request.user, is_completed = False)
			game.gmap = str(gamemap.generate())
			game.save()
			return Response(game.gmap)
		elif method == "get":
			game = Game.objects.get(user = request.user, is_completed = False)
			gmap = eval(game.gmap)

			#Получаем список всех зданий
			buildings = UserBuild.objects.filter(login = request.user, game = game)
			for b in buildings:
				progress = 1
				if b.completed == False:
					full_price = b.building.pp
					current_price = b.progress
					progress = 1.0 * current_price / full_price
				serializer = BuildingSerializer(b.building, many = False)
				(gmap[b.y][b.x])["building"] = serializer.data
				(gmap[b.y][b.x])["building"]["progress"] = progress

				if (gmap[b.y][b.x])["building"]["name"] == 'Ратуша':
					(gmap[b.y][b.x])["building"]["sprite"] = "castle" + str(game.castle_level)

			# Получаем список всех жителей
			citizens = Citizen.objects.filter(game = game, free = False)
			citizens_array = [[c.x, c.y] for c in citizens]
			for i in range(0, 32):
				for j in range(0, 32):
					if [j, i] in citizens_array:
						gmap[i][j]['citizen'] = True
					else:
						gmap[i][j]['citizen'] = False

					food = 0
					production = 0
					gold = 0
					culture = 0
					science = 0
					faith = 0
					tourism = 0

					# Добавляем подсказку
					cell_type = gmap[i][j]['type']
					land_type = 'Равнина'
					resource_type = False


					if cell_type == Empire.PLAIN:
						food = 1
					if cell_type == Empire.SAND:
						land_type = 'Пустыня'
						faith = 1
					elif cell_type == Empire.SEA:
						land_type = 'Море'
						food = 1
					elif cell_type == Empire.MOUNTAIN:
						land_type = 'Горы'
						science = 1
						production = 1

					# Определяем вид ресурса
					cell_resource = gmap[i][j]['resource']
					if cell_resource == Empire.RESOURCE_STONE:
						resource_type = 'Камень'
					if cell_resource == Empire.RESOURCE_WOOD:
						resource_type = 'Дерево'
					if cell_resource == Empire.RESOURCE_SANDS:
						resource_type = 'Песок'
					if cell_resource == Empire.RESOURCE_IRON:
						resource_type = 'Железо'
					if cell_resource == Empire.RESOURCE_CARBON:
						resource_type = 'Уголь'
					if cell_resource == Empire.RESOURCE_OIL:
						resource_type = 'Нефть'
					if cell_resource == Empire.RESOURCE_URAN:
						resource_type = 'Уран'
					if cell_resource == Empire.RESOURCE_WHEAT:
						resource_type = 'Пшеница'
					if cell_resource == Empire.RESOURCE_GRAPES:
						resource_type = 'Виноград'
					if cell_resource == Empire.RESOURCE_CITRUS:
						resource_type = 'Цитрусовые'
					if cell_resource == Empire.RESOURCE_FISH:
						resource_type = 'Рыба'

					tooltip_building = False
					if gmap[i][j]["building"] != "":
						tooltip_building = gmap[i][j]["building"]["name"]
						food, faith, science, production = (0,0,0,0)
						for bonus in gmap[i][j]["building"]["bonus"]:
							if bonus["type"] == "food":
								food += bonus["value"]
							elif bonus["type"] == "production":
								production += bonus["value"]
							elif bonus["type"] == "culture":
								culture += bonus["value"]
							elif bonus["type"] == "faith":
								faith += bonus["value"]
							elif bonus["type"] == "science":
								science += bonus["value"]
							elif bonus["type"] == "tourism":
								tourism += bonus["value"]
							elif bonus["type"] == "gold":
								gold += bonus["value"]


					resources = []
					if food > 0:
						resources.append({
							"icon": "food",
							"value": food,
						})
					if production > 0:
						resources.append({
							"icon": "production",
							"value": production,
						})
					if culture > 0:
						resources.append({
							"icon": "culture",
							"value": culture,
						})
					if science > 0:
						resources.append({
							"icon": "science",
							"value": science,
						})
					if faith > 0:
						resources.append({
							"icon": "faith",
							"value": faith,
						})
					if gold > 0:
						resources.append({
							"icon": "gold",
							"value": gold,
						})
					if tourism > 0:
						resources.append({
							"icon": "tourism",
							"value": tourism,
						})
					
					gmap[i][j]['tooltip'] = {
						"land": land_type,
						"building": tooltip_building,
						"resources": resources,
						"resource_type": resource_type,
					}

			return Response(gmap)

		elif method == "citizens":
			game = Game.objects.get(user = request.user, is_completed = False)
			citizens = Citizen.objects.all().filter(game = game, free = False)
			coordinates = []
			for c in citizens:
				coordinates.append({
					"x": c.x,
					"y": c.y,
				})
			return Response(coordinates)			
		elif method == "save":
			new_map = data.get("map", False)
			if new_map:
				game = Game.objects.get(user = request.user, is_completed = False)
			else:
				nation = data.get("nation", False)
				if nation:				
					country = Nation.objects.get(pk = int(nation))	
					print(country)
					gamemap = Map("RU")
					game = Game()
					game.nation = country
					mapobj = Map(country)
					gamemap = mapobj.generate()
					game.gmap = json.dumps(gamemap)
					game.save()
				return Response(gamemap.generate())
		elif method == "bounds":
			game = Game.objects.get(user = request.user, is_completed = False)
			gmap = Map(game.nation)
			return Response(gmap.get_bounds(game))
		elif method == "culture":
			game = Game.objects.get(user = request.user, is_completed = False)
			gmap = Map(game.nation)
			cells = gmap.new_territories(game)
			game.gmap = str(cells)
			game.save()
			return Response('ok')
		elif method == "citizens_cells":
			game = Game.objects.get(user = request.user, is_completed = False)
			gmap = Map(game.nation)
			bounds = gmap.get_bounds(game)

			citizens = Citizen.objects.filter(game = game, free = False).order_by('y').order_by('x')
			citizens_array = [[c.x, c.y] for c in citizens]
			print(citizens_array)
			citizens_cells = [[0 for x in range(bounds['x2'] - bounds['x1'] + 1)] for y in range(bounds['y2'] - bounds['y1'] + 1)]
			for i in range(0, bounds['y2'] - bounds['y1'] + 1):
				for j in range(0, bounds['x2'] - bounds['x1'] + 1):
					print('check', [j + bounds['x1'], i + bounds['y1']])
					if [j + bounds['x1'], i + bounds['y1']] in citizens_array:
						citizens_cells[i][j] = True
					else:
						citizens_cells[i][j] = False
			return Response(citizens_cells)
		elif method == "citizen_set":
			game = Game.objects.get(user = request.user, is_completed = False)
			x = int(data.get("x", False))
			y = int(data.get("y", False))
			data_status = data.get("status", False)
			if data_status == "false":
				status = False
			else:
				status = True
			print(x, y, status)

			if status == False:
				citizen = Citizen.objects.filter(game = game, x = x, y = y).latest('id')
				citizen.x = 0
				citizen.y = 0
				citizen.free = True
				citizen.save()
				return Response("ok")
				print('false status')
			elif status == True:
				try:
					citizen = Citizen.objects.filter(game = game, free = True).latest('id')
					citizen.x = x
					citizen.y = y
					citizen.free = False
					citizen.save()
					return Response("ok")
					print('true status')
				except ObjectDoesNotExist:
					return Response('failed')			
			return Response("failed")
		elif method == "free_citizens":
			game = Game.objects.get(user = request.user, is_completed = False)
			citizens_count = Citizen.objects.filter(game = game, free = True).count()

			full_count_citizens = Citizen.objects.filter(game = game).count()

			places = 0
			gm = GameManager()
			stats = gm.get_stats(game)
			places = stats['places']

			return Response({
				"free": citizens_count,
				"count": full_count_citizens,
				"places": places,
			})

class StatsAPI(APIView):
	def get(self, request, format = None):
		from game.classes import Map

		data = request.GET
		method = data.get("m", False)
		game = Game.objects.all().filter(user = request.user, is_completed = False).latest('id')

		if method == "stats":
			gm = GameManager()
			stats = gm.get_stats(game)
			current_stats = {
				"gold": round(request.user.userprofile.gold, 1),
				"production": round(game.production, 1),
				"science": round(game.science, 1),
				"faith": round(game.faith, 1),
				"food": round(game.food, 1),
				"culture": round(game.culture, 1),
				"culture_next": game.culture_level * 15,
			}
			return Response({
				"current": current_stats,
				"step": stats
			})

		if method == "data":			
			production_data = []
			food_data = []
			faith_data = []
			culture_data = []
			gold_data = []

			latest_steps = Step.objects.all().filter(game = game).order_by('-id')[:48]

			for step in latest_steps:
				production_data.append(round(step.production, 1))
				food_data.append(round(step.food, 1))
				faith_data.append(round(step.faith, 1))
				culture_data.append(round(step.culture, 1))
				gold_data.append(round(step.gold, 1))


			production = {
				"text": "Производство",
				"legend-text": "Производство",
				"line-color":"#ffa500",
				"marker": {
					"size": 2,
				},
				"values": production_data
			}
			food = {
				"text": "Еда",
				"legend-text": "Еда",
				"borderColor": "#66ff66",
				"line-color":"#66ff66",
				"marker": {
					"size": 2,
				},
				"values": food_data
			}
			faith = {
				"text": "Вера",
				"legend-text": "Вера",
				"borderColor": "#bbbbbb",
				"line-color":"#bbbbbb",
				"marker": {
					"size": 2,
				},
				"values": faith_data
			}
			culture = {
				"text": "Культура",
				"legend-text": "Культура",
				"borderColor": "#8b00ff",
				"line-color":"#8b00ff",
				"marker": {
					"size": 2,
				},
				"values": culture_data
			}
			gold = {
				"text": "Золото",
				"legend-text": "Золото",
				"borderColor": "#ffff00",
				"line-color":"#ffff00",
				"marker": {
					"size": 2,
				},
				"values": gold_data
			}
			return Response([production, food, faith, culture, gold]) #, food, faith, culture, gold])

		if method == "population":			
			citizens_data = []

			latest_steps = reversed(Step.objects.all().filter(game = game).order_by('-id')[:50])

			for step in latest_steps:
				citizens_data.append(step.citizens)

			return Response([{
				"text": "Население",
				"legend-text": "Население",
				"line-color":"#00ff00",
				"marker": {
					"size": 2,
				},
				"values": citizens_data
			}])

		if method == "nations":
			nations = Nation.objects.all()
			games = Game.objects.all().filter(is_completed = False)

			nation_response = []

			for nation in nations:
				unique_building = Building.objects.get(nations = nation)
				serializer = BuildingSerializer(unique_building, many = False)
				is_locked = False

				if games.filter(nation = nation).exists():
					is_locked = True

				nation_response.append({
					"id": nation.id,
					"title": nation.title,
					"icon": nation.icon.url,
					"bonus": nation.bonus,
					"building": serializer.data,
					"is_locked": is_locked,
				})

			return Response(nation_response)