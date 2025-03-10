import pygame, sys, random, math, textwrap
pygame.init()
pygame.font.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
GOLD = (212,175,55)
LIGHT_GRAY = (220,220,220)
DARK_GRAY = (40,40,40)
GRAY = (180,180,180)
LIGHT_BLUE = (200,200,255)
DARK_BROWN = (50,40,30)
SHOP_BUTTON_COLOR = (101,67,33)
TOOLTIP_BG_COLOR = (245,222,179)
TOOLTIP_TEXT_COLOR = WHITE
PATH_COLOR = RED

element_tints = {
    "flame": (255,150,50,80),
    "frost": (173,216,230,80),
    "lightning": (255,255,100,80),
    "arrow": (220,220,220,80),
    "wind": (200,200,255,80),
    "toxin": (150,0,150,80),
    "earth": (139,69,19,80),
    "shadow": (100,100,100,80),
    "holy": (255,255,255,80),
    "shield": (200,200,200,80)
}

try:
    FANTASY_FONT = pygame.font.SysFont("Castellar", 32)
    FANTASY_FONT_SMALL = pygame.font.SysFont("Castellar", 22)
    INFO_FONT = pygame.font.SysFont("Castellar", 24)
except Exception as e:
    FANTASY_FONT = pygame.font.SysFont("arial", 32)
    FANTASY_FONT_SMALL = pygame.font.SysFont("arial", 22)
    INFO_FONT = pygame.font.SysFont("arial", 24)

def draw_big_button(surface, rect, text, font, bg_color, border_color, text_color):
    shadow = rect.copy()
    shadow.x += 4; shadow.y += 4
    pygame.draw.rect(surface, (0,0,0), shadow, border_radius=8)
    pygame.draw.rect(surface, bg_color, rect, border_radius=8)
    pygame.draw.rect(surface, border_color, rect, 4, border_radius=8)
    txt = font.render(text, True, text_color)
    surface.blit(txt, txt.get_rect(center=rect.center))

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line: lines.append(current_line)
    return lines

PASSIVE_POOL = [
    {"id": "rapid_fire", "name": "Rapid Fire", "description": "Fires 10% faster.", "icon_color": (255,100,100), "effect": ("attack_speed", 1.10)},
    {"id": "mighty_strikes", "name": "Mighty Strikes", "description": "Deals 10% more damage.", "icon_color": (100,255,100), "effect": ("damage", 1.10)},
    {"id": "wealth_magnet", "name": "Wealth Magnet", "description": "Earns 10% more gold per demon.", "icon_color": (255,215,0), "effect": ("gold", 1.10)},
    {"id": "extended_range", "name": "Extended Range", "description": "Increases range by 10%.", "icon_color": (100,100,255), "effect": ("range", 1.10)},
    {"id": "arcane_insight", "name": "Arcane Insight", "description": "Upgrade costs reduced by 10%.", "icon_color": (150,0,150), "effect": ("upgrade_cost", 0.90)},
    {"id": "elemental_mastery", "name": "Elemental Mastery", "description": "Boosts elemental effects by 10%.", "icon_color": (0,200,200), "effect": ("elemental", 1.10)},
    {"id": "arcane_surge", "name": "Arcane Surge", "description": "Increases spell power by 10%.", "icon_color": (200,0,200), "effect": ("spell_power", 1.10)},
    {"id": "critical_focus", "name": "Critical Focus", "description": "10% chance to double damage.", "icon_color": (255,105,180), "effect": ("critical", 1.10)},
    {"id": "chain_reaction", "name": "Chain Reaction", "description": "Spell effects chain to an extra enemy.", "icon_color": (255,140,0), "effect": ("chain", 1.10)}
]
PASSIVE_SHORT = {
    "rapid_fire": "+10% Attack Speed",
    "mighty_strikes": "+10% Damage",
    "wealth_magnet": "+10% Gold",
    "extended_range": "+10% Range",
    "arcane_insight": "-10% Upgrade Cost",
    "elemental_mastery": "+10% Spell Effects",
    "arcane_surge": "+10% Spell Power",
    "critical_focus": "+10% Critical",
    "chain_reaction": "+10% Chain"
}

TOWER_POOL = [
    {"name": "Crimson Cannon", "color": (220,20,60), "range": 80, "damage": 30, "attack_rate": 1.0, "tooltip": "Explosive blast.", "design": "flame"},
    {"name": "Azure Aegis", "color": (30,144,255), "range": 90, "damage": 20, "attack_rate": 0.8, "tooltip": "Steady defense.", "design": "shield"},
    {"name": "Emerald Sniper", "color": (50,205,50), "range": 120, "damage": 45, "attack_rate": 0.5, "tooltip": "Precise shots.", "design": "sniper"},
    {"name": "Solar Barrage", "color": (255,215,0), "range": 85, "damage": 35, "attack_rate": 0.7, "tooltip": "Searing flares.", "design": "burst"},
    {"name": "Amethyst Shock", "color": (138,43,226), "range": 75, "damage": 28, "attack_rate": 1.2, "tooltip": "Arcane lightning.", "design": "lightning"},
    {"name": "Inferno Incinerator", "color": (255,69,0), "range": 65, "damage": 55, "attack_rate": 0.6, "tooltip": "Raging flame.", "design": "flame"},
    {"name": "Glacial Sentinel", "color": (0,255,255), "range": 100, "damage": 18, "attack_rate": 1.0, "tooltip": "Icy blasts.", "design": "frost"},
    {"name": "Mystic Oracle", "color": (255,0,255), "range": 90, "damage": 25, "attack_rate": 1.5, "tooltip": "Mystical energy.", "design": "swirl"},
    {"name": "Auric Bastion", "color": (212,175,55), "range": 100, "damage": 35, "attack_rate": 0.9, "tooltip": "Steadfast magic.", "design": "bastion"},
    {"name": "Hybrid Vanguard", "color": (180,180,255), "range": 110, "damage": 40, "attack_rate": 1.0, "tooltip": "Fused arcane and kinetic power.", "design": "hybrid", "hybrid": ["arcane_surge", "rapid_fire"]},
    {"name": "Elemental Conflux", "color": (255,200,200), "range": 95, "damage": 42, "attack_rate": 1.1, "tooltip": "Fusion of fire and frost.", "design": "hybrid", "hybrid": ["rapid_fire", "frost"]}
]

DEMON_INFO = [
    {"type": "Fast Demon", "description": "Quick and nimble.", "icon_color": (255,100,150)},
    {"type": "Tank Demon", "description": "Sturdy and robust.", "icon_color": (50,150,200)},
    {"type": "Stealth Demon", "description": "Sneaky and cute.", "icon_color": (150,150,50)},
    {"type": "Special Demon", "description": "Unique and quirky.", "icon_color": (200,100,255)},
    {"type": "Dark Demon", "description": "Mischievous and mysterious.", "icon_color": (100,50,50)},
    {"type": "Frost Demon", "description": "Cool and frosty.", "icon_color": (150,220,255)},
    {"type": "Storm Demon", "description": "Zany and electric.", "icon_color": (255,255,100)},
    {"type": "Venom Demon", "description": "Sly and vibrant.", "icon_color": (100,0,200)},
    {"type": "Necro Demon", "description": "Spooky and cute.", "icon_color": (120,120,120)},
    {"type": "Celestial Demon", "description": "Magical and exotic.", "icon_color": (255,200,50)}
]

ELEMENTS_INFO = [
    {"element": "Flame", "color": (255,69,0), "description": "Explosive, searing bursts."},
    {"element": "Frost", "color": (173,216,230), "description": "Icy blasts that slow enemies."},
    {"element": "Lightning", "color": (255,255,0), "description": "Chain lightning strikes."},
    {"element": "Arrow", "color": (192,192,192), "description": "Piercing, swift projectiles."},
    {"element": "Wind", "color": (123,104,238), "description": "Gusts that push foes back."},
    {"element": "Toxin", "color": (75,0,130), "description": "Poison clouds that drain vitality."},
    {"element": "Earth", "color": (139,69,19), "description": "Crushing impacts."},
    {"element": "Shadow", "color": (75,0,130), "description": "Weakening, sapping energy."},
    {"element": "Holy", "color": (255,215,0), "description": "Divine smiting power."},
    {"element": "Shield", "color": (200,200,200), "description": "Enemies hit take 25% extra damage."}
]

def get_rating_attack_rate(attack_rate):
    if attack_rate <= 0.6: return 5
    elif attack_rate <= 0.8: return 4
    elif attack_rate <= 1.0: return 3
    elif attack_rate <= 1.2: return 2
    else: return 1

def get_rating_damage(damage):
    if damage < 25: return 1
    elif damage < 35: return 2
    elif damage < 45: return 3
    elif damage < 55: return 4
    else: return 5

def get_rating_range(rng):
    if rng < 70: return 1
    elif rng < 80: return 2
    elif rng < 100: return 3
    elif rng < 120: return 4
    else: return 5

def get_tower_description(tower_spec):
    name = tower_spec["name"]
    if "hybrid" in tower_spec:
        typ = ", ".join(tower_spec["hybrid"]).capitalize()
    else:
        typ = tower_spec.get("design", "Unknown").capitalize()
    damage = str(tower_spec["damage"])
    speed = str(tower_spec["attack_rate"])
    rng = str(tower_spec["range"])
    return f"Name: {name}\nType: {typ}\nDamage: {damage}\nSpeed: {speed}\nRange: {rng}"

def create_background_texture(width, height):
    bg = pygame.Surface((width, height))
    for y in range(height):
        r = int(20 + (80-20)*(y/height))
        g = int(20 + (80-20)*(y/height))
        b = int(40 + (120-40)*(y/height))
        pygame.draw.line(bg, (r,g,b), (0,y), (width,y))
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        rad = random.randint(5,15)
        col = (random.randint(50,100), random.randint(50,100), random.randint(80,120))
        s = pygame.Surface((rad*2, rad*2), pygame.SRCALPHA)
        pygame.draw.circle(s, col+(80,), (rad,rad), rad)
        bg.blit(s, (x-rad, y-rad))
    return bg

def create_castle_sprite():
    castle = pygame.Surface((40,40), pygame.SRCALPHA)
    pygame.draw.rect(castle, (150,150,150), (5,20,30,15))
    pygame.draw.rect(castle, BLACK, (5,20,30,15), 2)
    pygame.draw.polygon(castle, (180,180,180), [(5,20),(20,5),(35,20)])
    pygame.draw.polygon(castle, BLACK, [(5,20),(20,5),(35,20)], 2)
    return castle

def create_spelltower_sprite(tower_spec):
    base_color = tower_spec.get("color", (180,180,180))
    design = tower_spec.get("design", "default")
    surf = pygame.Surface((64,64), pygame.SRCALPHA)
    if design == "flame":
        pygame.draw.rect(surf, base_color, (20,30,24,30))
        roof_color = (min(255, int(base_color[0]*1.1)), min(255, int(base_color[1]*1.1)), min(255, int(base_color[2]*1.1)))
        pygame.draw.polygon(surf, roof_color, [(20,30),(32,10),(44,30)])
    elif design == "shield":
        pygame.draw.rect(surf, base_color, (16,28,32,36))
        battlement = (max(base_color[0]-30,0), max(base_color[1]-30,0), max(base_color[2]-30,0))
        for i in range(3):
            pygame.draw.rect(surf, battlement, (18+i*10,26,6,4))
    elif design == "sniper":
        pygame.draw.rect(surf, base_color, (26,20,12,40))
        pygame.draw.circle(surf, base_color, (32,16), 6)
    elif design == "burst":
        pygame.draw.circle(surf, base_color, (32,32), 28)
        roof_color = (min(255, int(base_color[0]*1.1)), min(255, int(base_color[1]*1.1)), min(255, int(base_color[2]*1.1)))
        pygame.draw.polygon(surf, roof_color, [(32,4),(20,28),(44,28)])
    elif design == "lightning":
        pygame.draw.polygon(surf, base_color, [(32,8),(24,20),(36,20),(28,32),(40,32),(32,44)])
    elif design == "bastion":
        pygame.draw.rect(surf, base_color, (16,28,32,32))
        pygame.draw.rect(surf, (max(base_color[0]-20,0), max(base_color[1]-20,0), max(base_color[2]-20,0)), (16,28,32,32), 3)
    elif design == "hybrid":
        left_color = base_color
        passive_colors = {p["id"]: p["icon_color"] for p in PASSIVE_POOL}
        if "hybrid" in tower_spec and len(tower_spec["hybrid"]) > 0:
            right_color = passive_colors.get(tower_spec["hybrid"][0], base_color)
        else:
            right_color = base_color
        pygame.draw.rect(surf, left_color, (10,20,22,40))
        pygame.draw.rect(surf, right_color, (32,20,22,40))
        pygame.draw.rect(surf, BLACK, (10,20,44,40), 2)
    else:
        pygame.draw.circle(surf, base_color, (32,32), 28)
        pygame.draw.circle(surf, (max(base_color[0]-30,0), max(base_color[1]-30,0), max(base_color[2]-30,0)), (32,32), 28, 3)
    return surf

def create_tower_attack_sprites(tower_spec):
    idle = create_spelltower_sprite(tower_spec)
    attack = []
    base_color = tower_spec.get("color", (180,180,180))
    aura_color = (min(255, int(base_color[0]*1.2)), min(255, int(base_color[1]*1.2)), min(255, int(base_color[2]*1.2)), 80)
    aura_radii = [36, 32, 28, 32, 36, 32]
    for i in range(6):
        frame = idle.copy()
        aura = pygame.Surface((64,64), pygame.SRCALPHA)
        pygame.draw.circle(aura, aura_color, (32,32), aura_radii[i])
        frame.blit(aura, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        attack.append(frame)
    return {"idle": idle, "attack": attack}

def create_demon_sprites(demon_type, base_color):
    sprites = []
    for frame in range(6):
        surf = pygame.Surface((40,40), pygame.SRCALPHA)
        shift = frame % 3
        if demon_type == "Fast Demon":
            pts = [(20,4+shift),(28,10),(34,20),(28,30),(20,34-shift),(12,30),(8,20),(12,10)]
        elif demon_type == "Tank Demon":
            pts = [(12,10+shift),(32,6),(38,20),(32,34),(12,30),(4,20)]
        elif demon_type == "Stealth Demon":
            pts = [(20,4+shift),(30,10),(36,20),(30,30),(20,36),(10,30),(4,20),(10,10)]
        elif demon_type == "Special Demon":
            pts = [(20,6+shift),(32,10),(38,20),(32,30),(20,34),(8,30),(2,20),(8,10)]
        elif demon_type == "Dark Demon":
            pts = [(20,4+shift),(30,10),(36,20),(30,30),(20,34),(10,30),(4,20),(10,10)]
        elif demon_type == "Frost Demon":
            pts = [(20,4+shift),(30,8),(36,16),(32,26),(20,30),(8,26),(4,16),(10,8)]
        elif demon_type == "Storm Demon":
            pts = [(20,2+shift),(34,6),(38,16),(34,26),(20,30),(6,26),(2,16),(6,6)]
        elif demon_type == "Venom Demon":
            pts = [(20,6+shift),(30,12),(36,20),(30,28),(20,34),(10,28),(4,20),(10,12)]
        elif demon_type == "Necro Demon":
            pts = [(20,4+shift),(32,8),(38,18),(32,28),(20,34),(8,28),(2,18),(8,8)]
        elif demon_type == "Celestial Demon":
            pts = [(20,2+shift),(32,6),(38,16),(32,26),(20,30),(8,26),(2,16),(8,6)]
        else:
            pts = [(20,4+shift),(30,10),(36,20),(30,30),(20,34),(10,30),(4,20),(10,10)]
        pygame.draw.polygon(surf, base_color, pts)
        pygame.draw.polygon(surf, BLACK, pts, 2)
        pygame.draw.circle(surf, WHITE, (12,20), 4)
        pygame.draw.circle(surf, BLACK, (12,20), 2)
        pygame.draw.circle(surf, WHITE, (28,20), 4)
        pygame.draw.circle(surf, BLACK, (28,20), 2)
        sprites.append(surf)
    return sprites

def create_projectile_sprites(element):
    sprites = []
    for frame in range(3):
        surf = pygame.Surface((16,16), pygame.SRCALPHA)
        if element=="flame":
            pygame.draw.circle(surf, (255,69,0), (8,8), 5+frame)
            pygame.draw.circle(surf, (255,140,0), (8,8), 3+frame)
        elif element=="frost":
            pts = [(4+frame,2),(12-frame,2),(14-frame,8),(12-frame,14),(4+frame,14),(2+frame,8)]
            pygame.draw.polygon(surf, (173,216,230), pts)
            pygame.draw.polygon(surf, (0,0,255), pts, 1)
        elif element=="lightning":
            pts = [(2,8-frame),(8,4+frame),(14,8-frame),(8,12+frame)]
            pygame.draw.lines(surf, (255,255,0), False, pts, 2)
        elif element=="arrow":
            pts = [(2,8),(14,8),(10,5+frame),(10,11-frame)]
            pygame.draw.polygon(surf, (192,192,192), pts)
        elif element=="serpent":
            pygame.draw.circle(surf, (0,255,0), (8,8), 6+frame)
            pygame.draw.line(surf, (0,180,0), (8,8),(8,14-frame), 2)
        elif element=="toxin":
            pygame.draw.circle(surf, (75,0,130), (8,8), 7)
            pygame.draw.circle(surf, (125,0,180), (8,8), 4+frame)
        elif element=="wind":
            pygame.draw.arc(surf, (123,104,238), (2,2,12,12), math.radians(30*frame), math.radians(150+30*frame), 2)
        elif element=="earth":
            pygame.draw.rect(surf, (139,69,19), (3,3,10,10))
            pygame.draw.rect(surf, (100,50,20), (3,3,10,10), 1)
        elif element=="shadow":
            pygame.draw.circle(surf, (75,0,130), (8,8), 6)
            pygame.draw.circle(surf, (30,0,60), (8,8), 3+frame)
        elif element=="holy":
            pygame.draw.circle(surf, (255,215,0), (8,8), 6+frame)
            pygame.draw.circle(surf, (255,255,255), (8,8), 3, 1)
        elif element=="shield":
            pygame.draw.circle(surf, (200,200,200), (8,8), 6+frame)
            pygame.draw.circle(surf, (150,150,150), (8,8), 3, 1)
        else:
            pygame.draw.circle(surf, (200,200,200), (8,8), 5)
        sprites.append(surf)
    return sprites

VIRTUAL_WIDTH = 1280
VIRTUAL_HEIGHT = 720
FPS = 60
TOP_PANEL_HEIGHT = 70
LEFT_PANEL_WIDTH = 200
RIGHT_PANEL_WIDTH = 200
INFO_PANEL_HEIGHT = 100
GRID_WIDTH = 10
GRID_HEIGHT = 10

def recalc_layout():
    global central_width, GAME_BOARD_HEIGHT, CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y
    central_width = VIRTUAL_WIDTH - LEFT_PANEL_WIDTH - RIGHT_PANEL_WIDTH
    GAME_BOARD_HEIGHT = VIRTUAL_HEIGHT - TOP_PANEL_HEIGHT - INFO_PANEL_HEIGHT
    CELL_SIZE = min(central_width // GRID_WIDTH, GAME_BOARD_HEIGHT // GRID_HEIGHT)
    GRID_OFFSET_X = LEFT_PANEL_WIDTH + (central_width - GRID_WIDTH * CELL_SIZE) // 2
    GRID_OFFSET_Y = TOP_PANEL_HEIGHT + (GAME_BOARD_HEIGHT - GRID_HEIGHT * CELL_SIZE) // 2

recalc_layout()

class PathGenerator:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.path_points = []
    def generate_path(self):
        self.path_points = []
        start = (0, self.grid_height//2)
        end = (self.grid_width-1, random.randint(0, self.grid_height-1))
        current = start
        self.path_points.append(current)
        while current != end:
            possible = []
            x, y = current
            if x+1 < self.grid_width:
                possible.append((x+1, y))
            if y-1 >= 0:
                possible.append((x, y-1))
            if y+1 < self.grid_height:
                possible.append((x, y+1))
            possible.sort(key=lambda pos: math.hypot(end[0]-pos[0], end[1]-pos[1]))
            if len(possible) > 1 and random.random() < 0.3:
                chosen = random.choice(possible[:2])
            else:
                chosen = possible[0]
            current = chosen
            if current not in self.path_points:
                self.path_points.append(current)
            if len(self.path_points) > self.grid_width * self.grid_height:
                break
        return self.path_points

class TowerDeck:
    def __init__(self, deck_size=3):
        self.deck_size = deck_size
        self.font = FANTASY_FONT_SMALL
        self.tooltip_font = FANTASY_FONT_SMALL
        self.buttons = []
        self.create_buttons()
    def create_buttons(self):
        self.buttons = []
        self.options = random.sample(TOWER_POOL, self.deck_size)
        margin = 20
        panel_height = VIRTUAL_HEIGHT - TOP_PANEL_HEIGHT
        gap = 10
        button_height = (panel_height - 2*margin - gap*(self.deck_size-1)) // self.deck_size
        button_width = LEFT_PANEL_WIDTH - 2*margin
        for i, tower_spec in enumerate(self.options):
            rect = pygame.Rect(margin, margin + i*(button_height+gap), button_width, button_height)
            self.buttons.append({"rect": rect, "tower_spec": tower_spec, "purchased": False})
    def draw(self, surface, offset=(0, TOP_PANEL_HEIGHT)):
        ox, oy = offset
        for btn in self.buttons:
            if not btn["purchased"]:
                adj_rect = btn["rect"].move(ox, oy)
                draw_big_button(surface, adj_rect, "", self.font, SHOP_BUTTON_COLOR, BLACK, WHITE)
                preview_sprite = create_spelltower_sprite(btn["tower_spec"])
                preview_sprite = pygame.transform.scale(preview_sprite, (50,50))
                preview_rect = pygame.Rect(adj_rect.centerx-25, adj_rect.y+5, 50, 50)
                surface.blit(preview_sprite, preview_rect.topleft)
                text_lines = []
                text_lines.append(btn["tower_spec"]["name"])
                if "hybrid" in btn["tower_spec"]:
                    types = ", ".join(btn["tower_spec"]["hybrid"])
                else:
                    types = btn["tower_spec"].get("design", "Unknown")
                text_lines.append("Type: " + types.capitalize())
                text_lines.append("Damage: " + str(btn["tower_spec"]["damage"]))
                text_lines.append("Speed: " + str(btn["tower_spec"]["attack_rate"]))
                text_lines.append("Range: " + str(btn["tower_spec"]["range"]))
                y_text = preview_rect.bottom + 2
                for line in text_lines:
                    t = self.tooltip_font.render(line, True, WHITE)
                    surface.blit(t, (adj_rect.x+5, y_text))
                    y_text += self.tooltip_font.get_linesize()
        current_time = pygame.time.get_ticks()/1000.0
        random.seed(int(current_time*0.3))
        for _ in range(2):
            sx = random.randint(0, LEFT_PANEL_WIDTH)
            sy = random.randint(TOP_PANEL_HEIGHT, TOP_PANEL_HEIGHT+(VIRTUAL_HEIGHT-TOP_PANEL_HEIGHT))
            radius = random.randint(2,3)
            pygame.draw.circle(surface, YELLOW, (sx, sy), radius)
    def handle_event(self, event, game_manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            local_pos = (pos[0], pos[1]-TOP_PANEL_HEIGHT)
            for i, btn in enumerate(self.buttons):
                if btn["rect"].collidepoint(local_pos) and not btn["purchased"]:
                    if game_manager.gold >= 25:
                        game_manager.gold -= 25
                        btn["purchased"] = True
                        game_manager.current_tower_selection = btn["tower_spec"].copy()
                        self.buttons.pop(i)
                    break

class PassiveTracker:
    def __init__(self, font):
        self.font = FANTASY_FONT_SMALL
        self.passives = {}
        for p in PASSIVE_POOL:
            self.passives[p["id"]] = {"data": p, "stack": 0}
        self.rect = pygame.Rect(VIRTUAL_WIDTH - RIGHT_PANEL_WIDTH, TOP_PANEL_HEIGHT, RIGHT_PANEL_WIDTH, VIRTUAL_HEIGHT - TOP_PANEL_HEIGHT - INFO_PANEL_HEIGHT)
    def draw(self, surface):
        pygame.draw.rect(surface, LIGHT_BLUE, self.rect, border_radius=8)
        padding = 12
        y = self.rect.y + padding
        for pid in self.passives:
            p = self.passives[pid]
            icon_rect = pygame.Rect(self.rect.x + padding, y, 40, 40)
            pygame.draw.circle(surface, p["data"]["icon_color"], icon_rect.center, 20)
            txt = self.font.render(p["data"]["name"], True, BLACK)
            surface.blit(txt, txt.get_rect(midleft=(icon_rect.right+5, icon_rect.centery)))
            if p["stack"] > 0:
                stack_txt = self.font.render(str(p["stack"]), True, RED)
                surface.blit(stack_txt, (icon_rect.right-10, icon_rect.bottom-15))
            y += 40 + padding

class InfoScreen:
    def __init__(self, font):
        self.font = INFO_FONT
        self.pages = ["How to Play", "Spellbook", "Demonology", "Passives"]
        self.current_page = "How to Play"
        self.page_buttons = []
        btn_width = 140
        btn_height = 40
        gap = 12
        total_width = len(self.pages)*btn_width + (len(self.pages)-1)*gap
        start_x = 120 + (VIRTUAL_WIDTH - 240 - total_width)//2
        y = 140
        for page in self.pages:
            rect = pygame.Rect(start_x, y, btn_width, btn_height)
            self.page_buttons.append((rect, page))
            start_x += btn_width + gap
        self.resume_button = pygame.Rect(VIRTUAL_WIDTH//2 - 140, VIRTUAL_HEIGHT-100, 120, 50)
        self.reset_button = pygame.Rect(VIRTUAL_WIDTH//2 + 20, VIRTUAL_HEIGHT-100, 120, 50)
    def draw(self, surface):
        overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,220))
        surface.blit(overlay, (0,0))
        modal_rect = pygame.Rect(80,80,VIRTUAL_WIDTH-160,VIRTUAL_HEIGHT-160)
        pygame.draw.rect(surface, LIGHT_GRAY, modal_rect, border_radius=12)
        pygame.draw.rect(surface, BLACK, modal_rect, 4, border_radius=12)
        title = self.font.render("Information - " + self.current_page, True, BLACK)
        surface.blit(title, title.get_rect(center=(modal_rect.centerx, modal_rect.top+40)))
        for rect, page in self.page_buttons:
            draw_big_button(surface, rect, page, self.font, GREEN if page==self.current_page else LIGHT_BLUE, BLACK, BLACK)
        content_rect = pygame.Rect(modal_rect.left+20, modal_rect.top+90, modal_rect.width-40, modal_rect.height-100)
        pygame.draw.rect(surface, WHITE, content_rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, content_rect, 3, border_radius=8)
        if self.current_page == "How to Play":
            instructions = ("Place towers for 25 gold each. Right-click to upgrade (3 levels). Press SPACE or START to begin a wave. Every 5 rounds, the enemy count doubles.")
            lines = wrap_text(instructions, self.font, content_rect.width-10)
            y_text = content_rect.top+8
            for line in lines:
                t = self.font.render(line, True, BLACK)
                surface.blit(t, (content_rect.left+8, y_text))
                y_text += self.font.get_linesize()+4
        elif self.current_page == "Spellbook":
            y_text = content_rect.top+8
            for elem in ELEMENTS_INFO:
                pygame.draw.circle(surface, elem["color"], (content_rect.left+20, y_text+10), 10)
                t = self.font.render(f"{elem['element']}: {elem['description']}", True, BLACK)
                surface.blit(t, (content_rect.left+40, y_text))
                y_text += self.font.get_linesize()+4
        elif self.current_page == "Demonology":
            y_text = content_rect.top+8
            for demon in DEMON_INFO:
                pygame.draw.circle(surface, demon["icon_color"], (content_rect.left+20, y_text+10), 10)
                t = self.font.render(f"{demon['type']}: {demon['description']}", True, BLACK)
                surface.blit(t, (content_rect.left+40, y_text))
                y_text += self.font.get_linesize()+4
        elif self.current_page == "Passives":
            y_text = content_rect.top+8
            for passive in PASSIVE_POOL:
                pygame.draw.circle(surface, passive["icon_color"], (content_rect.left+20, y_text+10), 10)
                t = self.font.render(f"{passive['name']}: {passive['description']}", True, BLACK)
                surface.blit(t, (content_rect.left+40, y_text))
                y_text += self.font.get_linesize()+4
        draw_big_button(surface, self.resume_button, "Resume", self.font, GREEN, BLACK, BLACK)
        draw_big_button(surface, self.reset_button, "Reset", self.font, RED, BLACK, BLACK)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for rect, page in self.page_buttons:
                if rect.collidepoint(pos):
                    self.current_page = page
                    return "stay"
            if self.resume_button.collidepoint(pos):
                return "resume"
            if self.reset_button.collidepoint(pos):
                return "reset"
        return "stay"

class Enemy:
    def __init__(self, path, speed=50, health=100):
        self.path = path
        self.pos = self.grid_to_screen(self.path[0])
        self.speed = speed
        self.health = health
        self.current_target_index = 1
        self.alive = True
        self.rewarded = False
        self.slow_timer = 0
        self.slow_factor = 1.0
        self.dot_timer = 0
        self.dot_damage = 0
        self.reversed_timer = 0
        self.element = "dark"
        self.weakness = "swirl"
        self.type = "demon"
        self.custom_color = RED
        self.sprites = None
        self.anim_frame = 0
        self.anim_timer = 0.1
        self.status_tint = None
        self.tint_timer = 0
    def grid_to_screen(self, grid_coord):
        x, y = grid_coord
        return [GRID_OFFSET_X + x * CELL_SIZE + CELL_SIZE//2,
                GRID_OFFSET_Y + y * CELL_SIZE + CELL_SIZE//2]
    def update(self, dt):
        if self.reversed_timer > 0 and self.current_target_index > 0:
            target = self.grid_to_screen(self.path[self.current_target_index-1])
            self.reversed_timer -= dt
            if self.reversed_timer <= 0:
                target = self.grid_to_screen(self.path[self.current_target_index])
            else:
                if math.hypot(self.pos[0]-target[0], self.pos[1]-target[1]) < 5:
                    self.current_target_index = max(self.current_target_index-1, 0)
        else:
            target = self.grid_to_screen(self.path[self.current_target_index])
        if self.slow_timer > 0:
            self.slow_timer -= dt
            if self.slow_timer <= 0: self.slow_factor = 1.0
        if self.dot_timer > 0:
            self.take_damage(self.dot_damage * dt)
            self.dot_timer -= dt
        if self.tint_timer > 0:
            self.tint_timer -= dt
        else:
            self.status_tint = None
        if not self.alive or self.current_target_index >= len(self.path): return
        dx = target[0]-self.pos[0]
        dy = target[1]-self.pos[1]
        distance = math.hypot(dx,dy)
        if distance:
            dir_x, dir_y = dx/distance, dy/distance
        else:
            dir_x, dir_y = 0,0
        current_speed = self.speed * self.slow_factor
        travel = current_speed * dt
        if travel >= distance:
            self.pos = target
            if self.reversed_timer > 0 and self.current_target_index > 0:
                self.current_target_index = max(self.current_target_index-1, 0)
            else:
                self.current_target_index += 1
        else:
            self.pos[0] += dir_x * travel
            self.pos[1] += dir_y * travel
        self.anim_timer -= dt
        if self.anim_timer <= 0:
            self.anim_frame = (self.anim_frame+1) % 6
            self.anim_timer = 0.1
    def draw(self, surface):
        if self.sprites:
            pos_int = (int(self.pos[0])-20, int(self.pos[1])-20)
            surface.blit(self.sprites[self.anim_frame], pos_int)
        bar_width = 30; bar_height = 4; ratio = max(self.health,0)/100
        bar_x = int(self.pos[0])-bar_width//2; bar_y = int(self.pos[1])-26
        pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, int(bar_width*ratio), bar_height))
        if self.status_tint:
            tint = pygame.Surface((40,40), pygame.SRCALPHA)
            tint.fill(self.status_tint)
            surface.blit(tint, (int(self.pos[0])-20, int(self.pos[1])-20))
    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0: self.alive = False
    def reached_end(self):
        return self.current_target_index >= len(self.path)

class Tower:
    def __init__(self, grid_pos, tower_spec):
        self.grid_pos = grid_pos
        self.pos = self.grid_to_screen(grid_pos)
        self.tower_spec = tower_spec.copy()
        self.range_radius = tower_spec["range"]
        self.damage = tower_spec["damage"]
        self.attack_rate = tower_spec["attack_rate"] * 1.2
        self.cooldown = 0
        self.upgrade_level = 0
        self.show_range = True
        self.range_display_timer = 0
        sprite_set = create_tower_attack_sprites(tower_spec)
        self.idle_sprite = sprite_set["idle"]
        self.attack_sprites = sprite_set["attack"]
        self.attack_anim_frame = 0
        self.attack_anim_timer = 0.2
    def grid_to_screen(self, grid_coord):
        x, y = grid_coord
        return [GRID_OFFSET_X + x * CELL_SIZE + CELL_SIZE//2,
                GRID_OFFSET_Y + y * CELL_SIZE + CELL_SIZE//2]
    def update(self, dt, demons, animations, passives):
        if self.range_display_timer > 0:
            self.range_display_timer -= dt
        else:
            self.show_range = False
        self.cooldown -= dt
        effective_range = self.range_radius * passives["range"]
        effective_rate = self.attack_rate * passives["attack_speed"]
        for demon in demons:
            if demon.alive:
                dist = math.hypot(demon.pos[0]-self.pos[0], demon.pos[1]-self.pos[1])
                if dist <= effective_range and self.cooldown <= 0:
                    dmg = self.damage * passives["damage"]
                    design = self.tower_spec.get("design")
                    if "hybrid" in self.tower_spec:
                        split_dmg = dmg / len(self.tower_spec["hybrid"])
                        for elem in self.tower_spec["hybrid"]:
                            apply_effect(elem, demon, split_dmg, animations, self.pos)
                        self.cooldown = 1.0 / effective_rate
                    else:
                        apply_effect(design, demon, dmg, animations, self.pos)
                        self.cooldown = 1.0 / effective_rate
                    self.attack_anim_timer = 0.2
                    break
        self.attack_anim_timer -= dt
        if self.attack_anim_timer <= 0:
            self.attack_anim_frame = (self.attack_anim_frame+1) % 6
            self.attack_anim_timer = 0.2
    def draw(self, surface):
        pos_int = (int(self.pos[0])-32, int(self.pos[1])-32)
        if self.cooldown > 0.1:
            surface.blit(self.idle_sprite, pos_int)
        else:
            surface.blit(self.attack_sprites[self.attack_anim_frame], pos_int)
        if self.upgrade_level >= 1:
            pygame.draw.rect(surface, GOLD, (int(self.pos[0])-32, int(self.pos[1])-32, 12, 12))
        if self.upgrade_level >= 2:
            pygame.draw.rect(surface, YELLOW, (int(self.pos[0])-20, int(self.pos[1])-32, 12, 12))

class FancyAttackAnimation:
    def __init__(self, start, end, duration, color, element=None):
        self.start = start.copy()
        self.end = end.copy()
        self.duration = duration
        self.elapsed = 0.0
        self.color = color
        self.element = element
        self.projectile_sprites = create_projectile_sprites(element) if element else None
        self.anim_frame = 0
        self.anim_timer = 0.1
        self.projectile_pos = start.copy()
    def update(self, dt):
        self.elapsed += dt
        if self.projectile_sprites:
            self.anim_timer -= dt
            if self.anim_timer <= 0:
                self.anim_frame = (self.anim_frame+1) % 3
                self.anim_timer = 0.1
        frac = min(self.elapsed/self.duration, 1)
        self.projectile_pos[0] = self.start[0] + (self.end[0]-self.start[0])*frac
        self.projectile_pos[1] = self.start[1] + (self.end[1]-self.start[1])*frac
    def draw(self, surface):
        pos = (int(self.projectile_pos[0]), int(self.projectile_pos[1]))
        if self.projectile_sprites:
            surface.blit(self.projectile_sprites[self.anim_frame], (pos[0]-8, pos[1]-8))
        else:
            pygame.draw.circle(surface, self.color, pos, 6)
        if self.element == "toxin":
            pygame.draw.circle(surface, (75,0,130,100), pos, 12)
        elif self.element == "lightning":
            mid = ((self.start[0]+self.end[0])//2 + random.randint(-5,5),
                   (self.start[1]+self.end[1])//2 + random.randint(-5,5))
            pygame.draw.lines(surface, (255,0,0), False, [self.start, mid, self.end], 2)
        elif self.element == "flame":
            pygame.draw.circle(surface, (255,69,0), pos, 10, 2)
    def is_finished(self):
        return self.elapsed >= self.duration

def apply_effect(element, demon, dmg, animations, tower_pos):
    if element == "frost":
        demon.slow_factor = 0.5; demon.slow_timer = 2
    elif element == "wind":
        demon.reversed_timer = 1
    elif element == "toxin":
        demon.dot_timer = 3; demon.dot_damage = 5
    elif element == "earth":
        demon.slow_factor = 0.8; demon.slow_timer = 2
    elif element == "shadow":
        demon.slow_factor = 0.7; demon.slow_timer = 1.5
    elif element == "holy":
        dmg *= 1.5
    elif element == "shield":
        dmg *= 1.25
    demon.take_damage(dmg)
    if element in element_tints:
        demon.tint_timer = 1.0; demon.status_tint = element_tints[element]
    animations.append(FancyAttackAnimation(tower_pos, demon.pos, 0.3, demon.custom_color if hasattr(demon, "custom_color") else RED, element=element))

VIRTUAL_WIDTH = 1280
VIRTUAL_HEIGHT = 720
FPS = 60
TOP_PANEL_HEIGHT = 70
LEFT_PANEL_WIDTH = 200
RIGHT_PANEL_WIDTH = 200
INFO_PANEL_HEIGHT = 100
GRID_WIDTH = 10
GRID_HEIGHT = 10

def recalc_layout():
    global central_width, GAME_BOARD_HEIGHT, CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y
    central_width = VIRTUAL_WIDTH - LEFT_PANEL_WIDTH - RIGHT_PANEL_WIDTH
    GAME_BOARD_HEIGHT = VIRTUAL_HEIGHT - TOP_PANEL_HEIGHT - INFO_PANEL_HEIGHT
    CELL_SIZE = min(central_width // GRID_WIDTH, GAME_BOARD_HEIGHT // GRID_HEIGHT)
    GRID_OFFSET_X = LEFT_PANEL_WIDTH + (central_width - GRID_WIDTH * CELL_SIZE) // 2
    GRID_OFFSET_Y = TOP_PANEL_HEIGHT + (GAME_BOARD_HEIGHT - GRID_HEIGHT * CELL_SIZE) // 2

recalc_layout()

class GameManager:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = FANTASY_FONT
        self.passive_upgrades = {"attack_speed": 1.0, "damage": 1.0, "gold": 1.0, "range": 1.0, "upgrade_cost": 1.0}
        self.routes = []
        initial_route = PathGenerator(GRID_WIDTH, GRID_HEIGHT).generate_path()
        self.routes.append(initial_route)
        self.enemies = []
        self.towers = []
        self.player_health = 10
        self.gold = 100
        self.wave = 0
        self.spawn_timer = 0
        self.spawn_interval = 0.5
        self.enemies_to_spawn = 0
        self.state = "intro"
        self.tower_deck = TowerDeck(deck_size=3)
        self.current_tower_selection = None
        self.attack_animations = []
        self.top_panel = pygame.Surface((VIRTUAL_WIDTH, TOP_PANEL_HEIGHT))
        self.top_panel.fill(DARK_GRAY)
        self.passive_tracker = PassiveTracker(self.font)
        self.info_button_rect = pygame.Rect(LEFT_PANEL_WIDTH, TOP_PANEL_HEIGHT+GAME_BOARD_HEIGHT, central_width, INFO_PANEL_HEIGHT)
        self.info_screen = InfoScreen(self.font)
        self.grid_background = self.create_grid_background()
        self.special_enemy_level = 0
        self.pending_upgrade_tower = None
        self.intro_start_button = None
        self.start_pause_button_rect = pygame.Rect(VIRTUAL_WIDTH-150, VIRTUAL_HEIGHT-80, 140, 60)
        self.passive_choices = []
        self.background_texture = create_background_texture(VIRTUAL_WIDTH, VIRTUAL_HEIGHT)
        self.previous_state = "deck"
        self.wave_timer = 0
        self.castle_sprite = create_castle_sprite()
    def update(self, dt):
        if self.state in ["intro", "upgrade_menu", "info"]:
            return
        if self.state == "playing":
            self.wave_timer += dt
            if self.enemies_to_spawn > 0:
                self.spawn_timer -= dt
                if self.spawn_timer <= 0:
                    self.spawn_enemy()
                    self.spawn_timer = self.spawn_interval
            for demon in self.enemies:
                if demon.alive:
                    demon.update(dt)
                    if demon.reached_end():
                        demon.alive = False
                        self.player_health -= 1
                        if self.player_health <= 0:
                            self.state = "gameover"
                else:
                    if not hasattr(demon, "rewarded") or not demon.rewarded:
                        self.gold += int(10 * self.passive_upgrades["gold"])
                        demon.rewarded = True
            self.enemies = [d for d in self.enemies if d.alive]
            for spelltower in self.towers:
                spelltower.update(dt, self.enemies, self.attack_animations, self.passive_upgrades)
            for anim in self.attack_animations:
                anim.update(dt)
            self.attack_animations = [anim for anim in self.attack_animations if not anim.is_finished()]
            if self.wave_timer > 3.0 and self.enemies_to_spawn <= 0 and len(self.enemies) == 0:
                self.passive_choices = random.sample(PASSIVE_POOL, 2)
                self.state = "passive_choice"
        elif self.state == "paused":
            pass
    def start_wave(self):
        self.wave += 1
        self.wave_timer = 0
        self.tower_deck = TowerDeck(deck_size=3)
        for tower in self.towers:
            tower.show_range = False
            tower.range_display_timer = 0
        base_count = 4 if self.wave == 1 else 4 + (self.wave - 1) * 2
        if self.wave % 5 == 0:
            self.enemies_to_spawn = base_count * 2
        else:
            self.enemies_to_spawn = base_count
        self.spawn_timer = self.spawn_interval
        self.state = "playing"
    def spawn_enemy(self):
        base_speed = 50 + self.wave * 1.0
        base_health = 100 + self.wave * 1
        r = random.random()
        demon = None
        if r < 0.10:
            speed = base_speed * 1.5; health = int(base_health * 0.7)
            color = (255,100,150)
            demon = Enemy(random.choice(self.routes), speed=speed, health=health)
            demon.custom_color = color; demon.type = "Fast Demon"; demon.element = "wind"; demon.weakness = "frost"
        elif r < 0.20:
            speed = base_speed * 0.7; health = int(base_health * 2)
            color = (50,150,200)
            demon = Enemy(random.choice(self.routes), speed=speed, health=health)
            demon.custom_color = color; demon.type = "Tank Demon"; demon.element = "earth"; demon.weakness = "shield"
        elif r < 0.30:
            speed = base_speed; health = int(base_health * 0.8)
            color = (150,150,50)
            demon = Enemy(random.choice(self.routes), speed=speed, health=health)
            demon.custom_color = color; demon.type = "Stealth Demon"; demon.element = "shadow"; demon.weakness = "swirl"
        elif r < 0.40:
            speed = base_speed + 5; health = int(base_health * 1.2)
            color = (200,100,255)
            demon = Enemy(random.choice(self.routes), speed=speed, health=health)
            demon.custom_color = color; demon.type = "Special Demon"; demon.element = "fire"; demon.weakness = "serpent"
        elif r < 0.50:
            speed = base_speed; health = base_health
            color = (100,50,50)
            demon = Enemy(random.choice(self.routes), speed=speed, health=health)
            demon.custom_color = color; demon.type = "Dark Demon"; demon.element = "dark"; demon.weakness = "swirl"
        elif r < 0.60:
            speed = base_speed * 0.9; health = int(base_health * 1.1)
            color = (150,220,255)
            demon = Enemy(random.choice(self.routes), speed=speed, health=health)
            demon.custom_color = color; demon.type = "Frost Demon"; demon.element = "frost"; demon.weakness = "fire"
        elif r < 0.70:
            speed = base_speed * 1.2; health = int(base_health * 0.9)
            color = (255,255,100)
            demon = Enemy(random.choice(self.routes), speed=speed, health=health)
            demon.custom_color = color; demon.type = "Storm Demon"; demon.element = "lightning"; demon.weakness = "arrow"
        elif r < 0.80:
            speed = base_speed; health = int(base_health * 1.0)
            color = (100,0,200)
            demon = Enemy(random.choice(self.routes), speed=speed, health=health)
            demon.custom_color = color; demon.type = "Venom Demon"; demon.element = "toxin"; demon.weakness = "holy"
        elif r < 0.90:
            speed = base_speed * 0.8; health = int(base_health * 1.5)
            color = (120,120,120)
            demon = Enemy(random.choice(self.routes), speed=speed, health=health)
            demon.custom_color = color; demon.type = "Necro Demon"; demon.element = "shadow"; demon.weakness = "lightning"
        else:
            speed = base_speed * 1.1; health = int(base_health * 1.0)
            color = (255,200,50)
            demon = Enemy(random.choice(self.routes), speed=speed, health=health)
            demon.custom_color = color; demon.type = "Celestial Demon"; demon.element = "holy"; demon.weakness = "dark"
        demon.sprites = create_demon_sprites(demon.type, demon.custom_color if hasattr(demon, "custom_color") else RED)
        self.enemies.append(demon)
        self.enemies_to_spawn -= 1
    def upgrade_tower(self, tower):
        if tower.upgrade_level == 0 and self.gold >= int(30 * self.passive_upgrades["upgrade_cost"]):
            self.gold -= int(30 * self.passive_upgrades["upgrade_cost"])
            tower.attack_rate *= 1.5; tower.range_radius += 15; tower.upgrade_level += 1
            tower.idle_sprite = add_border(tower.idle_sprite, GOLD, 4)
            tower.attack_sprites = update_attack_sprites(tower.attack_sprites, GOLD, 4)
        elif tower.upgrade_level == 1 and self.gold >= int(50 * self.passive_upgrades["upgrade_cost"]):
            self.gold -= int(50 * self.passive_upgrades["upgrade_cost"])
            tower.attack_rate *= 2; tower.range_radius += 20; tower.upgrade_level += 1
            tower.idle_sprite = add_border(tower.idle_sprite, YELLOW, 3)
            tower.attack_sprites = update_attack_sprites(tower.attack_sprites, YELLOW, 3)
        elif tower.upgrade_level == 2 and self.gold >= int(70 * self.passive_upgrades["upgrade_cost"]):
            self.gold -= int(70 * self.passive_upgrades["upgrade_cost"])
            tower.attack_rate *= 3; tower.range_radius += 25; tower.upgrade_level += 1
            tower.idle_sprite = add_border(tower.idle_sprite, RED, 3)
            tower.attack_sprites = update_attack_sprites(tower.attack_sprites, RED, 3)
        self.attack_animations.append(FancyAttackAnimation(tower.pos, tower.pos, 0.5, GOLD, element="upgrade"))
    def rebuild_ui(self):
        recalc_layout()
        self.top_panel = pygame.Surface((VIRTUAL_WIDTH, TOP_PANEL_HEIGHT))
        self.top_panel.fill(DARK_GRAY)
        self.grid_background = self.create_grid_background()
        self.tower_deck.create_buttons()
        self.passive_tracker.rect = pygame.Rect(VIRTUAL_WIDTH - RIGHT_PANEL_WIDTH, TOP_PANEL_HEIGHT, RIGHT_PANEL_WIDTH, VIRTUAL_HEIGHT - TOP_PANEL_HEIGHT - INFO_PANEL_HEIGHT)
        self.info_button_rect = pygame.Rect(LEFT_PANEL_WIDTH, TOP_PANEL_HEIGHT+GAME_BOARD_HEIGHT, central_width, INFO_PANEL_HEIGHT)
        self.start_pause_button_rect = pygame.Rect(VIRTUAL_WIDTH-150, VIRTUAL_HEIGHT-80, 140, 60)
        self.background_texture = create_background_texture(VIRTUAL_WIDTH, VIRTUAL_HEIGHT)
    def create_grid_background(self):
        bg_width = GRID_WIDTH * CELL_SIZE; bg_height = GRID_HEIGHT * CELL_SIZE
        bg = pygame.Surface((bg_width, bg_height))
        for y in range(bg_height):
            ratio = y / bg_height
            r = int(30 + (70-30) * ratio)
            g = int(30 + (70-30) * ratio)
            b = int(60 + (90-60) * ratio)
            pygame.draw.line(bg, (r, g, b), (0, y), (bg_width, y))
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                cell_rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                base_color = DARK_BROWN if (x+y)%2==0 else (60,50,40)
                if any((x,y) in route for route in self.routes):
                    base_color = PATH_COLOR
                pygame.draw.rect(bg, base_color, cell_rect)
                rnd = random.Random(x*100+y)
                for _ in range(2):
                    dot_x = cell_rect.x + rnd.randint(2, CELL_SIZE-4)
                    dot_y = cell_rect.y + rnd.randint(2, CELL_SIZE-4)
                    pygame.draw.circle(bg, (80,70,60), (dot_x,dot_y), 2)
                pygame.draw.rect(bg, BLACK, cell_rect, 1)
        for route in self.routes:
            pts = []
            for coord in route:
                gx, gy = coord
                center = (gx*CELL_SIZE+CELL_SIZE//2, gy*CELL_SIZE+CELL_SIZE//2)
                pts.append(center)
            pygame.draw.lines(bg, RED, False, pts, 2)
            castle = create_castle_sprite()
            end_cell = route[-1]
            cx = end_cell[0]*CELL_SIZE + CELL_SIZE//2 - 20
            cy = end_cell[1]*CELL_SIZE + CELL_SIZE//2 - 20
            bg.blit(castle, (cx, cy))
        return bg
    def draw_intro(self, surface):
        surface.blit(self.background_texture, (0,0))
        overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        surface.blit(overlay, (0,0))
        title = self.font.render("Welcome to Spelltower Clash!", True, WHITE)
        surface.blit(title, title.get_rect(center=(VIRTUAL_WIDTH//2,150)))
        rules = [
            "Place your towers for 25 gold each.",
            "Right-click a tower to upgrade it (3 levels).",
            "Press SPACE or START to begin a wave.",
            "Every 5 rounds, enemy count doubles."
        ]
        for i, rule in enumerate(rules):
            txt = self.font.render(rule, True, WHITE)
            surface.blit(txt, txt.get_rect(center=(VIRTUAL_WIDTH//2,220+i*40)))
        start_button = pygame.Rect(VIRTUAL_WIDTH//2-80,400,160,70)
        draw_big_button(surface, start_button, "START", self.font, GREEN, BLACK, BLACK)
        self.intro_start_button = start_button
    def draw_info_screen(self, surface):
        self.info_screen.draw(surface)
    def draw_passive_choice_menu(self, surface):
        menu_width = 500; menu_height = 250
        menu_rect = pygame.Rect((VIRTUAL_WIDTH-menu_width)//2, (VIRTUAL_HEIGHT-menu_height)//2, menu_width, menu_height)
        pygame.draw.rect(surface, LIGHT_BLUE, menu_rect, border_radius=12)
        pygame.draw.rect(surface, BLACK, menu_rect, 4, border_radius=12)
        title_text = self.font.render("Choose a Passive Upgrade", True, BLACK)
        surface.blit(title_text, (menu_rect.x+20, menu_rect.y+20))
        self.passive_choice_buttons = []
        gap = 12; button_width = 220; button_height = 70
        for i, passive in enumerate(self.passive_choices):
            button_rect = pygame.Rect(menu_rect.x+60, menu_rect.y+70+i*(button_height+gap), button_width, button_height)
            draw_big_button(surface, button_rect, passive["name"], self.font, WHITE, BLACK, BLACK)
            icon_rect = pygame.Rect(menu_rect.x+10, button_rect.y+10, 40, 40)
            pygame.draw.circle(surface, passive["icon_color"], icon_rect.center, 20)
            self.passive_choice_buttons.append((button_rect, passive))
    def draw_info_button(self, surface):
        pygame.draw.rect(surface, LIGHT_BLUE, self.info_button_rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, self.info_button_rect, 4, border_radius=8)
        info_text = self.font.render("INFO", True, BLACK)
        surface.blit(info_text, info_text.get_rect(center=self.info_button_rect.center))
    def draw_start_pause_button(self, surface):
        text = "START" if self.state in ["deck", "paused"] else "PAUSE" if self.state=="playing" else ""
        draw_big_button(surface, self.start_pause_button_rect, text, self.font, GREEN, BLACK, BLACK)
    def draw_top_panel(self, surface):
        self.top_panel.fill(DARK_GRAY)
        hud_text = f"Health: {self.player_health}   Gold: {int(self.gold)}   Wave: {self.wave}"
        hud_surface = self.font.render(hud_text, True, WHITE)
        self.top_panel.blit(hud_surface, (20,10))
        surface.blit(self.top_panel, (0,0))
    def draw(self, surface):
        surface.fill(DARK_GRAY)
        if self.state=="intro":
            self.draw_intro(surface); return
        if self.state=="info":
            self.draw_info_screen(surface); return
        if self.state=="passive_choice":
            self.draw_passive_choice_menu(surface); return
        surface.blit(self.grid_background, (GRID_OFFSET_X, GRID_OFFSET_Y))
        for spelltower in self.towers:
            spelltower.draw(surface)
        for demon in self.enemies:
            demon.draw(surface)
        for anim in self.attack_animations:
            anim.draw(surface)
        self.draw_top_panel(surface)
        shop_rect = pygame.Rect(0, TOP_PANEL_HEIGHT, LEFT_PANEL_WIDTH, GAME_BOARD_HEIGHT+INFO_PANEL_HEIGHT)
        pygame.draw.rect(surface, LIGHT_GRAY, shop_rect)
        if self.state in ["deck", "paused"]:
            self.tower_deck.draw(surface, offset=(0, TOP_PANEL_HEIGHT))
        self.passive_tracker.draw(surface)
        self.draw_info_button(surface)
        self.draw_start_pause_button(surface)
        if self.state=="upgrade_menu" and self.pending_upgrade_tower is not None:
            upgrade_rect = pygame.Rect(self.pending_upgrade_tower.pos[0]-60, self.pending_upgrade_tower.pos[1]-60, 150, 70)
            draw_big_button(surface, upgrade_rect, "Upgrade?\nCost: 30 Gold", self.font, LIGHT_BLUE, BLACK, BLACK)
            self.upgrade_menu_upgrade_rect = upgrade_rect
        if self.state=="gameover":
            gameover_text = self.font.render("GAME OVER", True, RED)
            surface.blit(gameover_text, gameover_text.get_rect(center=(VIRTUAL_WIDTH//2, VIRTUAL_HEIGHT//2)))
    def draw_info_screen(self, surface):
        self.info_screen.draw(surface)
    def handle_event(self, event):
        if self.state=="intro":
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if self.intro_start_button and self.intro_start_button.collidepoint(pos):
                    self.state = "deck"
            return
        if self.state=="info":
            if event.type == pygame.MOUSEBUTTONDOWN:
                res = self.info_screen.handle_event(event)
                if res=="resume":
                    self.state = self.previous_state
                elif res=="reset":
                    self.__init__()
                    self.state = "intro"
            return
        if self.state=="upgrade_menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if self.upgrade_menu_upgrade_rect and self.upgrade_menu_upgrade_rect.collidepoint(pos):
                    self.upgrade_tower(self.pending_upgrade_tower)
                    self.pending_upgrade_tower = None
                    self.state = "deck"
                    return
            return
        if self.state=="passive_choice":
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for button_rect, passive in self.passive_choice_buttons:
                    if button_rect.collidepoint(pos):
                        self.passive_tracker.passives[passive["id"]]["stack"] += 1
                        self.state = "deck"
                        self.passive_choices = []
                        return
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if self.info_button_rect.collidepoint(pos):
                self.previous_state = self.state
                self.state = "info"
                return
            if self.start_pause_button_rect.collidepoint(pos):
                if self.state in ["deck", "paused"]:
                    self.state = "playing"
                    self.start_wave()
                elif self.state=="playing":
                    self.state = "paused"
                return
            if pos[0] < LEFT_PANEL_WIDTH:
                if self.tower_deck.buttons:
                    self.tower_deck.handle_event(event, self)
            else:
                if event.button == 1:
                    if (GRID_OFFSET_X <= pos[0] < GRID_OFFSET_X+GRID_WIDTH*CELL_SIZE and
                        GRID_OFFSET_Y <= pos[1] < GRID_OFFSET_Y+GRID_HEIGHT*CELL_SIZE):
                        if self.current_tower_selection:
                            grid_x = (pos[0]-GRID_OFFSET_X)//CELL_SIZE
                            grid_y = (pos[1]-GRID_OFFSET_Y)//CELL_SIZE
                            if not any((grid_x,grid_y) in route for route in self.routes) and not any(tower.grid_pos==(grid_x,grid_y) for tower in self.towers):
                                new_tower = Tower((grid_x,grid_y), self.current_tower_selection)
                                self.towers.append(new_tower)
                                self.current_tower_selection = None
                elif event.button == 3:
                    if (GRID_OFFSET_X <= pos[0] < GRID_OFFSET_X+GRID_WIDTH*CELL_SIZE and
                        GRID_OFFSET_Y <= pos[1] < GRID_OFFSET_Y+GRID_HEIGHT*CELL_SIZE):
                        grid_x = (pos[0]-GRID_OFFSET_X)//CELL_SIZE
                        grid_y = (pos[1]-GRID_OFFSET_Y)//CELL_SIZE
                        for tower in self.towers:
                            if tower.grid_pos==(grid_x,grid_y):
                                self.pending_upgrade_tower = tower
                                self.state = "upgrade_menu"
                                break
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.state=="deck":
                    self.state = "playing"
                    self.start_wave()
                elif self.state=="playing":
                    self.state = "paused"
                elif self.state=="paused":
                    self.state = "playing"
            return

def add_border(surf, color, thickness):
    new_surf = surf.copy()
    pygame.draw.rect(new_surf, color, new_surf.get_rect(), thickness)
    return new_surf

def update_attack_sprites(attack_sprites, color, thickness):
    new_sprites = []
    for sprite in attack_sprites:
        new_sprite = sprite.copy()
        pygame.draw.rect(new_sprite, color, new_sprite.get_rect(), thickness)
        new_sprites.append(new_sprite)
    return new_sprites

def main():
    global VIRTUAL_WIDTH, VIRTUAL_HEIGHT
    window = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Spelltower Clash")
    gm = GameManager()
    virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
    running = True
    while running:
        dt = gm.clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                VIRTUAL_WIDTH, VIRTUAL_HEIGHT = event.size
                window = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)
                gm.rebuild_ui()
                virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
            gm.handle_event(event)
        gm.update(dt)
        gm.draw(virtual_surface)
        scaled = pygame.transform.scale(virtual_surface, window.get_size())
        window.blit(scaled, (0,0))
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
