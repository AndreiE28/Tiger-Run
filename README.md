# 🐅 Tiger Run

[logo](/assets/images/logo_2.png)

**Tiger Run** is a 2D side-scrolling endless runner game built in Python using Pygame. Play as a pixel tiger dashing through the jungle, jumping over obstacles, and leveling up while grooving to retro-style background music!

## 🎮 Features

- Smooth running and jumping animations
- Obstacle spawning and collision detection
- Dynamic level progression (increased difficulty over time)
- Retro UI with settings, pause, and control menus
- Background scrolling effect
- High score saving
- Custom volume settings for music and SFX

## 🕹 Controls

- **Jump**: `SPACE`
- **Pause**: `ESCAPE`
- **Menu Navigation**: Mouse

## 📁 Project Structure

```

Tiger_Run/
├── assets/
│   ├── images/
│   │   ├── background.png
│   │   ├── obstacle.png
│   │   └── tiger_running_animation_#.png
│   └── sounds/
│       ├── background_music.mp3
│       ├── dying_sound.mp3
│       ├── jump_sound.mp3
│       ├── landing_sound.mp3
│       ├── level_up_sound.mp3
│       └── select.mp3
├── Tiger Run.py
└── highscore.txt

````

## 🛠 Requirements

- Python 3.x
- Pygame (`pip install pygame`)

## 🚀 Running the Game

1. Download or clone the repo.
2. Make sure all required assets are in place.
3. Run the game with:

```bash
python "Tiger Run.py"
````


## 🧠 How It Works

* The game features a loop that switches between menu, gameplay, pause, and game-over states.
* The tiger has a running and jumping animation handled by separate classes.
* Obstacle collision ends the run and resets the score.
* Score and difficulty increase over time, encouraging longer runs.
* Menus and volume settings are built with a reusable `Button` class.

## 🎵 Credits

* Sound effects & music: Custom / open-source retro game sounds
* Visuals: Pixel-style art and animations for a vibrant retro experience

## 📝 License

Provided for educational and entertainment use. If redistributing, ensure you have the right to use all sound and graphic assets included.

Run fast, jump hard, and don’t look back. 🐅💨
