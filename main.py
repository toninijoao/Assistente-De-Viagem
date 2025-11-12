import os, json, re
from google import genai
from dotenv import load_dotenv

os.system('cls' if os.name == 'nt' else 'clear')

load_dotenv()

api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("Erro: API_KEY não encontrada!")


client = genai.Client(api_key=api_key)
chat = client.chats.create(model="gemini-2.5-flash")

while True:
    print("🎒 Olá! Sou o seu NOVO Assistente de VIAGEM! 🎒\n\n")

    destino = input("📍 Qual será o seu Destino? \n💬 Seu Destino: ")

    origem = input("\n📍E irá sair de onde?\n💬 Seu Ponto de Partida: ")

    promptpergunta = (
        f"Calcule a distância rodoviária (por estradas) entre {origem} e {destino}, "
        "em quilômetros. "
        "Responda APENAS com um número decimal representando a distância total em KM, "
        "sem texto adicional, sem unidade e sem explicação."
        )
    resposta = chat.send_message(promptpergunta)
    distancia = resposta.text.strip()
    numero_encontrado = re.search(r'\d+[\.,]?\d*', distancia)
    if numero_encontrado:
        distancia = float(numero_encontrado.group().replace(',', '.'))
    else:
        print(f"\n Não foi possível extrair a distância da resposta!")
        continue


    carro = input(f"\n🚙 Qual carro você irá usar para ir de {origem} até {destino}?\n💬 Carro: ")
    promptcarro = (
        f"Qual é a autonomia média de um {carro} em KM/L? em gasolina"
        "Responda com apenas uma casa decimal(exemplo: 12.5)"
    )
    respostacarro = chat.send_message(promptcarro)
    autonomia = respostacarro.text.strip()
    numero_encontrado = re.search(r'\d+[\.,]?\d*', autonomia)
    if numero_encontrado:
        autonomia = float(numero_encontrado.group().replace(',', '.'))
    else:
        print(f"\n Não foi possível extrair a autonomia da resposta!")
        continue

    gasto = distancia / autonomia
    valor = gasto * 6.39
    print(f"\n⛽ Com o seu {carro}, que tem uma autonomia de {autonomia} KM com 1 litro de gasolina, você gastará {gasto} Litros de Gasolina para percorrer o trajeto de {distancia} KM entre {origem} e {destino}.\n💰 Considerando o preço médio da Gasolina em Outubro de 2025(R$6,39), você gastará aproximadamente R${valor:.2f} em Combustível")

    perguntarota = input(f"\n\n🛣️ Gostaria de saber qual é a melhor rota para ir de {origem} até {destino}? (sim/não)")

    if perguntarota.lower() == 'sim':
        promprota = (f"Encontre a rota de carro mais rápida entre {origem} e {destino}."
                     "Você é um assistente de rotas."
                     "Responda APENAS com um objeto JSON, sem ```json ou markdown."
                     "O JSON deve conter exatamente uma chave:"
                     "'cidades_rota': uma lista de strings contendo as *principais* cidades e municípios na ordem da rota (sem incluir a origem e o destino)."   
                     )
        
        respostarota = chat.send_message(promprota)
        rota = respostarota.text.strip()

        try:
            dados_rota = json.loads(rota)
            cidades_rota = dados_rota["cidades_rota"]

            print(f"\n🛣️ Cidades na Rota de {origem} até {destino}: ")
            for cidade in cidades_rota:
                print(f"-> {cidade}")
                
        except json.JSONDecodeError:
            print("\nErro! A resposta não está no formato esperado.")

    else:
        print("\nOk!\n")

    tempo = distancia / 110

    pergunta_tempo =input(f"\nGostaria de saber quanto tempo irá demorar a viagem de {origem} a {destino}? (sim/não)")
    if pergunta_tempo.lower() == 'sim':
        horas = int(tempo)
        minutos = ((tempo - horas) * 60)

        print(f"\n⏰ A viagem de {origem} a {destino} terá uma duração aproximada de {horas} horas e {minutos:.2f} minutos. (levando em consideração que a velocidade média de carro será de 110 km/h). ⏰\n")
    else:
        print("\nOk!\n")

    continuar = input("Deseja continuar usando o Assistente de Viagem? (sim/não): \nSua Resposta: ")
    if continuar.lower() != 'sim':
        print("Obrigado por usar o Assistente de Viagem! Até a próxima! 👋")
        break
