$(document).ready(() => {
	// Create the click event to toggle the display of the archive year/months.
	$(".archive-bar .year > div, .archive-bar .month > div").click(e => {
		$(e.target).parent().toggleClass("closed")
	});
});
