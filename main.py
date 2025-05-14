import spacy

# Carrega modelo com vetores semânticos
nlp = spacy.load("pt_core_news_lg")

# Frases de referência para cada INTENT
intents_examples = {
    "1": ["quero ver meu histórico escolar", "histórico", "cursadas",  "disciplinas que já cursei", "lista de matérias feitas"],
    "2": ["qual o horário das aulas", "horário", "horas", "ver calendário das aulas", "quando são minhas aulas" , "quando"],
    "3": ["ver minhas notas", "notas", "provas", "quero saber minhas provas", "quanto tirei na avaliação", "desempenho"],
    "4": ["preciso de um comprovante de matrícula", "matrícula", "quero declaração da faculdade", "declaração de vínculo"],
    "5": ["trancar uma matéria", "trancar", "trancamento", "informações sobre trancamento", "trancar disciplina"],
    "6": ["datas importantes do período", "quais são os prazos", "informações do calendário acadêmico"],
    "7": ["quero falar com a secretaria", "secretária", "preciso de ajuda com atendimento", "entrar em contato com a secretaria"],
    "8": ["dúvidas sobre estágio", "estágio",  "como funciona o estágio obrigatório", "orientações de estágio"],
    "9": ["como conseguir bolsa de permanência", "bolsa",  "ajuda financeira estudantil", "bolsas para continuar o curso"],
    "10": ["quero ser monitor", "informações sobre iniciação científica", "bolsa IC ou monitoria", "monitoria", "bolsa", "iniciação científica", "ic"]
}

intents_map = {
    "1": "Consultar histórico escolar",
    "2": "Verificar horários de aulas",
    "3": "Consultar notas de disciplinas",
    "4": "Solicitar declaração de matrícula",
    "5": "Obter informações sobre trancamento de disciplinas",
    "6": "Informações sobre datas dentro do período",
    "7": "Falar com a secretaria",
    "8": "Receber orientações para estágio",
    "9": "Solicitar informações sobre bolsas de permanência",
    "10": "Solicitar informações sobre bolsas financeiras (Monitoria, IC)"
}

# Tópicos gerais agrupando intents
grupos = {
    "matérias": ["2", "3"],
    "matricula": ["1", "4", "5"],
    "datas": ["6"],
    "bolsa": ["8", "9", "10"],
    "secretaria": ["7"]
}

def detectar_intent_por_similaridade(mensagem_usuario):
    doc_user = nlp(mensagem_usuario.lower())
    max_sim = 0
    melhor_intent = None
    for intent_id, exemplos in intents_examples.items():
        for exemplo in exemplos:
            doc_exemplo = nlp(exemplo)
            similaridade = doc_user.similarity(doc_exemplo)
            if similaridade > max_sim:
                max_sim = similaridade
                melhor_intent = intent_id
    if max_sim > 0.70:
        return melhor_intent, max_sim, doc_user
    return None, max_sim, doc_user

def perguntar_grupo_baseado_similaridade(doc_usuario):
    max_sim = 0
    grupo_mais_provavel = None
    for grupo in grupos:
        doc_grupo = nlp(grupo)
        sim = doc_usuario.similarity(doc_grupo)
        if sim > max_sim:
            max_sim = sim
            grupo_mais_provavel = grupo

    if grupo_mais_provavel:
        resposta = input(f"Sua dúvida é sobre {grupo_mais_provavel}? (sim/não/sair): ").strip().lower()
        if resposta == "sair":
            print("Bot: Encerrando. Até logo! 👋")
            exit()
        if resposta == "sim":
            intents = grupos[grupo_mais_provavel]
            for i in intents:
                resposta2 = input(f"Você quer: {intents_map[i]}? (sim/não/sair): ").strip().lower()
                if resposta2 == "sair":
                    print("Bot: Encerrando. Até logo! 👋")
                    exit()
                if resposta2 == "sim":
                    print(f"✅ INTENT {i}: {intents_map[i]}")
                    return
        print("Bot: Não consegui identificar com clareza. Vamos tentar novamente.")
        descobrir_intent_por_perguntas()


def descobrir_intent_por_perguntas():
    for grupo, intents in grupos.items():
        resposta = input(f"Sua dúvida é sobre {grupo}? (sim/não/sair): ").strip().lower()
        if resposta == "sair":
            print("Bot: Encerrando. Até logo! 👋")
            exit()
        if resposta == "sim":
            for i in intents:
                resp = input(f"Você quer: {intents_map[i]}? (sim/não/sair): ").strip().lower()
                if resp == "sair":
                    print("Bot: Encerrando. Até logo! 👋")
                    exit()
                if resp == "sim":
                    print(f"✅ INTENT {i}: {intents_map[i]}")
                    return
    print("Bot: Desculpe, não consegui entender sua dúvida.")

def chatbot():
    print("🤖 Olá! Sou a assistente virtual da sua faculdade.")
    print("Digite sua dúvida (ou 'sair' para encerrar):")
    while True:
        mensagem = input("Você: ")
        if mensagem.lower() in ["sair", "exit", "fim"]:
            print("Bot: Até logo! 👋")
            break

        intent, confianca, doc_user = detectar_intent_por_similaridade(mensagem)
        if intent:
            resposta = input(f"Bot: Você quis dizer: {intents_map[intent]}? (sim/não/sair): ").strip().lower()
            if resposta == "sim":
                print(f"✅ INTENT {intent}: {intents_map[intent]}")
            elif resposta == "sair":
                print("Bot: Até logo! 👋")
                break
            else:
                print("Bot: Tudo bem, vamos tentar entender melhor com base no que você falou...")
                perguntar_grupo_baseado_similaridade(doc_user)
        else:
            print("Bot: Não entendi bem sua dúvida. Vamos por partes.")
            descobrir_intent_por_perguntas()

# Rodar
if __name__ == "__main__":
    chatbot()
