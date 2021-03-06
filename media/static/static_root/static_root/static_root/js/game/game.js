//Build 100 - 09.04.16
WebFontConfig = {
	google: { families: [ 'Neucha::latin,cyrillic' ] }
};

var game = new Phaser.Game(1024, 768, Phaser.WEBGL, 'game', {
	init: init,
	preload: preload,
	create: create,
	update: update,
	render: render,
});

function init() {
	game.kineticScrolling = game.plugins.add(Phaser.Plugin.KineticScrolling);
}

function preload() {
	game.stage.backgroundColor = '#000000';
	game.time.advancedTiming = true;

	game.load.image('loading-screen', '/media/game/loading_screen.jpg');
	game.load.script('webfont', 'https://ajax.googleapis.com/ajax/libs/webfont/1/webfont.js');

	game.load.image('food', '/media/game/icons/food.png');
	game.load.image('production', '/media/game/icons/production.png');
	game.load.image('culture', '/media/game/icons/culture.png');
	game.load.image('faith', '/media/game/icons/faith.png');
	game.load.image('science', '/media/game/icons/science.png');

	game.load.image('plain', '/media/game/grass.png');
	game.load.image('sand', '/media/game/sand.png');
	game.load.image('mountain', '/media/game/mountains.png');
	
	game.load.image('sea', '/media/game/water.png');
	game.load.image('seaE', '/media/game/waterE.png');
	game.load.image('seaW', '/media/game/waterW.png');
	game.load.image('seaS', '/media/game/waterS.png');
	game.load.image('seaN', '/media/game/waterN.png');
	game.load.image('seaEWNS', '/media/game/waterEWNS.png');
	game.load.image('seaE', '/media/game/waterE.png');
	game.load.image('seaW', '/media/game/waterW.png');
	game.load.image('seaN', '/media/game/waterN.png');
	game.load.image('seaS', '/media/game/waterS.png');
	game.load.image('seaEW', '/media/game/waterEW.png');
	game.load.image('seaNS', '/media/game/waterNS.png');
	game.load.image('sea_W', '/media/game/water_W.png');
	game.load.image('sea_E', '/media/game/water_E.png');
	game.load.image('sea_N', '/media/game/water_N.png');
	game.load.image('sea_S', '/media/game/water_S.png');

	// game.load.image('castle', '/media/game/castle.gif');
	
	game.load.image('stone_plain', '/media/game/stone_plain.png');
	game.load.image('stone_sand', '/media/game/stone_sand.png');
	game.load.image('wood', '/media/game/wood.png');
	game.load.image('sands', '/media/game/sands.png');
	game.load.image('iron_plain', '/media/game/iron_plain.png');
	game.load.image('iron_sand', '/media/game/iron_sand.png');
	game.load.image('carbon', '/media/game/carbon_plain.png');
	game.load.image('oil', '/media/game/oil.png');
	game.load.image('uran_plain', '/media/game/uran_plain.png');
	game.load.image('uran_sand', '/media/game/uran_sand.png');
	// game.load.image('uran', '/media/game/uran.png');
	// game.load.image('oil', '/media/game/oil.png');
	// game.load.image('aluminium', '/media/game/aluminium.png');

	game.load.image('wheat', '/media/game/wheat.png');
	game.load.image('grapes', '/media/game/grapes.png');
	game.load.image('citrus', '/media/game/citrus.png');
	
	// game.load.image('flower', '/media/game/flower.png');

	// game.load.tilemap('landscape', '/media/game/landscape_tilemap.png');

	game.load.image('castle1', '/media/game/castle1.png');
}

var map = new Map('RUS');
var render = new Render(game);
map.generate();

function create() {
	// console.log(map.cells);
	game.world.setBounds(-1024, -768, 4096, 3072);
	// game.world.setBounds(0, 0, 1024, 768);
	game.debug.text(game.time.fps, 8, 16, '#00FF00');
	// var loading_screen = game.add.sprite(0, 0, 'loading-screen');
	// var loading_tooltip = game.add.text(game.world.centerX, 100, "Ратуша - основное здание в игре");
	// loading_tooltip.anchor.setTo(0.5);
	// loading_tooltip.font = 'Neucha';
	// loading_tooltip.fontSize = 14;
	// loading_tooltip.fill = "#ffd700";
	// loading_tooltip.setShadow(2, 2, 'rgba(0,0,0,0.5)', 2);
	render.draw(map);

	game.kineticScrolling.configure({
		kineticMovement: false,
		verticalScroll: true,
		timeConstantScroll: 0,
		horizontalWheel: false,
		verticalWheel: false,
		deltaWheel: 0
	});
	game.kineticScrolling.start();
	console.log(game);
}

var mouseTrack = {
	last: null,
}

function update() {
	game.debug.text(game.time.fps, 8, 16, '#00FF00');
}

function render() {
	game.debug.cameraInfo(game.camera, 32, 16);
}

$(function() {
	var scienceModal = new Modal($('#scienceModal'));
	var buildingModal = new Modal($('#buildingModal'));
	$('#scienceBtn').click(function() {
		scienceModal.show();
	});
	$('#buildingBtn').click(function() {
		buildingModal.show();
	});

	$('#help_button').click(function() {
		buildCastle = !buildCastle;
	});
});