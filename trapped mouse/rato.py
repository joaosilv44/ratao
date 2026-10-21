import os
import time


class LabirintoRato:
    def __init__(self, labirinto):
        self.labirinto = labirinto
        self.pilha = []
        self.visitados = []
        self.caminho = []

    def encontrar_caminho(self, inicio, fim):
        self.pilha.append(inicio)
        self.visitados.append(inicio)

        while self.pilha:
            posicao_atual = self.pilha.pop()
            self.caminho.append(posicao_atual)

            self.desenhar_labirinto_terminal(posicao_atual, inicio, fim)
            time.sleep(0.4)

            if posicao_atual == fim:
                return self.caminho

            for vizinho in self.obter_vizinhos(posicao_atual):
                if (
                    vizinho not in self.visitados
                    and self.labirinto[vizinho[0]][vizinho[1]] != 1
                ):
                    self.pilha.append(vizinho)
                    self.visitados.append(vizinho)

        return None

    def obter_vizinhos(self, posicao):
        x, y = posicao
        vizinhos = []

        # Ordem dos movimentos: cima, baixo, esquerda, direita
        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in movimentos:
            novo_x = x + dx
            novo_y = y + dy

            if (
                0 <= novo_x < len(self.labirinto)
                and 0 <= novo_y < len(self.labirinto[0])
            ):
                vizinhos.append((novo_x, novo_y))

        return vizinhos

    def desenhar_labirinto_terminal(self, posicao_do_rato, inicio, fim):
        # Limpa a tela do terminal
        os.system("cls" if os.name == "nt" else "clear")

        VERMELHO = "\033[91m"
        VERDE = "\033[92m"
        AMARELO = "\033[93m"
        CINZA = "\033[90m"
        RESET = "\033[0m"

        # Símbolos usados no desenho
        RATO = f"{VERMELHO} 🐭 {RESET}"
        PAREDE = f"{CINZA} ██ {RESET}"
        CAMINHO = "    "
        VISITADO = f"{AMARELO}  · {RESET}"
        SAIDA = f"{VERDE} 🚩 {RESET}"

        largura_borda = len(self.labirinto[0]) * 4 + 2

        print("╔" + "═" * largura_borda + "╗")
        print("║ " + f"{VERMELHO} 🐭 RATO {RESET}".center(30) + "║")
        print("╠" + "═" * largura_borda + "╣")

        for i in range(len(self.labirinto)):
            linha_visual = "║ "

            for j in range(len(self.labirinto[i])):
                posicao = (i, j)

                if posicao == posicao_do_rato:
                    linha_visual += RATO
                elif posicao == fim:
                    linha_visual += SAIDA
                elif self.labirinto[i][j] == 1:
                    linha_visual += PAREDE
                elif posicao in self.visitados:
                    linha_visual += VISITADO
                else:
                    linha_visual += CAMINHO

            linha_visual += " ║"
            print(linha_visual)

        print("╚" + "═" * largura_borda + "╝")

    def imprimir_caminho(self):
        for posicao in self.caminho:
            print(posicao)


def carregar_labirinto(nome_arquivo):
    labirinto = []

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            valores = [int(caractere) for caractere in linha if caractere in "01"]

            if valores:
                labirinto.append(valores)

    if not labirinto:
        raise ValueError("O arquivo não contém um labirinto.")

    largura = len(labirinto[0])

    for numero_linha, linha in enumerate(labirinto, start=1):
        if len(linha) != largura:
            raise ValueError(
                f"A linha {numero_linha} tem tamanho diferente das demais."
            )

    return labirinto


labirinto = carregar_labirinto("labirinto.txt")

inicio = (0, 0)
fim = (4, 5)

labirinto_solver = LabirintoRato(labirinto)
caminho = labirinto_solver.encontrar_caminho(inicio, fim)

if caminho:
    print("\nCaminho completo percorrido (Histórico):")
    labirinto_solver.imprimir_caminho()
else:
    print("Nenhum caminho encontrado.")