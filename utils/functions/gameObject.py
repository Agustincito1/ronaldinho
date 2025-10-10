import pygame
import random
from config import BLANCO, WIDTH, HEIGHT, duracion_partido, tiempo_inicio, partido_terminado, ventana, fuente_chica
pygame.init()



class Personaje:

    def __init__(self, tipo):

        if(tipo =="bot"):
            self.bot_img = pygame.transform.scale(pygame.image.load("./utils/imgs/pg.png"), (100, 100))
            self.bot_rect = self.bot_img.get_rect()
            self.bot_rect.x = WIDTH - 200
            self.bot_rect.y = HEIGHT - 50
            self.bot_hitbox = self.bot_rect.inflate(0, 0)
            self.bot_speed = 5
            self.gravity = 0.5
            self.jump_speed = -10
            self.bot_velocity_y = 0
            self.on_ground = True

        elif(tipo == "usuario"):
            
            self.player_img = pygame.image.load("./utils/imgs/pg.png")
            self.player_img = pygame.transform.scale(self.player_img, (100, 100))
            self.player_rect = self.player_img.get_rect()
            self.player_rect.x = 100
            self.player_rect.y = HEIGHT - 50

            self.player_speed = 5
            self.gravity = 0.5  
            self.jump_speed = -10  
            self.player_velocity_y = 0
            self.on_ground = True 
            self.player_hitbox = self.player_rect.inflate(0, 0)

    def update(self, tipo):
        if tipo == "bot":
            # gravedad
            self.bot_velocity_y += self.gravity
            self.bot_rect.y += self.bot_velocity_y

            piso_bot = HEIGHT - self.bot_rect.height
            if self.bot_rect.y >= piso_bot:
                self.bot_rect.y = piso_bot
                self.bot_velocity_y = 0
                self.on_ground = True

            # límites pantalla
            if self.bot_rect.x <= 0:
                self.bot_rect.x = 0
            if self.bot_rect.x >= WIDTH - self.bot_rect.width:
                self.bot_rect.x = WIDTH - self.bot_rect.width

        else:

            self.player_velocity_y += self.gravity
            self.player_rect.y += self.player_velocity_y

            piso = HEIGHT - self.player_rect.height
            if self.player_rect.y >= piso:
                self.player_rect.y = piso
                self.player_velocity_y = 0
                self.on_ground = True

            if self.player_rect.x <= 0:
                self.player_rect.x = 0

            if self.player_rect.x >= WIDTH - self.player_rect.width:
                self.player_rect.x = WIDTH - self.player_rect.width

    def mover_bot(self, pelota):
        import random

    def mover_bot(self, pelota):
        
        distancia_pelota = abs(pelota.pelota_rect.centerx - self.bot_rect.centerx)

        if distancia_pelota > 250:
            if self.bot_rect.centerx < WIDTH - 150: 
                self.bot_rect.x += self.bot_speed
            elif self.bot_rect.centerx > WIDTH - 150:
                self.bot_rect.x -= self.bot_speed

        else:
            if pelota.pelota_rect.centerx < self.bot_rect.centerx - random.randint(5, 20):
                self.bot_rect.x -= self.bot_speed
            elif pelota.pelota_rect.centerx > self.bot_rect.centerx + random.randint(5, 20):
                self.bot_rect.x += self.bot_speed

        if random.random() < 0.01:  
            self.bot_rect.x += random.choice([-15, 15])

        if (distancia_pelota < 80 and pelota.pelota_rect.y < self.bot_rect.y
            and self.on_ground and random.random() < 0.5):  # 50% de decidir saltar
            self.bot_velocity_y = self.jump_speed
            self.on_ground = False

        if self.bot_rect.x <= 0:
            self.bot_rect.x = 0
        if self.bot_rect.x >= WIDTH - self.bot_rect.width:
            self.bot_rect.x = WIDTH - self.bot_rect.width

        self.bot_hitbox.x = self.bot_rect.x
        self.bot_hitbox.y = self.bot_rect.y


    def mover(self, teclas):

        
        
        if teclas[pygame.K_LEFT]:
            self.player_rect.x -= self.player_speed
        if teclas[pygame.K_RIGHT]:
            self.player_rect.x += self.player_speed
        if teclas[pygame.K_UP] and self.on_ground:  
            self.player_velocity_y = self.jump_speed
            self.on_ground = False

        
        self.player_hitbox.x = self.player_rect.x
        self.player_hitbox.y = self.player_rect.y
        

        return

        


class Arco:

    def __init__(self, lado):
        self.image  = pygame.image.load('./utils/imgs/arcos.png').convert_alpha()

        if lado == "iz":

            self.arco_ancho = self.image.get_width()
            self.arco_alto = self.image.get_height()
            self.x = 0
            self.y = HEIGHT - self.arco_alto
        elif lado == "dr":
            # ➡️ ¡Aquí se le da la vuelta a la imagen solo para este objeto!
            image = pygame.transform.flip(self.image, True, False)
            # Posición derecha
            self.arco_ancho = self.image.get_width()
            self.arco_alto = self.image.get_height()
            self.x = WIDTH - self.arco_ancho
            self.y = HEIGHT - self.arco_alto
        
        self.arco_izq_x = 0
        self.arco_izq_y = HEIGHT - self.arco_alto
        self.arco_der_x = WIDTH - self.arco_ancho
        self.arco_der_y = HEIGHT - self.arco_alto

        if lado == "iz":
            self.x = self.arco_izq_x
            self.y = self.arco_izq_y
            self.rect = pygame.Rect(self.x, self.y, 20, self.arco_alto) 
        elif lado == "dr":
            self.x = self.arco_der_x
            self.y = self.arco_der_y
            self.rect = pygame.Rect(self.x + self.arco_ancho - 20, self.y, 20, self.arco_alto)
            
        self.draw_rect = self.image.get_rect(topleft=(self.x, self.y))
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.draw_rect)



class Pelota:
    def __init__(self):

        self.pelota_img = pygame.image.load("./utils/imgs/ball.png").convert_alpha()
        self.pelota_img = pygame.transform.scale(self.pelota_img, (50, 50)) 
        self.pelota_rect = self.pelota_img.get_rect()
        self.pelota_rect.x = WIDTH * 0.50 
        self.pelota_rect.y = HEIGHT * 0.50  
        self.pelota_speed_x = 2
        self.pelota_speed_y = 0.5
        self.pelota_rebote = -8
        self.pelota_elasticidad = 0.7
        self.energia = 0
        self.gravedad = 0.5
        self.pelota_hitbox = self.pelota_rect.inflate(0, 0)

        
    def reset_pelota(self):
        self.pelota_rect.x = WIDTH * 0.50
        self.pelota_rect.y = HEIGHT * 0.50
        self.pelota_speed_x = 2
        self.pelota_speed_y = 0

    def colision(self, pj, tipo):
        
        if tipo == "bot":
            if self.pelota_rect.colliderect(pj.bot_hitbox):

                self.pelota_speed_y = -8  
                if self.pelota_rect.centerx < pj.bot_hitbox.centerx:
                    self.pelota_speed_x = -5  # se va a la izquierda
                else:
                    self.pelota_speed_x = 5   # se va a la derecha
           
        else:
             
            if self.pelota_rect.colliderect(pj.player_hitbox):
                self.pelota_speed_y = -8  
                if self.pelota_rect.centerx < pj.player_hitbox.centerx:
                    self.pelota_speed_x = -5  # se va a la izquierda
                else:
                    self.pelota_speed_x = 5   # se va a la derecha
    
    def update(self):

        self.pelota_speed_y += self.gravedad
        self.pelota_rect.y += self.pelota_speed_y
        self.pelota_rect.x += self.pelota_speed_x
        if self.pelota_rect.bottom >= HEIGHT:
            self.pelota_rect.bottom = HEIGHT
            self.pelota_speed_y *= -self.pelota_elasticidad
            if abs(self.pelota_speed_y) < 1:
                self.pelota_speed_y = 0

            self.pelota_speed_x *= 0.9  
            if abs(self.pelota_speed_x) < 0.1:  
                self.pelota_speed_x = 0
        if self.pelota_rect.left <= 0 or self.pelota_rect.right >= WIDTH:
            self.pelota_speed_x *= -1

        
    def gol(self, arcoIz, arcoDer, goles_jugador, goles_bot):
        if arcoIz.rect.colliderect(self.pelota_rect):
            goles_bot += 1
            self.pelota_rect.x = WIDTH // 2
            self.pelota_rect.y = HEIGHT - 100
            self.pelota_speed_x = 0
            self.pelota_speed_y = 0

        if arcoDer.rect.colliderect(self.pelota_rect):
            goles_jugador += 1
            self.pelota_rect.x = WIDTH // 2
            self.pelota_rect.y = HEIGHT - 100
            self.pelota_speed_x = 0
            self.pelota_speed_y = 0

        return goles_jugador, goles_bot


class Contador: 
    def __init__(self, tiempo_actual, duracion_partido, fuente, color):
        self.duracion_partido = duracion_partido
        self.pause_start = 0
        self.tiempo_inicio = tiempo_actual
        self.tiempo_pausado = 0
        self.tiempo_restante = duracion_partido
        self.paused = False
        self.fuente = fuente
        self.color = color
        self.text = self.fuente.render(f"Tiempo: {self.duracion_partido}", True, self.color)

    def update(self, tiempo_actual):
        if not self.paused:
            tiempo_transcurrido = (tiempo_actual - self.tiempo_inicio - self.tiempo_pausado) // 1000
            self.tiempo_restante = max(0, self.duracion_partido - tiempo_transcurrido)
            self.text = self.fuente.render(f"Tiempo: {self.tiempo_restante}", True, self.color)

    def stop(self, tiempo_actual):
        if not self.paused:
            self.paused = True
            self.pause_start = tiempo_actual  # guardamos cuándo se pausó

    def resume(self, tiempo_actual):
        if self.paused:
            self.paused = False
            # sumamos el tiempo que estuvo pausado
            self.tiempo_pausado += (tiempo_actual - self.pause_start)

    def reset(self, tiempo_actual):
        self.tiempo_inicio = tiempo_actual
        self.tiempo_pausado = 0
        self.paused = False
        self.text = self.fuente.render(f"Tiempo: {self.duracion_partido}", True, self.color)



     