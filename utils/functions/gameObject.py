import pygame
import random
from config import BLANCO, WIDTH, HEIGHT, duracion_partido, tiempo_inicio, partido_terminado, ventana, fuente_chica, GROUND_OFFSET 
pygame.init()
PROFUNDIDAD_GOL = 50
class Arco:
    def __init__(self, lado):
        self.image = pygame.image.load('./utils/imgs/ar.png').convert_alpha()

        # Escalar la imagen
        nuevo_ancho = 200
        nuevo_alto = int(self.image.get_height() * (nuevo_ancho / self.image.get_width()))
        self.image = pygame.transform.scale(self.image, (nuevo_ancho, nuevo_alto))

        # Flip según el lado
        if lado == "dr":
            self.image = pygame.transform.flip(self.image, True, False)

        self.arco_ancho = self.image.get_width()
        self.arco_alto = self.image.get_height()

        # Posiciones
        if lado == "iz":
            self.x = 0
            self.y = HEIGHT - self.arco_alto - GROUND_OFFSET
            self.rect = pygame.Rect(self.x, self.y, 20, self.arco_alto)
            self.goal_area_rect = pygame.Rect(
                self.x + 20,  # Empieza justo después del poste que colisiona con la pelota.
                self.y,       # Empieza en la parte superior del arco.
                PROFUNDIDAD_GOL, # Un ancho suficiente para detectar la entrada.
                self.arco_alto  # Toda la altura del arco.
            )

        elif lado == "dr":
            self.x = WIDTH - self.arco_ancho
            self.y = HEIGHT - self.arco_alto - GROUND_OFFSET
            self.rect = pygame.Rect(self.x + self.arco_ancho - 20, self.y, 20, self.arco_alto)
            self.goal_area_rect = pygame.Rect(
                self.x + self.arco_ancho - 20 - PROFUNDIDAD_GOL, # Posición X: A la izquierda del poste.
                self.y,                                         # Empieza en la parte superior.
                PROFUNDIDAD_GOL,                                # Un ancho suficiente para detectar la entrada.
                self.arco_alto                                  # Toda la altura del arco.
            )

        # Rect para dibujar la imagen
        self.draw_rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.draw_rect)


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
        self.text = self.fuente.render(f"{self.duracion_partido}", True, self.color)

    def update(self, tiempo_actual):
        if not self.paused:
            tiempo_transcurrido = (tiempo_actual - self.tiempo_inicio - self.tiempo_pausado) // 1000
            self.tiempo_restante = max(0, self.duracion_partido - tiempo_transcurrido)
            self.text = self.fuente.render(f" {self.tiempo_restante}", True, self.color)

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
        self.text = self.fuente.render(f"{self.duracion_partido}", True, self.color)


class Personaje:

    def __init__(self, tipo):
        self.tipo = tipo
        self.gravity = 0.5
        self.jump_speed = -10
        self.on_ground = True
        self.current_speed = 5
        self.velocity_y = 0
        self.speed_x = 0

        self.image = pygame.transform.scale(pygame.image.load("./utils/imgs/pg.png"), (100, 100))
        if tipo == "bot":
            x_pos = WIDTH - 250
        else:
            x_pos = 150

        self.rect = self.image.get_rect(x=x_pos, y=HEIGHT - self.image.get_height() - GROUND_OFFSET)
        self.last_x = self.rect.x
        self.hitbox = self.rect.inflate(0, 0)

    def update(self):
        self.last_x = self.rect.x

        # Gravedad
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Piso elevado
        piso = HEIGHT - self.rect.height - GROUND_OFFSET
        if self.rect.y >= piso:
            self.rect.y = piso
            self.velocity_y = 0
            self.on_ground = True

        # Límites horizontales
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width

        # Actualizar hitbox
        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y
        self.speed_x = self.rect.x - self.last_x

    def mover_bot(self, pelota):
        
        self.last_x = self.rect.x
        distancia_pelota = abs(pelota.pelota_rect.centerx - self.rect.centerx)

        if distancia_pelota > 250:
            if self.rect.centerx < WIDTH - 150:
                self.rect.x += self.current_speed
            elif self.rect.centerx > WIDTH - 150:
                self.rect.x -= self.current_speed
        else:
            if pelota.pelota_rect.centerx < self.rect.centerx - random.randint(5, 20):
                self.rect.x -= self.current_speed
            elif pelota.pelota_rect.centerx > self.rect.centerx + random.randint(5, 20):
                self.rect.x += self.current_speed

        if random.random() < 0.01:
            self.rect.x += random.choice([-15, 15])

        if (distancia_pelota < 80 and pelota.pelota_rect.y < self.rect.y
            and self.on_ground and random.random() < 0.5):
            self.velocity_y = self.jump_speed
            self.on_ground = False

        # Límites
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width

        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y
        self.speed_x = self.rect.x - self.last_x

    def mover(self, teclas):
        delta_x = 0
        self.last_x = self.rect.x

        if teclas[pygame.K_LEFT]:
            delta_x = -self.current_speed
        if teclas[pygame.K_RIGHT]:
            delta_x = self.current_speed

        self.rect.x += delta_x

        if teclas[pygame.K_UP] and self.on_ground:
            self.velocity_y = self.jump_speed
            self.on_ground = False

        self.hitbox.topleft = self.rect.topleft
        self.speed_x = self.rect.x - self.last_x




import pygame

class Pelota:
    def __init__(self):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.VELOCIDAD_IMPACTO_Y = -6.0
        self.VELOCIDAD_BASE_X = 7.0
        self.VELOCIDAD_EMPUJE_X = 3.0

        self.original_image = pygame.image.load("./utils/imgs/ball.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))

        self.pelota_img = self.original_image
        self.rot_angle = 0

        self.pelota_rect = self.pelota_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.pelota_hitbox = self.pelota_rect.inflate(0, 0)

        self.MASA = 1.0
        self.pelota_speed_x = 0.0
        self.pelota_speed_y = 0.0

        self.gravedad = 9.8 * 0.05
        self.pelota_elasticidad = 0.70
        self.friccion_aire = 0.999
        self.friccion_suelo = 0.90
        self.VELOCIDAD_CONTROL_MAX = 5.0


    def reset_pelota(self):
        self.pelota_rect.center = (self.WIDTH // 2, self.HEIGHT // 2 - GROUND_OFFSET // 2)
        self.pelota_speed_x = 0.0
        self.pelota_speed_y = 0.0
        
    def check_colision(self, personaje, tipo):
        if self.pelota_rect.colliderect(personaje.hitbox):
            
            direccion_empuje = 1 if self.pelota_rect.centerx > personaje.hitbox.centerx else -1
            
            if self.pelota_speed_y > 0 and self.pelota_rect.bottom >= personaje.hitbox.top and self.pelota_rect.bottom <= personaje.hitbox.centery:
                
                self.pelota_rect.bottom = personaje.hitbox.top 
                self.pelota_speed_y = 0
                return tipo
                
            else:
                
                if abs(self.pelota_rect.centerx - personaje.hitbox.centerx) < (self.pelota_rect.width / 2) + (personaje.hitbox.width / 2):
                    self.pelota_rect.x += direccion_empuje * 1 
                
                return tipo
                    
            
        return None

    def manejar_impacto(self, personaje, es_patada=False):
        
        contacto_superior = self.pelota_rect.bottom < personaje.rect.centery
        
        direccion = 1 if self.pelota_rect.centerx > personaje.rect.centerx else -1
        
        if es_patada or contacto_superior:
            
            if contacto_superior:
                self.pelota_speed_y = -abs(self.VELOCIDAD_IMPACTO_Y) * 0.8
            else:
                self.pelota_speed_y = self.VELOCIDAD_IMPACTO_Y 
            
            self.pelota_speed_x = direccion * (self.VELOCIDAD_BASE_X + abs(personaje.speed_x) * 0.5)

        else:
            
            # Ajuste Clave: Aumentar la transferencia de velocidad pasiva a 0.5
            self.pelota_speed_x += personaje.speed_x * 0.5 
            
            if abs(self.pelota_speed_x) > self.VELOCIDAD_CONTROL_MAX:
                self.pelota_speed_x *= 0.35 
            else:
                self.pelota_speed_x *= 0.8 
            
            if abs(self.pelota_speed_x) > self.VELOCIDAD_CONTROL_MAX:
                self.pelota_speed_x = self.VELOCIDAD_CONTROL_MAX * (1 if self.pelota_speed_x > 0 else -1)

        
        if self.pelota_rect.bottom > personaje.rect.top and self.pelota_speed_y > 0:
             self.pelota_speed_y *= -0.3 
             
        MAX_SPEED = 20.0
        if abs(self.pelota_speed_x) > MAX_SPEED:
            self.pelota_speed_x = MAX_SPEED * (1 if self.pelota_speed_x > 0 else -1)


    def aplicar_patada(self, pj_centerx, pelota_centerx):
        self.pelota_speed_y = self.VELOCIDAD_IMPACTO_Y
        
        if pelota_centerx < pj_centerx:
            self.pelota_speed_x = -self.VELOCIDAD_BASE_X 
        else:
            self.pelota_speed_x = self.VELOCIDAD_BASE_X

    def update(self):
        self.pelota_speed_y += self.gravedad
        self.pelota_speed_x *= self.friccion_aire

        self.pelota_rect.y += self.pelota_speed_y
        self.pelota_rect.x += self.pelota_speed_x

        self.rot_angle -= self.pelota_speed_x * 1.5
        new_img = pygame.transform.rotate(self.original_image, self.rot_angle)
        old_center = self.pelota_rect.center
        self.pelota_img = new_img
        self.pelota_rect = self.pelota_img.get_rect(center=old_center)

        # Colisión con el suelo elevado
        suelo = self.HEIGHT - GROUND_OFFSET
        if self.pelota_rect.bottom >= suelo:
            self.pelota_rect.bottom = suelo
            self.pelota_speed_y *= -self.pelota_elasticidad
            self.pelota_speed_x *= self.friccion_suelo

            if abs(self.pelota_speed_y) < 0.5:
                self.pelota_speed_y = 0
            if abs(self.pelota_speed_x) < 0.2:
                self.pelota_speed_x = 0

        # Paredes
        if self.pelota_rect.left <= 0 or self.pelota_rect.right >= self.WIDTH:
            self.pelota_speed_x *= -self.pelota_elasticidad
            if self.pelota_rect.left < 0:
                self.pelota_rect.left = 0
            if self.pelota_rect.right > self.WIDTH:
                self.pelota_rect.right = self.WIDTH


    def draw(self, surface):
        surface.blit(self.pelota_img, self.pelota_rect)

    def gol(self, arcoIz, arcoDer, goles_jugador, goles_bot):
        if arcoIz.rect.colliderect(self.pelota_rect):
              goles_bot += 1
              self.pelota_rect.x = self.WIDTH // 2
              self.pelota_rect.y = self.HEIGHT - 50
              self.pelota_speed_x = 0
              self.pelota_speed_y = 0
              return goles_jugador, goles_bot

        if arcoDer.rect.colliderect(self.pelota_rect):
              goles_jugador += 1
              self.pelota_rect.x = self.WIDTH // 2
              self.pelota_rect.y = self.HEIGHT - 50
              self.pelota_speed_x = 0
              self.pelota_speed_y = 0
              return goles_jugador, goles_bot
              
        return goles_jugador, goles_bot






















