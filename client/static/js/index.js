document.addEventListener("DOMContentLoaded", () => {
	// Elementi del DOM
	const manualCheck = document.getElementById("manualCheck");
	const autoCheck = document.getElementById("autoCheck");
	const manualLumos = document.getElementById("manualLumos");
	const manualTemp = document.getElementById("manualTemp");
	const autoLumos = document.getElementById("autoLumos");
	const autoTemp = document.getElementById("autoTemp");
	const manualButton = document.getElementById("manualButton");
	const autoButton = document.getElementById("autoButton");

	// Funzione per mostrare la notifica
	const showNotification = (message) => {
		notification.textContent = message; // Aggiorna il messaggio
		notification.classList.add("show"); // Mostra la notifica
		setTimeout(() => {
			notification.classList.remove("show"); // Nasconde la notifica dopo 5 secondi
		}, 5000);
	};

	// Funzione per aggiornare lo stato dei pulsanti e degli input
	const updateState = () => {
		const isManualChecked = manualCheck.checked;
		const isAutoChecked = autoCheck.checked;

		// Stato modalità manuale
		manualLumos.disabled = !isManualChecked;
		manualTemp.disabled = !isManualChecked;
		manualButton.disabled = !isManualChecked;
		manualButton.style.backgroundColor = isManualChecked
			? "var(--bs-warning)"
			: "gray";

		//I pulsanti sono inizialmente disattivati. La funzione updateState garantisce che i pulsanti e
		//gli input siano abilitati/disabilitati in base allo stato delle checkbox.

			// Stato modalità automatica
		autoLumos.disabled = !isAutoChecked;
		autoTemp.disabled = !isAutoChecked;
		autoButton.disabled = !isAutoChecked;
		autoButton.style.backgroundColor = isAutoChecked
			? "var(--bs-warning)"
			: "gray";

		//Quando una checkbox viene deselezionata, il pulsante associato viene disattivato immediatamente,
			//e la funzione updateState si occupa di aggiornare il colore e lo stato.
	};

	// Listener per la checkbox "Manuale"
	manualCheck.addEventListener("change", () => {
		if (manualCheck.checked) {
			autoCheck.checked = false; // Deseleziona l'altra checkbox
		}
		updateState();
	});

	// Listener per la checkbox "Automatica"
	autoCheck.addEventListener("change", () => {
		if (autoCheck.checked) {
			manualCheck.checked = false; // Deseleziona l'altra checkbox
		}
		updateState();
	});


	// Funzione per inviare i dati tramite i pulsanti INVIA
	const handleSendMessage = async (mode) => {
		//con il lamba controlla il valore mode della checkbox
		const brightness = mode === "manual" ? manualLumos.value : autoLumos.value; //se è manuale mette il valore dello slider, altrimenti della form (forma if compatta)
		const temperature = mode === "manual" ? manualTemp.value : autoTemp.value;

		const payload = {
			mode,
			brightness: parseInt(brightness, 10), //convertire in valore intero
			temperature: parseInt(temperature, 10),
		};

		try {
			const response = await fetch("/send", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(payload),
			});
			const result = await response.json();
		} catch (error) {}
		showNotification("INVIATO!");
	};

	// Event listener per i pulsanti INVIA
	manualButton.addEventListener("click", () => handleSendMessage("manual")); //chiamata ricorsiva in base a quale click del pulsante
	autoButton.addEventListener("click", () => handleSendMessage("automatic"));

	// Inizializza lo stato
	updateState();
});
