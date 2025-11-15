# 🕹️ Catálogo de Jogos Digitais
📌 Descrição do Projeto

Este projeto consiste no desenvolvimento de um sistema de catálogo pessoal de jogos digitais, permitindo gerenciar jogos, acompanhar progresso, organizar por categorias e gerar relatórios de desempenho.
O sistema poderá ser executado via CLI (linha de comando) ou como uma API mínima (FastAPI/Flask — opcional). A aplicação aplica princípios de Programação Orientada a Objetos, incluindo herança, encapsulamento, métodos especiais e regras de negócio configuráveis.
A persistência será realizada em JSON ou SQLite, de forma desacoplada do domínio.

🎯 Objetivo

Criar um sistema completo e modular que permita:
- Cadastrar e gerenciar jogos do usuário.
- Controlar horas jogadas, status e avaliação.
- Organizar jogos por plataforma, gênero e coleções.
- Gerar relatórios como total de horas, média de notas, percentual por status e top 5 mais jogados.
- Aplicar boas práticas de POO e testes automatizados.

🧩 Estrutura de classes
Classe: Jogo 
Atributos principais:
-título
-gênero
-plataforma
-status (NÃO INICIADO, JOGANDO, FINALIZADO)
-horas_jogadas
-avaliacao (0–10)
-data_inicio
-data_termino
Métodos principais:
-atualizar_progresso()
-finalizar() (validação mínima de 1h)
-reiniciar()
