<html>
	<head>
		<title>LW Display</title>
		<style>

/*
	Based upon Jakub Hampl's "Designing a departures board with CSS3".
	http://gampleman.eu/post/1488470623/designing-a-departures-board-with-css3
*/

body {
	background-color: rgb(30,30,30);
}

.departure-board {
    padding:  0.36em;
    display: inline-block;
	line-height: 1.3em;
    background: rgb(30, 30, 30);
    -webkit-border-radius: 0.21em;
    -moz-border-radius: 0.21em;
    border-radius: 0.21em;
    color: #eee;
	font-family: Helvetica;
}


.departure-board span.letter {
	display: inline-block;
	width: 1em;
	margin: 0 .1em;
	height: 1.3em;
	text-align: center;
	position: relative;
}


.departure-board span.letter {
	-webkit-box-shadow:
		inset 0 -.07em 0 rgba(50, 50, 50, .7),
		inset 0 -.14em 0 rgba(0, 0, 0, .7),
		inset .14em 0 .28em rgba(0, 0, 0, .9),
		inset -.14em 0 .28em rgba(0, 0, 0, .9),
		0 .07em 0 rgba(255, 255, 255, .2);

	-moz-box-shadow:
		inset 0 -.07em 0 rgba(50, 50, 50, .7),
		inset 0 -.14em 0 rgba(0, 0, 0, .7),
		inset .14em 0 .28em rgba(0, 0, 0, .9),
		inset -.14em 0 .28em rgba(0, 0, 0, .9),
		0 .07em 0 rgba(255, 255, 255, .2);

	-o-box-shadow:
		inset 0 -.07em 0 rgba(50, 50, 50, .7),
		inset 0 -.14em 0 rgba(0, 0, 0, .7),
		inset .14em 0 .28em rgba(0, 0, 0, .9),
		inset -.14em 0 .28em rgba(0, 0, 0, .9),
		0 .07em 0 rgba(255, 255, 255, .2);

	box-shadow:
		inset 0 -.07em 0 rgba(50, 50, 50, .7),
		inset 0 -.14em 0 rgba(0, 0, 0, .7),
		inset .14em 0 .28em rgba(0, 0, 0, .9),
		inset -.14em 0 .28em rgba(0, 0, 0, .9),
		0 .07em 0 rgba(255, 255, 255, .2);
}


.departure-board span.letter:before {
	border-top: .07em solid rgba(0, 0, 0, .4);
	border-bottom: .07em solid rgba(255, 255, 255, .08);
	height: 0;
	position: relative;
	width: 100%;
	left: 0;
	top: .62em;
	content: " ";
	display: block;
	z-index: 2;
	-moz-transform: translate(0, -.05em);
	-o-transform: translate(0, -.1em);
}


.departure-board span.fold {
	display: block;
	position: absolute;
	height: 0;
	top: .65em;
}


.departure-board span.flap {
	display: block;
	position: absolute;
	top: 0em;
	width: 1em;
	height: .65em;
	margin: 0;
	overflow: hidden;
}


.departure-board span.text {
	width: 100%;
}


.departure-board span.bottom {
	top: .65em;
}


.departure-board span.bottom span.text {
	position: relative;
	top: -.65em;
}



.departure-board span.flap.falling {
	display: none;
	bottom: 0;
	top: auto;
}


.departure-board span.flap.falling span.text {
	-webkit-backface-visibility: hidden;
	border-top: .03em solid #444;
	border-bottom: .03em solid #444;
    background: #000;
	display: block;
	position: relative;

	-webkit-transform: scaleY(1);
	-moz-transform: scaleY(1);
	-o-transform: scaleY(1);
	transform: scaleY(1);

	-webkit-transition: -webkit-transform linear;
	-moz-transition: -moz-transform linear;
	-o-transition: -o-transform linear;
	transition: transform linear;
}

		</style>
	</head>

	<body>
		<center>
		<div id="test"></div>
		</center>

		<script type="text/javascript">
var DepartureBoard = function (element, options) {
	options = options || {};

	this._element = element;
	this._letters = [];

	element.className += ' departure-board';

	var rowCount = options.rowCount || 1,
		letterCount = options.letterCount || 25,
		letter,
		rowElement;

	for (var r = 0; r < rowCount; r++) {
		this._letters.push ([]);

		rowElement = document.createElement ('div');
		rowElement.className = 'row';
		element.appendChild (rowElement);

		for (var l = 0; l < letterCount; l++) {
			letter = new DepartureBoard.Letter ();
			this._letters[r].push (letter);
			rowElement.appendChild (letter.getElement ());
		}
	}
};


DepartureBoard.LETTERS = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,':()&!?+-";




DepartureBoard.prototype.spin = function () {
	var me = this;

	for (var i = 0, l = this._letters.length; i < l; i++) {
		(function (i) {
			window.setTimeout (function () {
				me._letters[i].spin ();
			}, 20 * i + Math.random () * 400);
		})(i);
	}
};




DepartureBoard.prototype.setValue = function (value) {
	if (!(value instanceof Array)) value = [value];
	var me = this;

	for (var r = 0, rl = this._letters.length; r < rl; r++) {
		value[r] = value[r]? value[r].toUpperCase () : '';

		for (var i = 0, l = this._letters[r].length; i < l; i++) {
			(function (r, i) {
				window.setTimeout (function () {
					var letterValue = value[r].substr (i, 1) || '';
					me._letters[r][i].setValue (letterValue);
				}, 2000 * r + 25 * i + Math.random () * 400);
			})(r, i);
		}
	}
};








DepartureBoard.Letter = function () {
	this._element = document.createElement ('span');
	this._element.className = 'letter';

	this._bottom = document.createElement ('span');
	this._bottom.className = 'flap bottom';
	this._element.appendChild (this._bottom);

	this._bottomText = document.createElement ('span');
	this._bottomText.className = 'text';
	this._bottom.appendChild (this._bottomText);


	this._top = document.createElement ('span');
	this._top.className = 'flap top';
	this._element.appendChild (this._top);

	this._topText = document.createElement ('span');
	this._topText.className = 'text';
	this._top.appendChild (this._topText);


	this._fold = document.createElement ('span');
	this._fold.className = 'fold';
	this._element.appendChild (this._fold);

	this._falling = document.createElement ('span');
	this._falling.className = 'flap falling';
	this._fold.appendChild (this._falling);

	this._fallingText = document.createElement ('span');
	this._fallingText.className = 'text';

	this._fallingText.style.WebkitTransitionDuration = this._fallingText.style.MozTransitionDuration =
		this._fallingText.style.OTransitionDuration = this._fallingText.style.transitionDuration = DepartureBoard.Letter.DROP_TIME * 0.5 + 'ms';

	this._falling.appendChild (this._fallingText);


	this._index = 0;
	this._interval = null;
	this._stopAt = null;
};


DepartureBoard.Letter.DROP_TIME = 100;




DepartureBoard.Letter.prototype.getElement = function () {
	return this._element;
};




DepartureBoard.Letter.prototype.spin = function (clear) {
	if (clear !== false) this._stopAt = null;

	var me = this;
	this._interval = window.setInterval (function () { me._tick (); }, DepartureBoard.Letter.DROP_TIME * 1.1);
};




DepartureBoard.Letter.prototype.setValue = function (value) {
	this._stopAt = DepartureBoard.LETTERS.indexOf (value);

	if (this._stopAt < 0) this._stopAt = 0;
	if (!this._interval && this._index != this._stopAt) this.spin (false);
};




DepartureBoard.Letter.prototype._tick = function () {
	var me = this,
		oldValue = DepartureBoard.LETTERS.charAt (this._index),
		fallingStyle = this._falling.style,
		fallingTextStyle = this._fallingText.style,
		newValue;


	this._index = (this._index + 1) % DepartureBoard.LETTERS.length;
	newValue = DepartureBoard.LETTERS.charAt (this._index);

	this._fallingText.innerHTML = oldValue;
	fallingStyle.display = 'block';

	this._topText.innerHTML = newValue;

	window.setTimeout (function () {
		fallingTextStyle.WebkitTransitionTimingFunction = fallingTextStyle.MozTransitionTimingFunction = fallingTextStyle.OTransitionTimingFunction = fallingTextStyle.transitionTimingFunction = 'ease-in';
		fallingTextStyle.WebkitTransform = fallingTextStyle.MozTransform = fallingTextStyle.OTransform = fallingTextStyle.transform = 'scaleY(0)';
	}, 1);


	window.setTimeout (function () {
		me._fallingText.innerHTML = newValue;

		fallingStyle.top = '-.03em';
		fallingStyle.bottom = 'auto';
		fallingTextStyle.top = '-.65em';

		fallingTextStyle.WebkitTransitionTimingFunction = fallingTextStyle.MozTransitionTimingFunction = fallingTextStyle.OTransitionTimingFunction = fallingTextStyle.transitionTimingFunction = 'ease-out';
		fallingTextStyle.WebkitTransform = fallingTextStyle.MozTransform = fallingTextStyle.OTransform = fallingTextStyle.transform = 'scaleY(1)';
	}, DepartureBoard.Letter.DROP_TIME / 2);


	window.setTimeout (function () {
		me._bottomText.innerHTML = newValue;
		fallingStyle.display = 'none';

		fallingStyle.top = 'auto';
		fallingStyle.bottom = 0;
		fallingTextStyle.top = 0;
	}, DepartureBoard.Letter.DROP_TIME);


	if (this._index === this._stopAt) {
		clearInterval (this._interval);
		delete this._interval;
	}
};

get_data = function() {
	console.log("Hello");
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", "/update/");
	xhttp.onload = function() {
		console.log(this.responseText);
	}
	xhttp.send();

	window.setTimeout(get_data, 10000);
}

		</script>

		<script>

			var board = new DepartureBoard (document.getElementById ('test'), { rowCount: 15, letterCount: 25 });
			board.setValue (['19:30 London King\'s Cross', '19:42 Sheffield']);

			window.setTimeout (function () {
				get_data();
			 	board.setValue ('19:42 Sheffield');
			}, 10000);

		</script>
	</body>
</html>
