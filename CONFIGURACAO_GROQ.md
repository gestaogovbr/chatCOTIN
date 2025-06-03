# Configuração do Groq Cloud (Llama-3.3-70B-Versatile)

## Terceira Opção de Modelo de IA Implementada

Agora o ChatCOTIN suporta três modelos de IA:

1. **llama3.2:latest** - Modelo Local (Ollama)
2. **databricks-llama-4-maverick** - Nuvem (Databricks)
3. **llama-3.3-70b-versatile** - Groq Cloud ⭐ **NOVO**

## Configuração da API Key do Groq

### 1. Obter a API Key

1. Acesse [https://console.groq.com](https://console.groq.com)
2. Crie uma conta ou faça login
3. Navegue para "API Keys" no painel
4. Clique em "Create API Key"
5. Copie a chave gerada

### 2. Configurar Variável de Ambiente

Adicione a variável de ambiente ao seu sistema:

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="sua_api_key_aqui"
```

**Windows (CMD):**
```cmd
set GROQ_API_KEY=sua_api_key_aqui
```

**Linux/Mac:**
```bash
export GROQ_API_KEY="sua_api_key_aqui"
```

### 3. Configuração Permanente

Para configuração permanente, adicione a variável ao arquivo `.env` do projeto:

```env
GROQ_API_KEY=sua_api_key_aqui
```

## Especificações Técnicas do Modelo

- **Modelo**: llama-3.3-70b-versatile
- **Parâmetros**: 70 bilhões
- **Janela de Contexto**: 128K tokens
- **Tokens de Saída Máximos**: 32,768
- **Velocidade**: ~275 TPS (Tokens por Segundo)
- **Arquitetura**: Transformer otimizado com Grouped-Query Attention (GQA)

## Performance e Benchmarks

- **MMLU**: 86.0% de precisão
- **HumanEval**: 88.4% pass@1 (geração de código)
- **MATH**: 77.0% sympy intersection score
- **MGSM**: 91.1% exact match (matemática multilíngue)

## Casos de Uso Ideais

- **Compreensão Avançada de Linguagem**: Capacidades multilíngues fortes
- **Geração de Código**: Excelente desempenho em programação
- **Resolução de Problemas Matemáticos**: Alta precisão em cálculos
- **Análise de Dados**: Processamento complexo de informações

## Custos (Referência)

- **Tokens de Entrada**: $0.59 por 1M tokens
- **Tokens de Saída**: $0.79 por 1M tokens

## Funcionalidades Suportadas

✅ **Tool Use**: Suportado  
✅ **JSON Mode**: Suportado  
❌ **Suporte a Imagens**: Não suportado  

## Como Usar

1. Certifique-se de que a variável `GROQ_API_KEY` está configurada
2. No ChatCOTIN, vá em **Configurações** (ícone de engrenagem)
3. Selecione **llama-3.3-70b-versatile (Groq Cloud)**
4. Clique em **Salvar Configurações**
5. Comece a conversar!

## Vantagens do Modelo Groq

- **Velocidade Extrema**: Inferência muito rápida (~275 TPS)
- **Qualidade Alta**: 70B parâmetros para respostas precisas
- **Eficiência**: Otimizado para produção
- **Multilíngue**: Excelente suporte ao português
- **Contexto Amplo**: 128K tokens de janela de contexto

## Troubleshooting

### Erro: "GROQ_API_KEY não está configurada"
- Verifique se a variável de ambiente está definida
- Reinicie o servidor Django após configurar
- Verifique se não há espaços extras na chave

### Erro de Conexão
- Verifique sua conexão com a internet
- Confirme se a API Key está válida
- Verifique se não ultrapassou os limites de uso

## Integração Técnica

A integração foi implementada mantendo toda a funcionalidade existente:

- **RAG (Retrieval-Augmented Generation)**: Totalmente suportado
- **Busca Semântica**: Funciona normalmente
- **Histórico de Conversas**: Mantido
- **Template Unificado**: Usa o mesmo prompt do ChatCOTIN
- **Regeneração de Respostas**: Suportada

A implementação garante que você tenha todas as funcionalidades do ChatCOTIN com a performance excepcional do Groq Cloud. 