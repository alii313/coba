from vpython import *
import random

# Membuat scene
scene = canvas(width=555, height=555)

# Membuat Tembok atau kotak
L = 5
box_size = vector(0.1, 2*L, 2*L)
wall_right = box(pos=vector(L, 0, 0), size=box_size, color=color.white)
wall_left = box(pos=vector(-L, 0, 0), size=box_size, color=color.white)
wall_top = box(pos=vector(0, L, 0), size=vector(2*L, 0.1, 2*L), color=color.white)
wall_bottom = box(pos=vector(0, -L, 0), size=vector(2*L, 0.1, 2*L), color=color.white)
wall_back = box(pos=vector(0, 0, -L), size=vector(2*L, 2*L, 0.1), color=color.white)

# Fungsi untuk membuat posisi bola random agar tidak keluar dari batas
def generate_random_position(existing_positions, ball_radius):
    while True:
        pos = vector(random.uniform(-L+1, L-1), random.uniform(-L+1, L-1), 0)
        if all(mag(pos - p) > 2*ball_radius for p in existing_positions):
            return pos

# Membuat bola dengan warna dan ukuran berbeda
colors = [color.red, color.green, color.blue, color.yellow, color.orange]
sizes = [0.5, 0.7, 0.6, 0.8, 0.9]
balls = []
ball_radius = 0.6
positions = []

for i in range(5):
    pos = generate_random_position(positions, ball_radius)
    positions.append(pos)
    balls.append(sphere(pos=pos,
                        radius=sizes[i], color=colors[i],
                        velocity=vector(random.uniform(-1, 1), random.uniform(-1, 1), 0),
                        stopped=False))

# Membuat bola ungu
purple_ball = sphere(pos=vector(0, 0, 0), radius=ball_radius*1.2, color=color.purple, velocity=vector(0, 0, 0))

# Membuat text untuk menghitung jumblah tabrakan
collision_count = 0
collision_text = label(pos=vector(0, L+1, 0), text='Score: 0', color=color.yellow, height=20, box=False, opacity=0)
win_text = label(pos=vector(0, 0, 0), text='Congratulation!', color=color.yellow, height=80, box=False)
win_text.visible = False

# Membuat definisi untuk mode mantul dan berhenti
bounce_mode = True
game_started = False

# Membuat definisi untuk tombol
def toggle_mode():
    global bounce_mode
    bounce_mode = not bounce_mode
    mode_button.text = 'Mode: Bounce' if bounce_mode else 'Mode: Stop'

# Membuat tombol
mode_button = button(text='Mode: Bounce', bind=toggle_mode, pos=scene.title_anchor)

def start_game():
    global game_started, collision_count
    game_started = True
    collision_count = 0
    collision_text.text = 'Score: 0'
    win_text.visible = False
    start_button.disabled = True

def restart_game():
    start_game()
    for ball in balls:
        ball.pos = generate_random_position([b.pos for b in balls], ball_radius)
        ball.velocity = vector(random.uniform(-1, 1), random.uniform(-1, 1), 0)
        ball.stopped = False
    purple_ball.pos = vector(0, 0, 0)
    purple_ball.velocity = vector(0, 0, 0)

start_button = button(text='Start Game', bind=start_game, pos=scene.title_anchor)
restart_button = button(text='Restart Game', bind=restart_game, pos=scene.title_anchor, disabled=True)

# Mendefinisikan keyboard untuk mengngontrol bola ungu
def move_purple_ball(evt):
    s = evt.key
    if s in ['left', 'a']:
        purple_ball.velocity.x = -1
    elif s in ['right', 'd']:
        purple_ball.velocity.x = 1
    elif s in ['up', 'w']:
        purple_ball.velocity.y = 1
    elif s in ['down', 's']:
        purple_ball.velocity.y = -1

scene.bind('keydown', move_purple_ball)

# Memperbarui fungsi
def update_positions():
    global collision_count

    # Memperbarui posisi bola
    for ball in balls:
        ball.pos += ball.velocity * dt

        # Cek tabrakan ke tembok
        if ball.pos.x > L - ball.radius or ball.pos.x < -L + ball.radius:
            ball.velocity.x *= -1
        if ball.pos.y > L - ball.radius or ball.pos.y < -L + ball.radius:
            ball.velocity.y *= -1

        # Cek tabrakan untuk bola lain
        for other in balls:
            if ball != other and mag(ball.pos - other.pos) < 2 * ball.radius:
                ball.velocity, other.velocity = other.velocity, ball.velocity

        # Cek tabrakan untuk bola ungu
        if mag(ball.pos - purple_ball.pos) < 2 * ball.radius:
            if bounce_mode:
                ball.velocity, purple_ball.velocity = purple_ball.velocity, ball.velocity
                collision_count += 1
                collision_text.text = f'Score: {collision_count}'
            else:
                if not ball.stopped:
                    ball.velocity = vector(0, 0, 0)
                    collision_count += 1
                    collision_text.text = f'Score: {collision_count}'
                    ball.stopped = True
        else:
            ball.stopped = False

    # Memperbarui posisi bola ungu
    purple_ball.pos += purple_ball.velocity * dt

    # Cek tabrakan ke tembok buat bola ungu
    if purple_ball.pos.x > L - purple_ball.radius or purple_ball.pos.x < -L + purple_ball.radius:
        purple_ball.velocity.x *= -1
    if purple_ball.pos.y > L - purple_ball.radius or purple_ball.pos.y < -L + purple_ball.radius:
        purple_ball.velocity.y *= -1

    # Cek untuk jumblah tabrakan
    if collision_count >= 10:
        win_text.visible = True
        restart_button.disabled = False

# Waktu
dt = 0.02

# Perulangan
while True:
    rate(100)
    if game_started:
        update_positions()
