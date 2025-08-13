# Projeto final de Introdução à Programação: Ruptura game ▶️

Este projeto consiste em um jogo 2D desenvolvido como parte da disciplina de Introdução à Programação. Utilizando a biblioteca _Pygame_, criamos uma experiência interativa que coloca em prática os conhecimentos adquiridos ao longo do semestre, desde estruturas de controle e manipulação de eventos até o uso de recursos gráficos e sonoros. Nosso objetivo foi transformar conceitos teóricos em algo concreto e funcional, unindo programação e criatividade.

A temática principal é inspirada na série _Ruptura (Severance)_, cuja ambientação enigmática e estética minimalista influenciaram fortemente a construção dos cenários, da paleta de cores e da atmosfera geral do jogo. Buscamos reproduzir a sensação de mistério e tensão característica da obra, adaptando-a para um formato interativo, no qual o jogador mergulha em um mundo dividido entre o trabalho e a vida pessoal, enfrentando desafios que testam tanto a lógica quanto a atenção aos detalhes. Ao longo do desenvolvimento, exploramos diferentes ideias de programação, narrativa e design, sempre buscando manter a identidade visual e o clima narrativo que definem o universo de _Ruptura_.


## Membros da Equipe 5 👥 
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/analauraboliveira">
        <img src="https://avatars.githubusercontent.com/u/207280291?s=400&u=35e9f2c0ae2f2abd4ac5df89616d0df430ba9a39&v=4" width="115"><br>
        <sub>Ana Laura Barboza (<code>albos</code>)</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Izadora1">
        <img src="https://avatars.githubusercontent.com/u/129686992?v=4" width="115"><br>
        <sub>Izadora Andrade (<code>itga</code>)</sub> 
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/laissaraiva">
        <img src="https://avatars.githubusercontent.com/u/224659710?v=4" width="115"><br>
        <sub>Laís Saraiva  (<code>lspc</code>)</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/lauravfonseca">
        <img src="https://avatars.githubusercontent.com/u/211055257?v=4" width="115"><br>
        <sub>Laura Fonseca (<code>lvnf</code>)</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/lestrb">
        <img src="https://avatars.githubusercontent.com/u/193823503?v=4" width="115"><br>
        <sub>Letícia Staudinger (<code>lsr</code>)</sub> 
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/safiracode">
        <img src="https://avatars.githubusercontent.com/u/206463303?v=4" width="115"><br>
        <sub>Safira Moraes (<code>smg</code>)</sub> 
      </a>
    </td>
  </tr>
</table>

## Divisão de tarefas do projeto 👨‍💻

| Time                                                  | Tarefas                                                                                |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [Ana Laura Barboza]                                   | Desenvolvimento do código e solução de problemas, design dos personagens, sonoplastia do jogo, organização do código, documentação nas planilhas e organização do GitHub |
| [Izadora Andrade]                                     | Desenvolvimento do código e solução de problemas,    |
| [Laís Saraiva]                                        | Desenvolvimento do código e solução de problemas,   |
| [Laura Fonseca]                                       | Desenvolvimento do código e solução de problemas,    |
| [Letícia Staudinger]                                  | Desenvolvimento do código e solução de problemas, |
| [Safira Moraes]                                       | Desenvolvimento do código e solução de problemas, |

## Arquitetura do projeto e organizacão do código 🏛
Organizamos o _Ruptura Game_ através de arquivos e pastas de acordo com suas funções para facilitar a manutenção e permitir que as integrantes do grupo trabalhasse em partes diferentes do código sem conflitos.  

A estrutura do repositório está organizada assim:  
- `main.py` : ponto de entrada do jogo, onde o Pygame é inicializado e o loop principal é executado.  
- `constants.py` : centraliza variáveis e configurações fixas, como cores, dimensões da tela, FPS e outros parâmetros globais.  
- `mapa.py` : gerencia a estrutura do mapa, posicionamento de elementos e obstáculos.  
- `tela_start.py` : tela inicial do jogo, com título e opções de navegação.  
- `tela_tutorial.py` : apresenta as instruções básicas para orientar o jogador.  
- `game_over.py` : lógica e exibição da tela de derrota padrão.  
- `game_over_cobel.py` : tela de derrota específica para quando Mark é vencido pela personagem Cobel.  
- `venceu.py` : lógica e exibição da tela de vitória.  
- `classes/` : contém as classes principais, como personagens, inimigos e objetos interativos.  
- `audios/` : reúne todos os arquivos sonoros, incluindo efeitos e trilhas.  
- `imagens/` : ideias de imagens gerais, como ícones e fundos.
- `imagens_jogo/` : recursos visuais definitivos usados no jogo.  
- `ideias de imagens/` : material de referência para a criação da estética do jogo.  
- `__pycache__/` : arquivos compilados automaticamente pelo Python.  


## Capturas de tela 🖼️

Abaixo estão algumas imagens do jogo:

<p align="center">
  <img src="imagens_jogo/tela_inicial.png" alt="Tela inicial" width="350"/>
  <img src="imagens_jogo/tela_tutorial.png" alt="Tela Tutorial" width="350"/>
  <img src="imagens_jogo/tela_tutorial_2.png" alt="Tela Tutorial 1" width="350"/>
  <img src="imagens_jogo/tela_tutorial_3.png" alt="Tela Tutorial 2" width="350"/>
  <img src="imagens_jogo/tela_tutorial_4.png" alt="Tela Tutorial 3" width="350"/>
  <img src="imagens_jogo/tela_jogo.png" alt="Tela do Jogo" width="350"/>
  <img src="imagens_jogo/tela_game_over.png" alt="Tela Game Over" width="350"/>
  <img src="imagens_jogo/tela_venceu.png" alt="Tela Venceu" width="350"/>
</p>

## Ferramentas, frameworks e bibliotecas utilizados 🛠️ 

## Conceitos da disciplina aplicados 💡

## Desafios, erros e lições aprendidas 💥


