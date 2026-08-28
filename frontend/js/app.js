const API_URL = "http://127.0.0.1:8000";
const BOIA_ID = 7;

async function carregarPainel() {
	try {
		const response = await fetch(
			`${API_URL}/boias/${BOIA_ID}/painel`
		);

		if (!response.ok) {
			throw new Error("Erro ao buscar dados da boia.");
		}

		const data = await response.json();

		atualizarDashboard(data);

	} catch (error) {
		console.error(error);

		document.getElementById("nivel-risco").textContent =
			"Erro ao carregar";
	}
}

function atualizarDashboard(data) {

	const dashboard = data.dashboard;
	const tendencia = data.tendencia;

	const nivelRisco = document.getElementById("nivel-risco");

	nivelRisco.textContent = dashboard.nivel_atual;

	nivelRisco.classList.remove(
		"normal",
		"atencao",
		"risco"
	);

	nivelRisco.classList.add(
		dashboard.nivel_atual.toLowerCase()
	);

	document.getElementById("temperatura").textContent =
		`${dashboard.temperatura_media.toFixed(2)} °C`;

	document.getElementById("onda-media").textContent =
		`${dashboard.altura_onda_media.toFixed(2)} m`;

	document.getElementById("maior-onda").textContent =
		`${dashboard.maior_onda} m`;

	document.getElementById("vento-medio").textContent =
		dashboard.vento_medio.toFixed(2);

	document.getElementById("maior-vento").textContent =
		dashboard.maior_vento;

	document.getElementById("total-leituras").textContent =
		dashboard.total_leituras;

	document.getElementById("nivel-anterior").textContent =
		tendencia.nivel_anterior;

	document.getElementById("tendencia-atual").textContent =
		tendencia.tendencia;

	atualizarHistorico(data.historico_risco);
}

function atualizarHistorico(historico) {

	const container =
		document.getElementById("historico-lista");

	container.innerHTML = "";

	historico.forEach(item => {

		const div = document.createElement("div");

		div.className = "historico-item";

		const nivel = item.nivel.toLowerCase();

		const data = new Date(item.data_hora);

		const dataFormatada = data.toLocaleString("pt-BR");

		div.innerHTML = `
			<span>
				Leitura ${item.leitura_id}
			</span>

			<span>
				${dataFormatada}
			</span>

			<strong class="${nivel}">
				${item.nivel}
			</strong>
		`;

		container.appendChild(div);
	});
}

carregarPainel();
