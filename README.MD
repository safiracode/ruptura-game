# Projeto final de Introdução à Programação: _Ruptura Game_ ▶️

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
- `classes` : contém as classes principais, como personagens, inimigos e objetos coletáveis.  
- `audios` : reúne todos os arquivos sonoros usados no jogo, incluindo efeitos e trilhas.  
- `imagens` : ideias de imagens gerais, como ícones dos coletáveis e os movimentos dos personagens.
- `imagens_jogo` : telas de início, derrota, vitória, tutorial e a tela geral do jogo.
- `ideias de imagens` : material de referência para a criação da estética do jogo.  
- `__pycache__` : arquivos compilados automaticamente pelo Python.  


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
Para o desenvolvimento do _Ruptura Game_, utilizamos um conjunto de ferramentas e tecnologias, que tornaram possível criar um projeto funcional, visualmente interessante e tecnicamente funcional. Esses recursos foram:

- **Python ** — Linguagem principal do projeto, utilizada para a implementação da lógica, organização das classes e integração de todas as partes do sistema.  
- **Pygame** — Biblioteca que serviu como base para o desenvolvimento gráfico, detecção de eventos, manipulação de sons e controle de animações.  
- **Visual Studio Code** — Editor de código adotado pelo grupo, com suporte a extensões úteis e integração com GitHub.  
- **GitHub** — Usado para o controle de versão, acompanhamento das alterações e colaboração remota de forma organizada.  
- **Canva e Photoshop** — Utilizados para a criação e edição de elementos visuais, preservando a identidade visual.  
- **Discord / WhatsApp** — Aplicativos de comunicação, utilizados para o alinhamento de equipe, com mensagens e reuniões por chamada de vídeo.  
- **YouTube, OpenGameArt e FreeSound** — Bibliotecas de efeitos sonoros e trilhas, enriquecendo o jogo. 

## Conceitos da disciplina aplicados 💡
Durante o desenvolvimento do _Ruptura Game_, colocamos em prática diversos conceitos vistos ao longo da disciplina, aplicando-os diretamente na lógica e na estrutura do jogo.  

Os _comandos condicionais_ (`if`, `elif`, `else`) foram fundamentais para controlar o fluxo de execução, determinando ações diferentes a depender de eventos como colisões, transições de fases ou escolha de opções no menu. Já os _laços de repetição_ (`for` e `while`) foram essenciais para percorrer coleções de dados, atualizar elementos em tela e manter o _game loop_ rodando de forma contínua até que uma condição de término fosse atingida.  

As _listas_ foram amplamente utilizadas para armazenar e gerenciar elementos do jogo, como conjuntos de sprites, obstáculos e sequências de frames de animação. Em alguns casos, usamos _tuplas_ para representar dados que não precisariam ser modificados, ou seja, que se mantêm constantes ao longo da execução do jogo. O uso de _matrizes_ também foi útil para representar mapas e fases do jogo, onde cada posição correspondia a um elemento do cenário. Isso possibilitou um controle mais intuitivo sobre a disposição dos objetos e facilitou a lógica de colisão e movimentação.  

As _funções_ desempenharam um papel importante na organização do código, separando responsabilidades em blocos lógicos, como: inicializar o jogo, processar entradas do usuário, atualizar o estado dos personagens e renderizar os elementos na tela.

Por fim, também aplicamos _Programação Orientada a Objetos (POO)_ para estruturar o jogo de forma modular e reutilizável. Criamos classes para representar entidades como o jogador, inimigos e elementos de cenário, encapsulando seus atributos e comportamentos e permitindo instanciar múltiplos objetos de forma independente.  

## Desafios, erros e lições aprendidas 💥
> **Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?** <
O maior erro cometido ao longo do desenvolvimento do *Ruptura Game* foi a subestimação do tempo necessário para integrar todos os elementos do jogo, especialmente no início do trabalho. Essa falta de planejamento prejudicou o andamento das etapas iniciais, atrasando a implementação de funcionalidades-chave. Lidamos com essa situação estabelecendo um cronograma mais rígido, redistribuindo tarefas e definindo responsabilidades claras para cada integrante, o que melhorou tanto a organização interna quanto o uso do nosso tempo.  

> **Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?** <
O maior desafio foi implementar a inteligência do inimigo de forma que sua movimentação e ações fossem coerentes com a proposta do jogo. Para superar essa dificuldade, realizamos pesquisas aprofundadas, estudamos referências de IA em outros jogos desenvolvidos em Pygame e fizemos vários testes práticos até encontrar um comportamento que equilibrasse desafio e jogabilidade.  

> **Quais as lições aprendidas durante o projeto?**  <
Aprendemos a importância de um bom planejamento desde o início, a necessidade de testar constantemente cada funcionalidade antes de integrá-la ao jogo e a valorizar a colaboração em equipe. Além disso, nos aprofundamos em ferramentas que antes não dominávamos — como Pygame, GitHub e Trello — e fortalecemos nossa capacidade de delegar funções, adaptar soluções e trabalhar de forma coesa para alcançar um resultado final satisfatório.  


