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
	"instructions/instruct-3.html",
	"instructions/instruct-ready.html",
	"stage.html",
	"postquestionnaire.html"
];

psiTurk.preloadPages(pages);

var instructionPages = [ // add as a list as many pages as you like
	"instructions/instruct-1.html",
	"instructions/instruct-2.html",
	"instructions/instruct-3.html",
	"instructions/instruct-ready.html"
];




/********************
* HTML manipulation
*
* All HTML files in the templates directory are requested 
* from the server when the PsiTurk object is created above. We
* need code to get those pages from the PsiTurk object and 
* insert them into the document.
*
* TODO: report data-  
* TODO: multiple instances
* TODO: surrender/restart
* TODO: Try on m.turk
* TODO: Change the look
*
********************/
var RushhourExperiment = function() {
	document.body.innerHTML = '<h1>Rush Hour</h1><p id="status"></p><div id="content"><ul id="game-stats"><li>Perfect score: <span class="value">15</span></li><li id="timer"></li><li>Moves: <span id="moves" class="value">0</span></li></ul><div id="game"><div class="exit"></div></div><p>Click and drag the cars to guide the green car to the exit.</p></div>';
	var puzzleId, board, boardPositions, carFreedom, carPadding, carPositions, colours, container, detectFreedom, drag, dragEnd, dragMove, dragStart, intersection, moves, occupiedPositions, positionToX, positionToY, ref, scalar, startMoment, startXY, svg, tilePadding, timer, updateTimer;
	container = '#game';
	colours = ['#ff7fff', '#7fff7f'];
	svg = d3.select(container).append('svg').attr('width', '100%').attr('height', '100%');
	board = 6;
	scalar = 100;
	tilePadding = 16;
	carPadding = 6;
	moves = 0;
	startMoment = moment();
	updateTimer = function() {
		return d3.select('#timer').text(moment().subtract(startMoment).format('mm:ss'));
	};
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
					time = d3.select('#timer').text();
					clearInterval(timer);
					message=' t:['+moment()+'] event:[win] piece:['+d.id+'] move#:['+moves+'] move:['+d.position+'] instance:['+puzzle_id+']'
					psiTurk.recordTrialData(message);
					psiTurk.saveData();	
					return d3.select('#status').text('You won! ' + time + ' and ' + (moves + 1) + ' moves');
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
		time = d3.select('#timer').text();
		message=' t:['+moment()+'] event:[drag_end] piece:['+d.id+'] move#:['+moves+'] move:['+newPosition+'] instance:['+puzzle_id+']';
		psiTurk.recordTrialData(message);
		psiTurk.saveData();	
		console.log(message)
		if (Math.abs(distance) > 0) {
			d3.select('#moves').text(++moves);
		}
		return d3.select(this).attr('data-position', d.position = newPosition).transition().attr('x', d.x = positionToX(d.position)).attr('y', d.y = positionToY(d.position));
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

	d3.json('static/js/level1.json', function(error, json) {
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
		}).attr('height', scalar - tilePadding * 2).attr('width', scalar - tilePadding * 2).attr('fill', '#f4f4f7');
		ref1 = json.cars;
		for (j = 0, len = ref1.length; j < len; j++) {
			car = ref1[j];
			car.x = positionToX(car.position);
			car.y = positionToY(car.position);
		}
		cars = svg.append('g').attr('class', 'cars').selectAll('rect.car').data(json.cars).enter().append('rect');
		message=' t:['+moment()+'] event:[start] piece:[NA] move#:['+moves+'] move:[NA] instance:['+puzzle_id+']'
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
	});
};
//}.call(this);
//};

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
