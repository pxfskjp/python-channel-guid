
// var G_days = [
// 	{ day: "Monday", date: "21st Sept" },
// 	{ day: "Tuesday", date: "22nd Sept" },
// 	{ day: "Wednesday", date: "23rd Sept" },
// 	{ day: "Thursday", date: "24th Sept" },
// 	{ day: "Friday", date: "25th Sept" },
// 	{ day: "Saturday", date: "26th Sept" },
// 	{ day: "Sunday", date: "27th Sept" }

// ];

var GLOBAL_selected_date = "default";
var GLOBAL_channels = []

var GLOBAL_time_offset = 0.0;

// var GLOBAL_done_first = false;

function decodeHtml(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
}

function ISODateString(d){
    function pad(n){return n<10 ? '0'+n : n}
    return d.getUTCFullYear()+'-'
    + pad(d.getUTCMonth()+1)+'-'
    + pad(d.getUTCDate())
}

function is_today(date) {
	var d = new Date();
	var ts = "" + ISODateString(d);
	// alert (date + "," + ts);
	return (ts == date); 
}

function change_day(day, elem) {
	// alert(is_today(day));
	$("#days > li").removeClass("day-selected");
	$(elem).parent().parent().addClass("day-selected");
	GLOBAL_selected_date = day;
	repopulate_all_channels();
	// alert(elem);
	if (!is_today(day)) {
		$("#channels-container").scrollLeft(0);
	}
	else {
		$("#channels-container").scrollLeft(240.0*updateTime()+90.0 - 300.0);
		// GLOBAL_done_first = true;
	}
	update_pos();
}

function updateTime() {
	// var d = new Date()
	var h = moment().tz("America/Los_Angeles").hour()
	var m = moment().tz("America/Los_Angeles").minute()
	// var h = d.hour
	// var m = d.minute
	var m_f = ((m)/60.0);
	var t = h + m_f;

	$("#current-time-bar").css("margin-left", (((t+GLOBAL_time_offset) * 240.0) + 90.0) + "px");
	setTimeout(updateTime, 1000*60);
	update_pos();
	return t + GLOBAL_time_offset;
}


function close_iframe() {
	$("#frame, #darken").css("visibility", "hidden");
	$("#frame, #darken").css("display", "none");
}

function show_iframe(str) {
	$("#frame, #darken").css("visibility", "visible");
	$("#frame, #darken").css("display", "block");

	$("#frame > iframe").attr("src", "about:blank");
	iframe = $("#frame > iframe")[0];

	iframedoc = iframe.contentDocument || iframe.contentWindow.document;
	iframedoc.body.innerHTML = '<strong style="text-align: center; width: 100%; display: block; margin-top: 120px;">Loading, please stand by...</strong>';

	$("#frame > iframe").attr("src", str);

}



function add_days () {


	$.ajax({
		url: "days",
		cache: false
	}).done(function(data) {
		var is_first = false;
		// alert(html);
		for (day_i = 0; day_i < data.length; ++day_i) {
			var c_day = data[day_i];


			var li = jQuery('<li/>', {});
			var a = $("<a/>", {}).attr("href", "#").attr("data-day", c_day.date).addClass("day-link").appendTo(li);
			GLOBAL_selected_date = c_day.date;
			$(a).click(function(e){
				e.preventDefault();
				change_day($(this).attr("data-day"), e.target);
			});

			var day_text = "";
			if (is_first) {
				day_text = "Today";
				is_first = false;
			} else {
				day_text = c_day.day;
			}
			$("<div/>", {
				class: "day-name",
				text: day_text
			}).appendTo(a);

			$("<div/>", {
				class: "day-date",
				text: c_day.human_date
			}).appendTo(a);


			$(li).appendTo('#days');



		}

		d = $($("#days").children("li")[0]).children("a")[0];

		change_day($(d).attr("data-day"), $(d).children()[0]);

		// $($("#days").children("li")[0]).addClass("day-selected");
		// updateTime();
		// $("#channels-container").scrollLeft($("#current-time-bar").offset().left - 90 - 200);
		// update_pos();
	});



}

function add_hour_markers() {
	offset = 0;
	cumul = 90;

	for (h = 0; h < 25; ++h) {
		var time_as_text = "" + h % 12;

		time_as_text += (h > 12) ? "pm" : "am";

		if ((h == 0) || (h == 24)) {time_as_text = "Midnight"}
		if (h == 12) {time_as_text = "Midday"}
		//if (h == 24) {time_as_text = ""}

		var e = $("<span/>", {
			class: "hour-marker",
			text: time_as_text
		});
		e.css("left", cumul+offset + "px");
		e.appendTo($("#time-bar"));
		cumul = cumul + 240;
	}

	add_half_hour_markers();
}

function add_half_hour_markers() {
	offset = 0;
	cumul = 90 + 120;

	for (h = 0; h < 24; ++h) {
		var time_as_text = "" + h % 12 + ":30";

		time_as_text += (h > 11) ? "pm" : "am";

		// if ((h == 0) || (h == 24)) {time_as_text = "Midnight"}
		// if (h == 12) {time_as_text = "Midday"}
		//if (h == 24) {time_as_text = ""}

		var e = $("<span/>", {
			class: "hour-marker half-hour",
			text: time_as_text
		});
		e.css("left", cumul+offset + "px");
		e.appendTo($("#time-bar"));
		cumul = cumul + 240;
	}
}

function add_programme(program, channel) {
	var hour = parseFloat(program.starts.substring(0,2));
	var minutes = parseFloat(program.starts.substring(2,4))/60.0;
	var start_time = hour+minutes-GLOBAL_time_offset;
	// console.log(GLOBAL_time_offset);
		var PIXELS_PER_MINUTE = 4;
	var pos = Math.floor((start_time * (PIXELS_PER_MINUTE * 60)+0.0)); //$(channel).attr("data-next-pos");

	var width = program.duration * PIXELS_PER_MINUTE;


	var prog_desc = decodeHtml(program.program_name.replace("&amp;", "&").replace("&#8217;", "'"));
	var desc = $("<span/>").addClass("program-desc").text(prog_desc);
	var episode_desc = "";
	if (program.episode_name) {
		episode_desc = program.episode_name;
	}
	var epi_desc = $("<span/>").addClass("episode-desc").text(episode_desc);
	var prog = $("<div/>").addClass("program").css("margin-left", pos + "px").css("width", width+"px");
	if (width < 240) {
		prog.addClass("program-short");
	}
	desc.appendTo(prog);
	// epi_desc.appendTo(prog);
	$(channel).find(".programs").append(prog);
	$(channel).attr("data-next-pos", pos + width);
}

function populate_channel(chan, dom) {
	// alert("pop");




	$.ajax({
		url: "schedule/" + chan.number + "/" + GLOBAL_selected_date
		//cache: false
	}).done(function(data) {
		if (data["error"] == "yes") {
			err = $("<span/>").addClass("not-found");
			err.append($("<a />").text("Click here").attr("href", chan.schedule_url).attr("target", "_blank").click(function(e){
				e.preventDefault();
				show_iframe(this);
			}));
			err.append($("<span />").text(" for "+ chan.name + " schedules"));

			dom.find(".channel-name").append(err);
		} else {
			for (prog_i = 0; prog_i < data.length; ++prog_i) {
				var prog = data[prog_i];
				add_programme(prog, dom);
			}
		}
	});

}

function repopulate_all_channels() {
	$(".program").remove();
	$(".not-found").remove();
	$("#days").css("visibility", "hidden");


	if (GLOBAL_channels.length > 0) {
		for (chan_i = 0; chan_i < GLOBAL_channels.length; ++chan_i) {
			var chan = GLOBAL_channels[chan_i];
			populate_channel(chan, chan.element);
			// alert(chan.test)
		}
	}
}

function maybe_reenable_days() {

}

function add_channel(chan) {
	//alert(chan.name);
	var number = $("<div/>").addClass("channel-number").text(chan.number);
	number.append($("<span/>").addClass("channel-name").text(chan.name))
	var name = $("<div/>").addClass("channel-name").text(chan.name);
	var logo = $("<div/>").addClass("channel-logo").append(number);
	logo.css("background-image", "url('static/img/logos_2/" + chan.number + ".jpg')");
	var dummy = $("<div/>").addClass("channel-logo-dummy");
	var programs = $("<div/>").addClass("programs");


	var display_name = "Test " + chan.name + " Show";
	if (display_name.length >= 25) {
		display_name = display_name.substring(0, 20) + "...";
	}
	// programs.append('<div class="program"><span class="program-desc">' + display_name + '</span><!--<span class="program-time">9am-10am</span>--></div>');
	var channel = $("<div/>").addClass("channel").attr("data-next-pos", 0);
	logo.appendTo(channel);
	// name.appendTo(channel);
	dummy.appendTo(channel);
	programs.appendTo(channel);

	channel.appendTo($("#channels-container"));

	chan.element = channel;

	populate_channel(chan, channel);

	// for (prog_i = 0; prog_i < G_test_data["programmes"].length; ++prog_i) {
	// 	add_programme(G_test_data["programmes"][prog_i], channel);
	// }
	
}





function add_channels() {
	// $('#channels-container').find('*').not('#time-bar').remove();
	$("#channels-container > *:not('#time-bar, #current-time-bar')").remove();
	$.ajax({
		url: "channels",
		cache: true
	}).done(function(data) {
		channels = data.channels;
		GLOBAL_channels = channels;
		// alert(html);
		for (chan_i = 0; chan_i < channels.length; ++chan_i) {
			var chan = channels[chan_i];
			add_channel(chan);
		}

		$("#current-time-bar").height(80*(channels.length+5));
	});
	// alert(1);
}

function scrollHorizontally(e) {
    e = window.event || e;
    var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
    //document.documentElement.scrollLeft -= (delta*40); // Multiplied by 40
    //document.body.scrollLeft -= (delta*40); // Multiplied by 40

    document.getElementById("channels").scrollLeft -= (delta*40);
    e.preventDefault();
}

function update_pos() {
			var left = $("#channels-container").scrollLeft();
		var top = $("#channels-container").scrollTop();
		$(".channel-logo").css("margin-left", ""+left+"px")
		$("#time-bar").css("margin-top", ""+top+"px")
}

$(document).ready(function() {

	// if (window.addEventListener) {
	//     // IE9, Chrome, Safari, Opera
	//     document.getElementById("channels").addEventListener("mousewheel", scrollHorizontally, false);
	//     // Firefox
	//     document.getElementById("channels").addEventListener("DOMMouseScroll", scrollHorizontally, false);
	// } else {
	//     // IE 6/7/8
	//     document.getElementById("channels").attachEvent("onmousewheel", scrollHorizontally);
	// }
	$("#channels-container").scroll(update_pos);
	$("#channels-container").on("touchmove", update_pos);

	add_days();
	add_hour_markers();
	add_channels();

	$("#next").click(function(){
		$("#channels-container").scrollLeft(  $("#channels-container").scrollLeft() + 240   );
	});

	$("#prev").click(function(){
		$("#channels-container").scrollLeft(  $("#channels-container").scrollLeft() - 240   );
	});


	$("#timezone").change(function(){
		// alert($(this).val());
		GLOBAL_time_offset = parseFloat($(this).val()) + 0.0;
		updateTime();
		repopulate_all_channels();
		$("#channels-container").scrollLeft(240.0*updateTime()+90.0 - 300.0);
	});
	update_pos();
	setTimeout(update_pos, 150);
	setTimeout(update_pos, 500);
	setTimeout(update_pos, 1500);
	setTimeout(update_pos, 3000);
	updateTime()

	// setInterval(maybe_reenable_days, 1000);

	$(document).ajaxStop(function(){
		$("#days").css("visibility", "visible");
	});


	$("#darken").click(function() {
		close_iframe();
	});

	//show_iframe();

	$("#frame-close").click(function() {
		close_iframe();
	});

	



});