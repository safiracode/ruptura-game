

        if self.jogador:
            # ... (colisões com itens, exceto chave)
            
            partes_colididas = pygame.sprite.spritecollide(self.jogador, self.grupo_chave_partes, True)
            for parte in partes_colididas:
                self.partes_coletadas[parte.parte_index] = True
                self.proxima_parte_a_spawnar += 1
                
                pos_jogador_grid = (self.jogador.rect.x // constants.TAMANHO_BLOCO, self.jogador.rect.y // constants.TAMANHO_BLOCO)
                if self.proxima_parte_a_spawnar == 1: self.spawnar_inimigo(segurancas.Drummond, self.grupo_segurancas, pos_jogador_grid)
                elif self.proxima_parte_a_spawnar == 2: self.spawnar_inimigo(segurancas.Milchick, self.grupo_segurancas, pos_jogador_grid)
                elif self.proxima_parte_a_spawnar == 3: self.spawnar_inimigo(segurancas.Mauer, self.grupo_segurancas, pos_jogador_grid)

                if self.proxima_parte_a_spawnar < constants.NUMERO_PARTES_CHAVE:
                    self.agendar_proxima_chave()
                elif all(self.partes_coletadas): # Se foi a última parte
                    x_porta, y_porta = constants.X_PORTA, constants.Y_PORTA
                    
                    # Procura pela parede de colisão no local da porta e a remove
                    for parede_sprite in self.grupo_paredes:
                        if parede_sprite.rect.x == x_porta * constants.TAMANHO_BLOCO and parede_sprite.rect.y == y_porta * constants.TAMANHO_BLOCO:
                            parede_sprite.kill() # DESTRÓI A BARREIRA INVISÍVEL
                            break
                    
                    # Adiciona a sprite VISUAL da porta aberta
                    nova_porta = porta.Porta(x_porta, y_porta)
                    self.todas_sprites.add(nova_porta)
                    self.grupo_porta.add(nova_porta)
            
            # ... (colisão com café)



            # ... (colisão com inimigos)
