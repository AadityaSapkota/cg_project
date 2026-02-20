import pygame, math, random, sys
pygame.init()
W, H = 900, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("🚀 Rocket to Mars")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("consolas", 32, bold=True)
font_sm  = pygame.font.SysFont("consolas", 16)

# ── Stars ──────────────────────────────────────────────────────────────────
stars = [(random.randint(0,W), random.randint(0,H), random.uniform(0.5,2)) for _ in range(250)]

# ── Particles ──────────────────────────────────────────────────────────────
particles = []

def exhaust(x, y):
    for _ in range(5):
        a = math.pi/2 + random.uniform(-0.4, 0.4)
        spd = random.uniform(2, 5)
        particles.append([x, y, math.cos(a)*spd, math.sin(a)*spd,
                           random.randint(20,40), random.choice(
                               [(255,255,180),(255,140,0),(200,50,0)])])

def dust(x, y):
    for _ in range(18):
        a = random.uniform(math.pi, 2*math.pi)
        spd = random.uniform(1, 3)
        particles.append([x+random.randint(-10,10), y,
                           math.cos(a)*spd, math.sin(a)*spd-random.uniform(0,1),
                           random.randint(25,55), (140,70,35)])

def tick_particles():
    dead = []
    for i,p in enumerate(particles):
        p[0]+=p[2]; p[1]+=p[3]; p[3]+=0.04; p[4]-=1
        if p[4]<=0: dead.append(i); continue
        a = p[4]/55
        c = tuple(min(255,int(v*a)) for v in p[5])
        pygame.draw.circle(screen, c, (int(p[0]),int(p[1])), max(1,int(3*a)))
    for i in reversed(dead): particles.pop(i)

# ── Drawers ────────────────────────────────────────────────────────────────
def draw_stars(t):
    for sx,sy,sz in stars:
        b = int(160 + 90*math.sin(t*0.03+sx))
        pygame.draw.circle(screen,(b,b,b),(sx,sy),int(sz*0.7))

def draw_earth(cx,cy,r):
    pygame.draw.circle(screen,(30,100,200),(cx,cy),r)
    for bx,by,br,c in [(cx-r//3,cy-r//4,r//3,(34,139,34)),
                        (cx+r//5,cy-r//3,r//4,(34,139,34)),
                        (cx+r//3,cy+r//6,r//6,(34,139,34))]:
        pygame.draw.ellipse(screen,c,(bx-br,by-br//2,br*2,br))
    for i in range(6): pygame.draw.circle(screen,(100,160,255),(cx,cy),r+i,1)

def draw_mars(cx,cy,r):
    pygame.draw.circle(screen,(180,60,20),(cx,cy),r)
    pygame.draw.ellipse(screen,(210,120,50),(cx-r//4,cy-r//3,r//2,r//4))
    pygame.draw.ellipse(screen,(220,220,240),(cx-r//4,cy-r-r//8,r//2,r//4))
    for i in range(4): pygame.draw.circle(screen,(180,80,40),(cx,cy),r+i,1)

def draw_rocket(rx,ry,flame=True,t=0,scale=1.0):
    s=scale
    body=[( 0,-28*s),(7*s,-14*s),(7*s,18*s),(-7*s,18*s),(-7*s,-14*s)]
    fins_l=[(-7*s,12*s),(-16*s,22*s),(-7*s,22*s)]
    fins_r=[( 7*s,12*s),( 16*s,22*s),( 7*s,22*s)]
    def T(pts): return [(rx+px,ry+py) for px,py in pts]
    if flame:
        fl=t*0.5; fk=math.sin(fl)*5*s
        fp=T([(0,18*s),(5*s,28*s),(2*s,(42+fk)*s),(0,(50+fk+3)*s),(-2*s,(42+fk)*s),(-5*s,28*s)])
        pygame.draw.polygon(screen,(200,50,0),fp)
        pygame.draw.polygon(screen,(255,140,0),T([(0,18*s),(3*s,28*s),(0,(38+fk)*s),(-3*s,28*s)]))
        pygame.draw.polygon(screen,(255,255,180),T([(0,18*s),(1*s,28*s),(0,35*s),(-1*s,28*s)]))
    pygame.draw.polygon(screen,(150,160,175),T(fins_l))
    pygame.draw.polygon(screen,(150,160,175),T(fins_r))
    pygame.draw.polygon(screen,(200,210,220),T(body))
    pygame.draw.polygon(screen,(230,235,240),T([(0,-28*s),(7*s,-14*s),(-7*s,-14*s)]))
    wc=T([(0,-4*s)])[0]
    wr=int(5*s)
    pygame.draw.circle(screen,(100,180,255),(int(wc[0]),int(wc[1])),wr)
    pygame.draw.circle(screen,(80,160,220),(int(wc[0]),int(wc[1])),wr,2)

def draw_mars_ground(gy):
    pts=[(0,gy)]
    x=0
    while x<W:
        pts.append((x,gy+random.randint(-3,3))); x+=random.randint(15,50)
    pts+=[(W,gy),(W,H),(0,H)]
    pygame.draw.polygon(screen,(140,60,30),pts)
    for cx,cy,cr in [(180,gy-4,22),(500,gy-3,14),(750,gy-5,18)]:
        pygame.draw.ellipse(screen,(100,40,20),(cx-cr,cy-cr//3,cr*2,cr*2//3),3)

def draw_astronaut(ax,ay,flag=False,t=0,facing=1):
    bob=math.sin(t*0.06)*2
    hy=int(ay-82+bob)
    # Legs
    pygame.draw.line(screen,(130,140,160),(ax,int(ay-30)),(ax-5*facing,ay),5)
    pygame.draw.line(screen,(130,140,160),(ax,int(ay-30)),(ax+5*facing,ay),5)
    # Body
    pygame.draw.rect(screen,(220,225,235),(ax-11,int(ay-62),22,32),border_radius=4)
    # Backpack
    pygame.draw.rect(screen,(100,110,130),(ax-11-6*facing,int(ay-58),7,14),border_radius=2)
    # Chest panel
    pygame.draw.rect(screen,(80,160,220),(ax-5,int(ay-56),10,7),border_radius=2)
    # Arms
    arm_r_y = int(ay-56+16)
    lax_end = ax-11-int(14*0.6)
    lay_end = arm_r_y+int(14*0.7)
    pygame.draw.line(screen,(130,140,160),(ax-11,arm_r_y),(lax_end,lay_end),4)
    flag_lift = -20 if flag else 0
    rax_end = ax+11+int(14*0.6)
    ray_end = arm_r_y+int(14*0.7)+flag_lift
    pygame.draw.line(screen,(130,140,160),(ax+11,arm_r_y),(rax_end,ray_end),4)
    # Flag
    if flag:
        pygame.draw.line(screen,(240,240,240),(rax_end,ray_end),(rax_end,ray_end-36),2)
        pygame.draw.rect(screen,(200,30,30),(rax_end,ray_end-36,28,9))
        pygame.draw.rect(screen,(240,240,240),(rax_end,ray_end-27,28,8))
        pygame.draw.rect(screen,(20,60,180),(rax_end,ray_end-19,28,8))
    # Helmet
    pygame.draw.circle(screen,(220,225,235),(ax,hy),13)
    pygame.draw.ellipse(screen,(100,180,255),(ax-9,hy-5,18,12))
    pygame.draw.ellipse(screen,(150,210,255),(ax-6,hy-3,8,6))
    pygame.draw.circle(screen,(180,185,200),(ax,hy),13,2)

def label(text,color,cx,cy):
    s=font_sm.render(text,True,(0,0,0))
    screen.blit(s,s.get_rect(center=(cx+1,cy+1)))
    s=font_sm.render(text,True,color)
    screen.blit(s,s.get_rect(center=(cx,cy)))

def big_label(text,color,cx,cy):
    s=font_big.render(text,True,(0,0,0))
    screen.blit(s,s.get_rect(center=(cx+2,cy+2)))
    s=font_big.render(text,True,color)
    screen.blit(s,s.get_rect(center=(cx,cy)))

def hud(stage):
    bar=pygame.Surface((W,40),pygame.SRCALPHA)
    bar.fill((0,0,0,130))
    screen.blit(bar,(0,0))
    label("🚀  EARTH → MARS  MISSION",(0,220,255),W//2,13)
    label(stage,(255,200,80),W//2,30)

# ── Scenes ─────────────────────────────────────────────────────────────────
# (name, duration_frames)
SCENES = [
    ("LAUNCH",   150),
    ("SPACE",    200),
    ("LANDING",  160),
    ("MARS",     280),
]

def run():
    global particles
    scene_idx = 0
    t = 0
    trail = []
    dust_done = False
    random.seed(42)

    while True:
        clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                if ev.key == pygame.K_SPACE:
                    scene_idx = (scene_idx + 1) % len(SCENES)
                    t = 0; trail.clear(); particles.clear(); dust_done = False

        name, dur = SCENES[scene_idx]
        frac = min(t / dur, 1.0)

        # advance & auto-next
        t += 1
        if t >= dur:
            scene_idx = (scene_idx + 1) % len(SCENES)
            t = 0; trail.clear(); particles.clear(); dust_done = False

        # ── LAUNCH ──────────────────────────────────────────────────────────
        if name == "LAUNCH":
            screen.fill((5,5,20))
            draw_stars(t)

            # Earth rising from bottom
            draw_earth(W//2, H+200, 300)

            ry = int(H*0.75 - frac*H*0.55)
            rx = W//2
            if t > 15: exhaust(rx, ry+40)
            tick_particles()
            draw_rocket(rx, ry, flame=(t>10), t=t, scale=1.3)

            if t < 40:
                cd = max(0, 3 - t//13)
                big_label(f"T-{cd}" if cd else "IGNITION!",(255,80,80),W//2,H//2)
            elif t < 90:
                big_label("LIFTOFF! 🚀",(255,200,50),W//2,H//2-30)

            hud("STAGE 1 — LIFTOFF FROM EARTH")

        # ── SPACE ───────────────────────────────────────────────────────────
        elif name == "SPACE":
            screen.fill((5,5,20))
            draw_stars(t)

            # Sun
            for i in range(10):
                a=math.radians(i*36+t*0.4)
                x1=70+math.cos(a)*46; y1=70+math.sin(a)*46
                x2=70+math.cos(a)*(56+5*math.sin(t*0.05+i)); y2=70+math.sin(a)*(56+5*math.sin(t*0.05+i))
                pygame.draw.line(screen,(255,200,50),(int(x1),int(y1)),(int(x2),int(y2)),2)
            pygame.draw.circle(screen,(255,200,40),(70,70),45)
            pygame.draw.circle(screen,(255,240,120),(55,55),15)

            draw_earth(60, H-60, max(8,int(60-frac*50)))
            draw_mars(W-70, 80, max(8,int(15+frac*45)))

            rx = int(130+frac*(W-260))
            ry = H//2 + int(math.sin(frac*math.pi*2)*55)
            trail.append((rx,ry))
            if len(trail)>70: trail.pop(0)
            for i,(tx,ty) in enumerate(trail):
                a=int(90*(i/len(trail)))
                pygame.draw.circle(screen,(a,a+40,a+90),(tx,ty),max(1,i*2//len(trail)+1))

            exhaust(rx,ry+35)
            tick_particles()
            draw_rocket(rx,ry,flame=True,t=t,scale=0.9)

            dist = int(225_000_000*(1-frac))
            label(f"DISTANCE TO MARS: {dist:,} km",(100,180,255),W//2,H-20)
            hud("STAGE 2 — INTERPLANETARY CRUISE")

        # ── LANDING ─────────────────────────────────────────────────────────
        elif name == "LANDING":
            screen.fill((28,8,4))
            draw_stars(t)

            gy = int(H*0.70)
            draw_mars_ground(gy)

            # Thin reddish atmosphere
            atm=pygame.Surface((W,H),pygame.SRCALPHA)
            pygame.draw.rect(atm,(180,60,20,14),(0,0,W,H))
            screen.blit(atm,(0,0))

            ry = int(60 + frac*(gy-115))
            rx = W//2

            if not dust_done and frac > 0.90:
                dust(rx, gy-8); dust_done = True

            exhaust(rx, ry+40)
            tick_particles()
            draw_rocket(rx, ry, flame=(frac<0.94), t=t, scale=1.2)

            # Landing legs
            if frac > 0.88:
                legy=gy-8
                pygame.draw.line(screen,(180,190,200),(rx-9,int(ry+32)),(rx-20,legy),4)
                pygame.draw.line(screen,(180,190,200),(rx+9,int(ry+32)),(rx+20,legy),4)

            if frac > 0.95:
                big_label("TOUCHDOWN! ✅",(0,255,120),W//2,H//2-60)

            hud("STAGE 3 — POWERED DESCENT & LANDING")

        # ── MARS ────────────────────────────────────────────────────────────
        elif name == "MARS":
            screen.fill((28,8,4))
            draw_stars(t)

            gy = int(H*0.70)
            draw_mars_ground(gy)

            atm=pygame.Surface((W,H),pygame.SRCALPHA)
            pygame.draw.rect(atm,(180,60,20,12),(0,0,W,H))
            screen.blit(atm,(0,0))

            tick_particles()

            # Landed rocket
            draw_rocket(W//2, gy-80, flame=False, t=t, scale=1.2)
            # Landing legs (always visible)
            legy=gy-8
            pygame.draw.line(screen,(180,190,200),(W//2-9,gy-80+32),(W//2-20,legy),4)
            pygame.draw.line(screen,(180,190,200),(W//2+9,gy-80+32),(W//2+20,legy),4)

            # Astronaut 1 walks left
            a1x = int(W//2 - 50 - frac*70)
            draw_astronaut(a1x, gy, flag=(frac>0.65), t=t, facing=-1)

            # Astronaut 2 appears at 0.3
            if frac > 0.30:
                a2x = int(W//2 + 55 + (frac-0.3)*80)
                draw_astronaut(a2x, gy, flag=False, t=t, facing=1)

            # Footprints
            for fp in range(int(frac*7)):
                fx = W//2-38 - fp*16
                pygame.draw.ellipse(screen,(100,40,25),(fx-5,gy-3,10,5))

            # Celebration fireworks
            if frac > 0.7 and t%10==0:
                for _ in range(8):
                    px=random.randint(80,W-80); py=random.randint(60,H//2)
                    col=(random.randint(150,255),random.randint(150,255),random.randint(100,255))
                    for _ in range(10):
                        a=random.uniform(0,math.pi*2)
                        ex=px+int(math.cos(a)*random.randint(5,25))
                        ey=py+int(math.sin(a)*random.randint(5,25))
                        pygame.draw.circle(screen,col,(ex,ey),random.randint(1,3))

            if frac < 0.4:
                big_label('"One giant leap for humankind."',(255,220,100),W//2,90)
            elif frac > 0.65:
                big_label("🎉  MISSION ACCOMPLISHED!",(255,140,50),W//2,90)
                label("Press SPACE to restart",(120,140,160),W//2,H-18)

            hud("STAGE 4 — HUMANS ON MARS")

        pygame.display.flip()

run()