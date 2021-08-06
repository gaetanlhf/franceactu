function changeCards(btnId, cards) {
	document.getElementById("intro").classList.add("fadeOut")

	setTimeout(function() {
		document.getElementById("intro").classList.add("d-none")

	}, 300);

	allNavBtn = document.querySelectorAll(".nav-link");
	allCards = document.querySelectorAll(".newscards");
	idCards = document.querySelectorAll("." + cards);

	allNavBtn.forEach(function(ele) {
		ele.classList.remove("active");
	});

	btnId.classList.add("active")
	
	allCards.forEach(function(ele) {
		ele.classList.remove("fadeIn");
		ele.classList.add("fadeOut");
		setTimeout(function() {
		ele.classList.add("d-none");
	}, 300);
	});
	setTimeout(function() {
	idCards.forEach(function(ele) {
		ele.classList.remove("fadeOut");
		ele.classList.remove("d-none");
		ele.classList.add("fadeIn");
	});
}, 300);
}



