# 📚 Como Atualizar a Base de Conhecimento do ChatCOTIN

Este guia explica como utilizar o script `atualizar_base_conhecimento.py` para incluir novos documentos na base de conhecimento do ChatCOTIN.

## 🎯 Para que serve?

O ChatCOTIN utiliza RAG (Retrieval-Augmented Generation) para responder perguntas baseadas em documentos específicos sobre:
- API de Dados Abertos do Governo Federal
- Portal Compras.gov.br
- Lei de Acesso à Informação (LAI)
- Transparência Pública

Sempre que você adicionar novos documentos, precisa rodar este script para que o ChatCOTIN "aprenda" o novo conteúdo.

## 📂 Formatos Suportados

O script processa automaticamente estes tipos de arquivo:

| Formato | Extensão | Descrição |
|---------|----------|-----------|
| **Microsoft Word** | `.docx` | Documentos oficiais, manuais, especificações |
| **Markdown** | `.md` | Documentação técnica, READMEs |
| **Texto Simples** | `.txt` | Arquivos de texto puro |

## 🚀 Como Usar

### Passo 1: Adicionar Documentos
Coloque seus novos documentos na pasta `Docs/`:
```
Docs/
├── documento_existente.docx
├── novo_manual.docx          ← NOVO
├── especificacoes_api.md     ← NOVO
└── lista_endpoints.txt       ← NOVO
```

### Passo 2: Executar o Script
No terminal, na pasta do projeto:
```bash
python atualizar_base_conhecimento.py
```

### Passo 3: Aguardar o Processamento
O script mostrará o progresso:
```
🚀 CHATCOTIN - Atualização da Base de Conhecimento
============================================================

📂 Documentos encontrados:
  📄 7 arquivos Word (.docx)
  📝 2 arquivos Markdown (.md)  
  📋 1 arquivos Texto (.txt)
  📊 Total: 10 documentos

🔄 Processando documentos...
  📄 Processando Word: manual_api.docx
    ✅ Extraído: 15,432 caracteres
  📝 Processando Markdown: especificacoes.md
    ✅ Extraído: 8,756 caracteres
...

✂️ Dividindo em chunks para processamento...
    ✅ Criados 89 chunks otimizados

🧠 Criando embeddings multilíngues...
💾 Salvando no ChromaDB...
✅ Base de conhecimento criada com sucesso!

🔍 Testando base de conhecimento...
  ✅ 'módulos da API': 2 resultado(s)
  ✅ 'transparência pública': 2 resultado(s)
...

🎉 ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!
   📄 10 documentos indexados
   🔍 Base pronta para consultas do ChatCOTIN
```

## ⚙️ O que o Script Faz Internamente

1. **🔍 Escaneia** a pasta `Docs/` procurando arquivos suportados
2. **📄 Extrai** texto de cada documento (incluindo tabelas em Word)
3. **✂️ Fragmenta** o texto em chunks otimizados para português
4. **🧠 Cria embeddings** usando modelo multilíngue especializado
5. **💾 Salva** tudo no banco vetorial ChromaDB
6. **🔍 Testa** se as consultas funcionam corretamente
7. **🗄️ Faz backup** do banco antigo antes de substituir

## 🛡️ Segurança e Backup

- ✅ **Backup automático**: O banco antigo é preservado antes da atualização
- ✅ **Validação**: Testa se os documentos foram indexados corretamente
- ✅ **Rollback**: Se algo der errado, o banco antigo ainda existe

## 🐛 Resolução de Problemas

### ❌ Erro: "Pasta Docs não encontrada"
**Solução**: Certifique-se de que existe uma pasta `Docs/` no projeto e que contém documentos.

### ❌ Erro: "Nenhum documento suportado encontrado"
**Solução**: Verifique se os arquivos têm extensões corretas (`.docx`, `.md`, `.txt`).

### ❌ Erro ao processar arquivo Word
**Possíveis causas**:
- Arquivo corrompido ou protegido por senha
- Formato muito antigo (.doc em vez de .docx)

**Solução**: Converta para .docx no Word ou use formato .txt/.md

### ❌ Erro de memória durante processamento
**Solução**: 
- Reduza o tamanho dos documentos
- Divida documentos grandes em arquivos menores
- Reinicie o computador para liberar memória

### ❌ ChatCOTIN não encontra informações após atualização
**Verificações**:
1. O script terminou com "ATUALIZAÇÃO CONCLUÍDA COM SUCESSO"?
2. Os testes de consulta mostraram resultados positivos?
3. Reinicie o servidor Django: `python manage.py runserver`

## 📊 Estatísticas Típicas

Para referência, uma base de conhecimento saudável tem:
- **7-15 documentos**: Cobertura boa dos temas principais
- **300-500 chunks**: Granularidade adequada para busca
- **150-300 mil caracteres**: Volume suficiente de informações

## 🔄 Quando Executar

Execute o script sempre que:
- ✅ Adicionar novos documentos oficiais
- ✅ Atualizar versões de manuais existentes
- ✅ Incluir novas especificações da API
- ✅ O ChatCOTIN não conseguir responder sobre tópicos que deveriam estar na base

## 💡 Dicas Importantes

1. **Qualidade dos documentos**: Documentos bem estruturados geram melhores resultados
2. **Nomes descritivos**: Use nomes de arquivo que facilitem identificação
3. **Formatos recomendados**: 
   - `.docx` para documentos oficiais
   - `.md` para documentação técnica
   - `.txt` para listas e dados simples
4. **Teste sempre**: Após atualizar, faça algumas perguntas ao ChatCOTIN para validar

## 📞 Suporte

Em caso de problemas persistentes:
1. Verifique se todas as dependências estão instaladas (`pip install -r requirements.txt`)
2. Confirme se o ambiente virtual está ativo
3. Execute com `python -v atualizar_base_conhecimento.py` para logs detalhados

---

**Autor**: Sistema ChatCOTIN  
**Última atualização**: Janeiro 2025  
**Versão**: 1.0 