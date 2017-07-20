var abilities;
var tactics;

$(document).ready(() => {
	abilities = $("li.ability, li.ability > .description > span");
	tactics = $("li.tactic, li.tactic > .description > span:not(.ability)");
	var difficultyToggles = $(".difficulty-toggle > span");
	difficultyToggles.click({"toggles": difficultyToggles, "toggleHandler": handleDifficultyToggle}, handleToggle);
	var roleToggles = $(".role-toggle > span");
	roleToggles.click({"toggles": roleToggles, "toggleHandler": handleRoleToggle}, handleToggle);

	var defaultDifficulty = Cookies.get("difficulty") || "normal";
	var defaultRole = Cookies.get("role") || "rdps";

	difficultyToggles.filter("*[toggle-val='" + defaultDifficulty + "']").first().trigger("click");
	roleToggles.filter("*[toggle-val='" + defaultRole + "']").first().trigger("click");
});

function handleToggle(e) {
	var toggle = $(e.target);
	if(toggle.hasClass("selected")) {
		return;
	}

	e.data.toggles.removeClass("selected");

	var toggleValue = toggle.attr("toggle-val");

	e.data.toggles.filter("*[toggle-val='" + toggleValue + "']").addClass("selected");

	e.data.toggleHandler(toggleValue);
}

function handleRoleToggle(role) {
	tactics.removeClass("first");
	var matchingTactics = tactics.filter(".role-" + role);
	matchingTactics.eq(0).addClass("first");
	matchingTactics.removeClass("role-hidden");
	tactics.not(".role-" + role + ", .role-all").addClass("role-hidden");

	Cookies.set("role", role);
}

function handleDifficultyToggle(difficulty) {
	abilities.removeClass("first");
	tactics.removeClass("first");

	var matchingAbilities = abilities.filter(".difficulty-" + difficulty);
	matchingAbilities.eq(0).addClass("first");
	matchingAbilities.removeClass("difficulty-hidden");
	abilities.not(".difficulty-" + difficulty + ", .difficulty-all").addClass("difficulty-hidden");

	var matchingTactics = tactics.filter(".difficulty-" + difficulty);
	matchingTactics.eq(0).addClass("first");
	matchingTactics.removeClass("difficulty-hidden");
	tactics.not(".difficulty-" + difficulty + ", .difficulty-all").addClass("difficulty-hidden");

	Cookies.set("difficulty", difficulty);
}
