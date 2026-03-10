document.addEventListener('DOMContentLoaded', () => {
    const converterBtn = document.getElementById('converter-btn');
    const valorJpyInput = document.getElementById('valor-jpy');
    const pesoGramasInput = document.getElementById('peso-gramas');
    
    const resultsArea = document.getElementById('results-area');
    const convertidoText = document.getElementById('convertido-text');
    const finalText = document.getElementById('final-text');
    
    const errorMessage = document.getElementById('error-message');

    // Função para formatar moeda em BRL
    const formatarBRL = (valor) => {
        return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    };

    // Função para formatar moeda em JPY
    const formatarJPY = (valor) => {
        return valor.toLocaleString('ja-JP', { style: 'currency', currency: 'JPY' });
    };

    converterBtn.addEventListener('click', async () => {
        // Obter valores
        const valorJpy = parseFloat(valorJpyInput.value);
        const pesoGramas = parseFloat(pesoGramasInput.value);

        // Limpar estados anteriores
        resultsArea.classList.add('hidden');
        errorMessage.classList.add('hidden');
        errorMessage.textContent = '';

        // Validação básica do frontend
        if (!valorJpy || valorJpy <= 0) {
            errorMessage.textContent = "Por favor, digite um valor em Yenes válido.";
            errorMessage.classList.remove('hidden');
            return;
        }

        if (!pesoGramas || pesoGramas <= 0) {
            errorMessage.textContent = "Por favor, digite um peso em gramas válido.";
            errorMessage.classList.remove('hidden');
            return;
        }

        // Mostrar estado de carregamento (opcional, mas bom)
        converterBtn.textContent = "CALCULANDO...";
        converterBtn.disabled = true;

        try {
            // Fazer a chamada para a API serverless da Vercel
            // A Vercel mapeia automaticamente a pasta /api para chamadas de API
            const response = await fetch('/api/index', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    valor: valorJpy,
                    peso: pesoGramas
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Sucesso: Exibir resultados
                convertidoText.textContent = `${formatarJPY(data.jpy_origin)} JPY equivale a ${formatarBRL(data.brl_converted)}`;
                finalText.textContent = `Valor final com cálculos adicionais: ${formatarBRL(data.final_result)}`;
                resultsArea.classList.remove('hidden');
            } else {
                // Erro do backend (ex: valor <= 0)
                errorMessage.textContent = `Erro do servidor: ${data.error || "Ocorreu um erro desconhecido."}`;
                errorMessage.classList.remove('hidden');
            }
        } catch (error) {
            // Erro de rede ou de requisição
            errorMessage.textContent = `Erro de conexão: ${error.message}`;
            errorMessage.classList.remove('hidden');
        } finally {
            // Restaurar botão
            converterBtn.textContent = "CONVERTER";
            converterBtn.disabled = false;
        }
    });
});
