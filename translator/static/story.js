$(document).ready(function () {
	$("#tabs li").bind('click', function() {
		var index = $(this).index();
		$("#tabcontents .content").removeClass("selected");
		$("#tabs li").removeClass("selected");
		$(this).addClass("selected");
		var a = $("#tabcontents .content").get(index);
		$(a).addClass("selected");

	});
});
