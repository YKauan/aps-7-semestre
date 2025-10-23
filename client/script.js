document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'http://127.0.0.1:5000/indicadores';

    // Seletores do DOM
    const form = document.getElementById('indicador-form');
    const formTitle = document.getElementById('form-title');
    const indicadorIdInput = document.getElementById('indicador-id');
    const empresaInput = document.getElementById('empresa');
    const anoInput = document.getElementById('ano');
    const consumoAguaInput = document.getElementById('consumo_agua_m3');
    const residuosInput = document.getElementById('residuos_ton');
    const emissoesCo2Input = document.getElementById('emissoes_co2_ton');
    const listaIndicadores = document.getElementById('indicadores-lista');
    const loadingMessage = document.getElementById('loading-message');
    const submitButton = form.querySelector('button[type="submit"]');
    const cancelButton = document.getElementById('btn-cancelar');

    // Busca e renderiza os indicadores
    const fetchAndRenderIndicadores = async () => {
        loadingMessage.style.display = 'block';
        listaIndicadores.innerHTML = '';
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error('Erro ao buscar dados da API');
            const data = await response.json();
            
            loadingMessage.style.display = 'none';

            if (Object.keys(data).length === 0) {
                listaIndicadores.innerHTML = '<p>Nenhum indicador registrado ainda.</p>';
                return;
            }

            for (const id in data) {
                const indicador = data[id];
                const card = document.createElement('div');
                card.className = 'indicador-card';
                card.innerHTML = `
                    <h3>${indicador.empresa} - ${indicador.ano}</h3>
                    <p><strong>Consumo de Água:</strong> ${indicador.consumo_agua_m3} m³</p>
                    <p><strong>Geração de Resíduos:</strong> ${indicador.residuos_ton} ton</p>
                    <p><strong>Emissões de CO2:</strong> ${indicador.emissoes_co2_ton} ton</p>
                    <div class="card-actions">
                        <button class="btn-edit" data-id="${id}">Editar</button>
                        <button class="btn-delete" data-id="${id}">Excluir</button>
                    </div>
                `;
                listaIndicadores.appendChild(card);
            }
        } catch (error) {
            loadingMessage.style.display = 'none';
            listaIndicadores.innerHTML = `<p style="color: #ff4d4d;">${error.message}</p>`;
        }
    };

    // Reseta o formulario
    const resetForm = () => {
        form.reset();
        indicadorIdInput.value = '';
        formTitle.textContent = 'Adicionar Novo Indicador';
        submitButton.textContent = 'Adicionar Indicador';
        cancelButton.style.display = 'none';
    };

    // Envio do formulario Incluir / Alterar (submit)
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const indicadorData = {
            empresa: empresaInput.value,
            ano: parseInt(anoInput.value),
            consumo_agua_m3: parseFloat(consumoAguaInput.value),
            residuos_ton: parseFloat(residuosInput.value),
            emissoes_co2_ton: parseFloat(emissoesCo2Input.value),
        };

        const id = indicadorIdInput.value;
        const method = id ? 'PUT' : 'POST';
        const url = id ? `${API_URL}/${id}` : API_URL;

        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(indicadorData),
            });

            if (!response.ok) throw new Error(`Erro ao ${id ? 'atualizar' : 'salvar'} indicador.`);
            
            resetForm();
            fetchAndRenderIndicadores();

        } catch (error) {
            alert(error.message);
        }
    });

    // Manipula edicao / exclusao
    listaIndicadores.addEventListener('click', async (e) => {
        const target = e.target;
        const id = target.dataset.id;

        if (!id) return;

        // Acao de excluir
        if (target.classList.contains('btn-delete')) {
            if (confirm('Tem certeza que deseja excluir este indicador?')) {
                try {
                    const response = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
                    if (!response.ok) throw new Error('Erro ao excluir indicador.');
                    fetchAndRenderIndicadores();
                } catch (error) {
                    alert(error.message);
                }
            }
        }

        // Acao de editar
        if (target.classList.contains('btn-edit')) {
            try {
                const response = await fetch(`${API_URL}/${id}`);
                if (!response.ok) throw new Error('Não foi possível carregar dados para edição.');
                const indicador = await response.json();
                
                // Preenche o formulario
                indicadorIdInput.value = id;
                empresaInput.value = indicador.empresa;
                anoInput.value = indicador.ano;
                consumoAguaInput.value = indicador.consumo_agua_m3;
                residuosInput.value = indicador.residuos_ton;
                emissoesCo2Input.value = indicador.emissoes_co2_ton;

                // Ajusta a UI para o modo de edicao
                formTitle.textContent = 'Editando Indicador';
                submitButton.textContent = 'Salvar Alterações';
                cancelButton.style.display = 'inline-block';
                window.scrollTo({ top: 0, behavior: 'smooth' });

            } catch (error) {
                alert(error.message);
            }
        }
    });

    // Cancela edicao
    cancelButton.addEventListener('click', resetForm);

    // Carga inicial dos dados
    fetchAndRenderIndicadores();
});