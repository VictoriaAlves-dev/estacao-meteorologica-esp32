
/*1. RELÓGIO E DATA */

function atualizarRelogio() {
    const agora = new Date();

    const horario = agora.toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    });

    const data = agora.toLocaleDateString("pt-BR", {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric"
    });

    document.getElementById("relogio").textContent = horario;
    document.getElementById("data-atual").textContent = data;
}

atualizarRelogio();
setInterval(atualizarRelogio, 1000);

/*  2. FUNDO DINÂMICO CONFORME O HORÁRIO */

const periodos = {
    morning: {
        imagem: "https://images.unsplash.com/photo-1706381778245-7fd5305c18b3?w=1600&h=900&fit=crop&auto=format",
        sobreposicao: "linear-gradient(160deg, rgba(10,30,80,.45), rgba(0,0,0,.20))",
        animacao: "kb-zoom-in"
    },

    afternoon: {
        imagem: "https://images.unsplash.com/photo-1599209248411-5124adbb1da2?w=1600&h=900&fit=crop&auto=format",
        sobreposicao: "linear-gradient(180deg, rgba(0,30,80,.30), rgba(0,0,0,.25))",
        animacao: "kb-pan-right"
    },

    evening: {
        imagem: "https://images.unsplash.com/photo-1505051508008-923feaf90180?w=1600&h=900&fit=crop&auto=format",
        sobreposicao: "linear-gradient(180deg, rgba(30,10,40,.35), rgba(50,15,10,.45))",
        animacao: "kb-zoom-out"
    },

    night: {
        imagem: "https://images.unsplash.com/photo-1608723724315-5e421874d7e9?w=1600&h=900&fit=crop&auto=format",
        sobreposicao: "linear-gradient(160deg, rgba(5,5,20,.60), rgba(0,0,0,.65))",
        animacao: "kb-pan-left"
    }
};

let periodoAtual = "";

function identificarPeriodo(hora) {
    if (hora >= 6 && hora < 12) {
        return "morning";
    }

    if (hora >= 12 && hora < 17) {
        return "afternoon";
    }

    if (hora >= 17 && hora < 20) {
        return "evening";
    }

    return "night";
}

function atualizarFundo() {
    const periodo = identificarPeriodo(new Date().getHours());

    if (periodo === periodoAtual) {
        return;
    }

    periodoAtual = periodo;

    const config = periodos[periodo];
    const body = document.body;

    body.style.setProperty(
        "--weather-image",
        `url("${config.imagem}")`
    );

    body.style.setProperty(
        "--weather-overlay",
        config.sobreposicao
    );

    body.style.setProperty(
        "--weather-animation",
        config.animacao
    );

    body.classList.remove("bg-changing");

    // Reinicia a animação de transição.
    void body.offsetWidth;

    body.classList.add("bg-changing");

    setTimeout(() => {
        body.classList.remove("bg-changing");
    }, 1300);
}

atualizarFundo();
setInterval(atualizarFundo, 30000);


/* 3. STATUS DA CONEXÃO MQTT */

function atualizarStatusMQTT(estado, mensagem) {
    const status = document.getElementById("status-mqtt");
    const texto = document.getElementById("texto-status");

    if (!status || !texto) {
        return;
    }

    status.dataset.state = estado;
    texto.textContent = mensagem;
}

// Ainda não existe conexão MQTT implementada.
atualizarStatusMQTT(
    "disconnected",
    "MQTT não configurado"
);


/* 4. MEDIÇÕES REAIS (Integradas com a API Python) */

async function atualizarMedicoes() {
    try {
        const resposta = await fetch("http://localhost:8000/clima/climaAtual");
        
        if (!resposta.ok) {
            throw new Error("Não foi possível buscar os dados da API.");
        }

        const respostaJson = await resposta.json();
        const dados = respostaJson.climaAtual && respostaJson.climaAtual.length > 0 
            ? respostaJson.climaAtual[0] 
            : null;

        if (!dados) {
            throw new Error("Nenhum dado de clima encontrado na base de dados.");
        }

        document.getElementById("temperatura-principal").textContent = `${dados.temperatura}°C`;
        document.getElementById("temperatura").textContent = `${dados.temperatura}°C`;
        document.getElementById("umidade").textContent = `${dados.umidade}%`;
        document.getElementById("indice-uv").textContent = dados.indiceUV;

        const agora = new Date();
        document.getElementById("ultima-atualizacao").textContent = 
            `Última atualização: ${agora.toLocaleTimeString("pt-BR")}`;

        atualizarStatusMQTT("connected", "Conectado ao Sistema");

    } catch (erro) {
        console.error("Erro ao atualizar medições:", erro);
        atualizarStatusMQTT("disconnected", "Aguardando dados...");
        
        // Zera ou limpa os números no front-end quando a base está vazia
        document.getElementById("temperatura-principal").textContent = "--°C";
        document.getElementById("temperatura").textContent = "--°C";
        document.getElementById("umidade").textContent = "--%";
        document.getElementById("indice-uv").textContent = "--";
    }
}
atualizarMedicoes();

setInterval(atualizarMedicoes, 5000);