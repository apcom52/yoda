'''clear sky (01) -> ясно
few clouds (02) -> малооблачно
scattered clouds (03) -> облачно
broken clouds (04) -> тучи
shower rain (09) -> ливень
rain (10) - дождь
thunderstorm (11) - гроза
snow(13) - снег
mist(50) - туман'''
#Kirov ID = 548408

def get_weather_desc(code):
	weather = {
		"200":  'гроза со слабым дождём',
		"201":  'гроза с дождём',
		"202":  'гроза с проливным дождём',
		"210":  'слабая гроза',
		"211":  'гроза',
		"212":  'сильная гроза',
		"221":  'жестокая гроза',
		"230":  'гроза со слабым моросящим дождём',
		"231":  'гроза с моросящим дождём',
		"232":  'гроза с сильным моросящим дождём',
		"300":  'слабая морось',
		"301":  'морось',
		"302":  'сильная морось',
		"310":  'слабый моросящий дождь',
		"311":  'моросящий дождь',
		"312":  'сильный моросящий дождь',
		"313":  'ливень и изморось',
		"314":  'сильный ливень и изморось',
		"321":  'проливной моросящий дождь',
		"500":  'слабый дождь',
		"501":  'дождь',
		"502":  'сильный дождь',
		"503":  'очень сильный дождь',
		"504":  'очень сильный дождь',
		"511":  'ледяной дождь',
		"520":  'слабый проливной дождь',
		"521":  'проливной дождь',
		"522":  'сильный проливной дождь',
		"531":  'жестокий ливень',
		"600":  'небольшой снегопад',
		"601":  'снегопад',
		"602":  'сильный снегопад',
		"611":  'слякоть',
		"612":  'дождь и слякоть',
		"615":  'слабый дождь и снег',
		"616":  'дождь и снег',
		"620":  'слабый мокрый снег',
		"621":  'снегопад',
		"622":  'сильный мокрый снег',
		"701":  'туман',
		"711":  'смог',
		"721":  'дымка',
		"731":  'песчаная буря',
		"741":  'туманно',
		"751":  'песок',
		"761":  'пыль',
		"752":  'ВУЛКАНИЧЕСКИЙ ПЕПЕЛ',
		"771":  'ШКВАЛ',
		"781":  'ТОРНАДО',
		"800":  'ясно',
		"801":  'слегка облачно',
		"802":  'облачно',
		"803":  'пасмурно с прояснениями',
		"804":  'пасмурно',
		"900":  'торнадо',
		"901":  'тропический шторм',
		"902":  'ураган',
		"903":  'мороз',
		"904":  'жара',
		"905":  'ветренно',
		"906":  'град',
		"951":  'Штиль',
		"952":  'Тихий ветер',
		"953":  'Легкий ветер',
		"954":  'Слабый ветер',
		"955":  'Умеренный ветер',
		"956":  'Свежий ветер',
		"957":  'Сильный ветер',
		"958":  'Крепкий ветер',
		"959":  'Очень крепкий',
		"960":  'Шторм',
		"961":  'Сильный шторм',
		"962":  'Жестокий шторм',
	}
	return weather[code]

def get_weather_icon(code):
	icons = {
		'800-801': 'A',
		'801-802': 'C',
		'803-804': 'D',
		'300-301-302-310-311-500': 'F',
		'312-313-321-501-502-520': 'R',
		'314-503-504-511-521-522-531': 'S',
		'210-211-212-221': 'T',
		'201-230-231': 'U',
		'202-232': 'V',
		'600-601-602-621': 'W',
		'611-612-615-616-620-622': 'X',
		'952-953-954': 'N',
		'955-956-957-958': 'Z',
		'959-960': 'a',
		'752-771-781': 'e',
	}

	keys = icons.keys()
	for k in keys:
		if str(code) in k:
			return icons[k]