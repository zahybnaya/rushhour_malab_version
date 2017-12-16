/*
 * Requires:
 *     psiturk.js
 *     utils.js
 */

// Initalize psiturk object
var psiTurk = new PsiTurk(uniqueId, adServerLoc, mode);
var mycondition = condition;  // these two variables are passed by the psiturk server process
var mycounterbalance = counterbalance;  // they tell you which condition you have been assigned to
// they are not used in the stroop code but may be useful to you
// All pages to be loaded
var pages = [
	"instructions/instruct-1.html",
	"instructions/instruct-2.html",
	"instructions/instruct-2_2.html",
	"instructions/instruct-3.html",
	"instructions/instruct-4.html",
	"instructions/instruct-ready.html",
	"stage.html",
	"thanks.html",
	"postquestionnaire.html"
];

psiTurk.preloadPages(pages);

var instructionPages = [ // add as a list as many pages as you like
	"instructions/instruct-1.html",
	"instructions/instruct-2.html",
	"instructions/instruct-2_2.html",
	"instructions/instruct-3.html",
	"instructions/instruct-4.html",
	"instructions/instruct-5.html",
	"instructions/instruct-ready.html"
];


var select_puzzles = function(howmany,max){
	indexes = [];
	while (indexes.length < howmany){
		indexes[indexes.length]=Math.floor(Math.random()*max);
	}
	return indexes;
}

function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;
  while (0 !== currentIndex) {
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }
  return array;
}

/********************
* HTML manipulation
*
* All HTML files in the templates directory are requested 
* from the server when the PsiTurk object is created above. We
* need code to get those pages from the PsiTurk object and 
* insert them into the document.
*
* TODO: Change the look/cosmetics
* 
********************/
var RushhourExperiment = function() {
	//document.body.innerHTML = '<h1>Rush Hour</h1></p><p id="status"></p><ul id="game-stats"><li id="timer"></li><li id="panel"></li><li>Moves: <span id="moves" class="value">0</span></li></ul><div id="game"><div class="exit"></div></div><p>Click and drag the cars to guide the green car to the exit.</p></div> </svg>';
	document.body.innerHTML = '</p><p id="status"></p><ul id="game-stats"><li id="buttons"></li></ul><div id="game"><div class="exit"></div></div></div> </svg>';
	var  board, boardPositions, carFreedom, carPadding, carPositions, colours, container, detectFreedom, drag, dragEnd, dragMove, dragStart, intersection, moves, occupiedPositions, positionToX, positionToY, ref, scalar, startMoment, startXY, svg, tilePadding, timer, updateTimer, gameWon, isTimeout, timeout;
	gameWon=false;
	container = '#game';
	timeout = 45*60*1000;
	colours = ['#009933','#cc0099'];
	svg = d3.select(container).append('svg').attr('width', '100%').attr('height', '100%');
	panelsvg = d3.select('#buttons').append('svg').attr('width', '100%').attr('height', '100%');
	board = 6;
	scalar = 100;
	tilePadding = 16;
	carPadding = 6;
	moves = 0;
	startMoment = moment();
	//puzzle_files = ['static/json/empty_v.json']; 
	puzzle_files = ['static/json/1509723682_71_prb78717_9_.json', 'static/json/1509488743_04_prb21044_9_.json', 'static/json/1509682160_18_prb72425_9_.json', 'static/json/1509728576_32_prb81064_9_.json', 'static/json/1509470807_13_prb13482_9_.json', 'static/json/1509556552_63_prb34405_9_.json', 'static/json/1509721337_05_prb77447_9_.json', 'static/json/1509477339_66_prb17203_9_.json', 'static/json/1509429110_14_prb5142_9_.json', 'static/json/1509566838_88_prb38511_9_.json', 'static/json/1509573002_21_prb41543_9_.json', 'static/json/1509503827_46_prb25973_9_.json', 'static/json/1509463627_74_prb9799_9_.json', 'static/json/1509649678_15_prb63683_9_.json', 'static/json/1509503135_71_prb25705_9_.json', 'static/json/1509420940_67_prb1228_9_.json', 'static/json/1509555412_17_prb33699_9_.json', 'static/json/1509643218_25_prb61959_9_.json', 'static/json/1509574359_43_prb42331_9_.json', 'static/json/1509477123_34_prb17035_9_.json', 'static/json/1509411897_18_prb717_11_.json', 'static/json/1509459257_76_prb7549_11_.json', 'static/json/1509720742_48_prb77111_11_.json', 'static/json/1509576724_28_prb43652_11_.json', 'static/json/1509555428_47_prb33717_11_.json', 'static/json/1509599054_93_prb52317_11_.json', 'static/json/1509491386_49_prb22491_11_.json', 'static/json/1509652414_89_prb65072_11_.json', 'static/json/1509473974_89_prb15412_11_.json', 'static/json/1509557042_37_prb34602_11_.json', 'static/json/1509490191_26_prb21669_11_.json', 'static/json/1509556026_72_prb34092_11_.json', 'static/json/1509429305_0_prb5252_11_.json', 'static/json/1509559246_47_prb35826_11_.json', 'static/json/1509571615_2_prb40909_11_.json', 'static/json/1509423295_78_prb2510_11_.json', 'static/json/1509556433_37_prb34290_11_.json', 'static/json/1509724613_21_prb79216_11_.json', 'static/json/1509422263_59_prb1969_11_.json', 'static/json/1509587855_12_prb48202_11_.json', 'static/json/1509673998_59_prb68514_14_.json', 'static/json/1509488403_92_prb20888_14_.json', 'static/json/1509455375_45_prb6294_14_.json', 'static/json/1509567550_91_prb38725_14_.json', 'static/json/1509419191_31_prb129_14_.json', 'static/json/1509653121_81_prb65535_14_.json', 'static/json/1509463186_98_prb9596_14_.json', 'static/json/1509656597_95_prb66793_14_.json', 'static/json/1509481208_68_prb19356_14_.json', 'static/json/1509502366_25_prb25255_14_.json', 'static/json/1509554623_5_prb33117_14_.json', 'static/json/1509546655_55_prb28956_14_.json', 'static/json/1509479376_37_prb18275_14_.json', 'static/json/1509457858_6_prb6671_14_.json', 'static/json/1509720366_41_prb76929_14_.json', 'static/json/1509468630_51_prb12360_14_.json', 'static/json/1509464540_58_prb10195_14_.json', 'static/json/1509545962_33_prb28697_14_.json', 'static/json/1509472355_7_prb14485_14_.json', 'static/json/1509503629_34_prb25871_14_.json', 'static/json/1509629349_75_prb57223_16_.json', 'static/json/1509565548_04_prb37893_16_.json', 'static/json/1509577648_29_prb44171_16_.json', 'static/json/1509420356_65_prb813_16_.json', 'static/json/1509474295_6_prb15595_16_.json', 'static/json/1509546793_06_prb29027_16_.json', 'static/json/1509508781_01_prb28189_16_.json', 'static/json/1509623373_2_prb55905_16_.json', 'static/json/1509722874_99_prb78361_16_.json', 'static/json/1509556503_33_prb34360_16_.json']; 
	puzzle_files=shuffle(puzzle_files)
	puzzle_number=0;
	howmany_puzzles=70;
	puzzle_file = puzzle_files[puzzle_number++];
	restartButton=panelsvg.append("image").attr("xlink:href", "static/images/restart.png").attr("x","0").attr("y","0").attr("width","55").attr("height", "55");
	surrenderButton=panelsvg.append("image").attr("xlink:href", "static/images/surrender.svg").attr("x","120").attr("y","0").attr("width","70").attr("height", "70");
	restartButton.on('click',function(){
		message=' t:['+moment()+'] event:[restart] piece:[NA] move#:['+moves+'] move:[NA] instance:['+puzzle_id+']'
		psiTurk.recordTrialData(message);
		psiTurk.saveData();	
		moves=0
		svg.selectAll('rect.car').remove();
		d3.json(puzzle_file,j_callback);
	});
	surrenderButton.on('click',function(){
		message=' t:['+moment()+'] event:[surrender] piece:[NA] move#:['+moves+'] move:[NA] instance:['+puzzle_id+']'
		psiTurk.recordTrialData(message);
		psiTurk.saveData();	
		if (moment().diff(startMoment) > timeout || puzzle_number>puzzle_file.length){
				return finish();
		}
		svg.selectAll('rect.car').remove();
		moves=0;
		puzzle_file = puzzle_files[puzzle_number++];
		d3.json(puzzle_file,j_callback);
		//gameWon=false;
		svg.selectAll('#great').remove();
		
	});

//	updateTimer = function() {
//		return d3.select('#timer').text(moment().diff(startMoment));
//	};

	timer = setInterval(updateTimer, 1000);
	intersection = function(a1, a2) {
		return a1.filter(function(n) {
			return a2.indexOf(n) !== -1;
		});
	};
	ref = [[], 0], carFreedom = ref[0], startXY = ref[1];
	dragStart = function(d) {
		carFreedom = detectFreedom(d3.select(this));
		message=' t:['+moment()+'] event:[drag_start] piece:['+d.id+'] move#:['+moves+'] move:['+d.position+'] instance:['+puzzle_id+']'
		psiTurk.recordTrialData(message);
		psiTurk.saveData();	
		console.log(message)
		return startXY = d.orientation === 'horizontal' ? d.x : d.y;
	};
	dragMove = function(d) {
		if (gameWon){
			return ;
		}
		var axis, car, leftBound, relativeXY, rightBound, time, xy;
		axis = d.orientation === 'horizontal' ? 'x' : 'y';
		xy = d3.event[axis];
		car = d3.select(this);
		relativeXY = xy - startXY;
		leftBound = relativeXY < 0 && Math.abs(relativeXY) < carFreedom[0] * scalar;
		rightBound = relativeXY >= 0 && relativeXY < carFreedom[1] * scalar;
		if (leftBound || rightBound) {
			return car.attr(axis, d[axis] = xy);
		} else {
			if (relativeXY < 0) {
				return car.attr(axis, d[axis] = startXY - carFreedom[0] * scalar);
			} else {
				car.attr(axis, d[axis] = startXY + carFreedom[1] * scalar);
				if (!rightBound && d.player && boardPositions(board - 1, 'vertical').indexOf(d.position + d.length - 1 + carFreedom[1]) > -1) {
					//time = d3.select('#timer').text();
					clearInterval(timer);
					message=' t:['+moment()+'] event:[win] piece:['+d.id+'] move#:['+moves+'] move:['+d.position+'] instance:['+puzzle_id+']'
					psiTurk.recordTrialData(message);
					psiTurk.saveData();	
					svg.selectAll('rect.car').remove();
					gameWon=true;
					return  ;
				}
			}
		}
	};

	dragEnd = function(d) {
		var distance, newPosition, positions, xy;
		xy = d.orientation === 'horizontal' ? d.x : d.y;
		distance = Math.round((xy - startXY) / scalar);
		positions = boardPositions(d.position, d.orientation);
		newPosition = positions[positions.indexOf(d.position) + distance];
		//time = d3.select('#timer').text();
		message=' t:['+moment()+'] event:[drag_end] piece:['+d.id+'] move#:['+moves+'] move:['+newPosition+'] instance:['+puzzle_id+']';
		psiTurk.recordTrialData(message);
		psiTurk.saveData();	
		console.log(message)
		if (Math.abs(distance) > 0) {
			d3.select('#moves').text(++moves);
		}
		ret=d3.select(this).attr('data-position', d.position = newPosition).transition().attr('x', d.x = positionToX(d.position)).attr('y', d.y = positionToY(d.position));
		if (gameWon){
			if ( moment().diff(startMoment) > timeout || puzzle_number>=howmany_puzzles){
				return finish();
			}
			pause = moment();
			great=svg.append("image").attr("id", "great").attr("xlink:href", "static/images/great.gif").attr("x","0").attr("y","0").attr("width","570").attr("height", "670");
			great.on('click',function(){
				timeout=timeout+moment().diff(pause);
				//svg.selectAll('rect.car').remove();
				moves=0;
				puzzle_file = puzzle_files[puzzle_number++];
				d3.json(puzzle_file,j_callback);
				gameWon=false;
				svg.selectAll('#great').remove();
			});
		}
		return ret;
		//return d3.select(this).attr('data-position', d.position = newPosition).transition().attr('x', d.x = positionToX(d.position)).attr('y', d.y = positionToY(d.position));
	};
	drag = d3.behavior.drag().origin(function(d) {
		return d;
	}).on('dragstart', dragStart).on('drag', dragMove).on('dragend', dragEnd);

	detectFreedom = function(car) {
		var l, lower, o, orientation, pos, positions, u, upper;
		pos = car.attr('data-position');
		orientation = car.attr('data-orientation');
		positions = boardPositions(pos, orientation);
		o = intersection(positions, occupiedPositions());
		upper = d3.min(o.filter(function(n) {
			return n > d3.max(carPositions(car));
		}));
		lower = d3.max(o.filter(function(n) {
			return n < d3.min(carPositions(car));
		}));
		if (upper) {
			u = positions.indexOf(upper) - positions.indexOf(d3.max(carPositions(car)));
		} else {
			u = board - positions.indexOf(d3.max(carPositions(car)));
		}
		l = positions.indexOf(d3.min(carPositions(car))) - positions.indexOf(lower);
		return [l - 1, u - 1];
	};

	boardPositions = function(position, orientation) {
		if (orientation === 'horizontal') {
			return d3.range(position - position % board, position - position % board + board);
		} else {
			return d3.range(position % board, Math.pow(board, 2), board);
		}
	};

	occupiedPositions = function() {
		var positions;
		positions = [];
		svg.selectAll('rect.car').each(function(d, i) {
			return positions = positions.concat(carPositions(d3.select(this)));
		});
		return positions;
	};

	carPositions = function(car) {
		var length, orientation, pos, possiblePositions, start;
		pos = parseInt(car.attr('data-position'));
		length = parseInt(car.attr('data-length'));
		orientation = car.attr('data-orientation');
		possiblePositions = boardPositions(pos, orientation);
		if (orientation === 'horizontal') {
			return possiblePositions.slice(pos % board, pos % board + length);
		} else {
			start = Math.floor(pos / board);
			return possiblePositions.slice(start, start + length);
		}
	};

	positionToX = function(position) {
		return scalar * (position % board) + carPadding;
	};

	positionToY = function(position) {
		return scalar * Math.floor(position / board) + carPadding;
	};

	var finish = function(){
	    currentview = new Questionnaire();
	};

	var j_callback = function(error, json) {
			var car, carAttributes, cars, j, len, ref1, squareAttributes, squares;
			puzzle_id = json.id;
			if (error) {
				console.warn(error);
			}
			squares = svg.append('g').attr('class', 'tiles').selectAll('rect.square').data(d3.range(Math.pow(board, 2))).enter().append('rect');
			squareAttributes = squares.attr('x', function(i) {
				return scalar * (i % board) + tilePadding;
			}).attr('y', function(i) {
				return scalar * Math.floor(i / board) + tilePadding;
			}).attr('height', scalar - tilePadding * 2).attr('width', scalar - tilePadding * 2).attr('fill', '#f4f4f2');
			ref1 = json.cars;
			for (j = 0, len = ref1.length; j < len; j++) {
				car = ref1[j];
				car.x = positionToX(car.position);
				car.y = positionToY(car.position);
			}
			cars = svg.append('g').attr('class', 'cars').selectAll('rect.car').data(json.cars).enter().append('rect');
			message=' t:['+moment()+'] event:[start] piece:[NA] move#:['+moves+'] move:[NA] instance:['+puzzle_id+']';
			psiTurk.recordTrialData(message);
			psiTurk.saveData();	
			return carAttributes = cars.attr('class', 'car').attr('data-position', function(d) {
				return d.position;
			}).attr('data-length', function(d) {
				return d.length;
			}).attr('data-orientation', function(d) {
				return d.orientation;
			}).attr('x', function(d) {
				return d.x;
			}).attr('y', function(d) {
				return d.y;
			}).attr('height', function(d) {
				return (d.orientation === 'vertical' ? scalar * d.length : scalar) - carPadding * 2;
			}).attr('width', function(d) {
				return (d.orientation === 'horizontal' ? scalar * d.length : scalar) - carPadding * 2;
			}).attr('fill', function(d) {
				if (d.player) {
					return colours[1];
				} else {
					return colours[0];
				}
			}).call(drag);
		};
	d3.json(puzzle_file,j_callback);

};//RushhourExperiment

/********************
* STROOP TEST       *
********************/
var StroopExperiment = function() {

	var wordon, // time word is presented
	    listening = false;

	// Stimuli for a basic Stroop experiment
	var stims = [
			["SHIP", "red", "unrelated"],
			["MONKEY", "green", "unrelated"],
			["ZAMBONI", "blue", "unrelated"],
			["RED", "red", "congruent"],
			["GREEN", "green", "congruent"],
			["BLUE", "blue", "congruent"],
			["GREEN", "red", "incongruent"],
			["BLUE", "green", "incongruent"],
			["RED", "blue", "incongruent"]
		];

	stims = _.shuffle(stims);

	var next = function() {
		if (stims.length===0) {
			finish();
		}
		else {
			stim = stims.shift();
			show_word( stim[0], stim[1] );
			wordon = new Date().getTime();
			listening = true;
			d3.select("#query").html('<p id="prompt">Type "R" for Red, "B" for blue, "G" for green.</p>');
		}
	};
	
	var response_handler = function(e) {
		if (!listening) return;

		var keyCode = e.keyCode,
			response;

		switch (keyCode) {
			case 82:
				// "R"
				response="red";
				break;
			case 71:
				// "G"
				response="green";
				break;
			case 66:
				// "B"
				response="blue";
				break;
			default:
				response = "";
				break;
		}
		if (response.length>0) {
			listening = false;
			var hit = response == stim[1];
			var rt = new Date().getTime() - wordon;

			psiTurk.recordTrialData({'phase':"TEST",
                                     'word':stim[0],
                                     'color':stim[1],
                                     'relation':stim[2],
                                     'response':response,
                                     'hit':hit,
                                     'rt':rt}
                                   );
			remove_word();
			next();
		}
	};

	var finish = function() {
	    $("body").unbind("keydown", response_handler); // Unbind keys
	    currentview = new Questionnaire();
	};
	
	var show_word = function(text, color) {
		d3.select("#stim")
			.append("div")
			.attr("id","word")
			.style("color",color)
			.style("text-align","center")
			.style("font-size","150px")
			.style("font-weight","400")
			.style("margin","20px")
			.text(text);
	};

	var remove_word = function() {
		d3.select("#word").remove();
	};

	
	// Load the stage.html snippet into the body of the page
	psiTurk.showPage('stage.html');

	// Register the response handler that is defined above to handle any
	// key down events.
	$("body").focus().keydown(response_handler); 

	// Start the test
	next();
};


/****************
* Questionnaire *
****************/

var Questionnaire = function() {

	var error_message = "<h1>Oops!</h1><p>Something went wrong submitting your HIT. This might happen if you lose your internet connection. Press the button to resubmit.</p><button id='resubmit'>Resubmit</button>";

	record_responses = function() {

		psiTurk.recordTrialData({'phase':'postquestionnaire', 'status':'submit'});

		$('textarea').each( function(i, val) {
			psiTurk.recordUnstructuredData(this.id, this.value);
		});
		$('select').each( function(i, val) {
			psiTurk.recordUnstructuredData(this.id, this.value);		
		});

	};

	prompt_resubmit = function() {
		document.body.innerHTML = error_message;
		$("#resubmit").click(resubmit);
	};

	resubmit = function() {
		document.body.innerHTML = "<h1>Trying to resubmit...</h1>";
		reprompt = setTimeout(prompt_resubmit, 10000);
		
		psiTurk.saveData({
			success: function() {
			    clearInterval(reprompt); 
                psiTurk.computeBonus('compute_bonus', function(){finish()}); 
			}, 
			error: prompt_resubmit
		});
	};

	// Load the questionnaire snippet 
	psiTurk.showPage('postquestionnaire.html');
	psiTurk.recordTrialData({'phase':'postquestionnaire', 'status':'begin'});
	
	$("#next").click(function () {
	    record_responses();
	    psiTurk.saveData({
            success: function(){
                psiTurk.computeBonus('compute_bonus', function() { 
                	psiTurk.completeHIT(); // when finished saving compute bonus, the quit
                }); 
            }, 
            error: prompt_resubmit});
	});
    
	
};

// Task object to keep track of the current phase
var currentview;

/*******************
 * Run Task
 ******************/
$(window).load( function(){
    psiTurk.doInstructions(
    	instructionPages, // a list of pages you want to display in sequence
    	function() { currentview = new RushhourExperiment(); } // what you want to do when you are done with instructions
    );
});
