from pathlib import Path


BASE_DIR = Path(__file__).parent

GRAPHICS_DIR = BASE_DIR / "graphics"

GROUND_IMG = str(GRAPHICS_DIR / "ground.png")
PLAYER_IMG = str(GRAPHICS_DIR / "player.png")
RUNNING_ENEMY_IMG = str(GRAPHICS_DIR / "running_enemy.png")
FLYING_ENEMY_IMG = str(GRAPHICS_DIR / "flying_enemy.png")

AUDIO_DIR = BASE_DIR / "audio"

JUMP_SOUNDS = (
    str(AUDIO_DIR / "jump1.ogg"),
    str(AUDIO_DIR / "jump2.ogg"),
    str(AUDIO_DIR / "jump3.ogg"),
)

SOUNDTRACK = str(AUDIO_DIR / "soundtrack.ogg")
