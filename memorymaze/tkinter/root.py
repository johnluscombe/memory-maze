import tkinter as tk

from memorymaze import MemoryMaze
from memorymaze.animation import ANIMATION_DELAY
from memorymaze.tkinter.canvas.grid import GridCanvas
from memorymaze.tkinter.event import BUTTON_1
from memorymaze.tkinter.event import CONFIGURE
from memorymaze.style import BOLD
from memorymaze.style import PRIMARY_COLOR
from memorymaze.style import SECONDARY_COLOR
from memorymaze.style import WHITE

TITLE = "Memory Maze"

PLAY = "PLAY"

MEMORY_MAZE_ICON = "assets/memory-maze.ico"
MEMORY_MAZE_LOGO = "assets/memory-maze-logo.png"
LIVES_IMAGE = "assets/lives.png"


class MemoryMazeRoot(tk.Tk):
    """
    Root widget of the Tkinter window.
    """

    def __init__(self):
        super().__init__()

        self.title(TITLE)
        self.minsize(600, 600)
        self.iconbitmap(MEMORY_MAZE_ICON)
        self.configure(bg=PRIMARY_COLOR, padx=50, pady=25)

        self._memory_maze = MemoryMaze()

        self._level_text = tk.StringVar()
        self._lives_text = tk.StringVar()

        game_container = tk.Frame(self, bg=PRIMARY_COLOR)

        lives_container = tk.Frame(game_container, bg=PRIMARY_COLOR)
        lives_image = tk.PhotoImage(file=LIVES_IMAGE)
        lives_image_label = tk.Label(lives_container, image=lives_image, borderwidth=0)
        lives_image_label.image = lives_image
        lives_image_label.pack(side=tk.LEFT)
        self._lives_label = tk.Label(lives_container, textvariable=self._lives_text, font=(None, 16), bg=PRIMARY_COLOR, fg=WHITE)
        self._lives_label.pack(side=tk.LEFT)
        lives_container.place(x=0, y=25)

        self._level_label = tk.Label(game_container, textvariable=self._level_text, font=(None, 36, BOLD), bg=PRIMARY_COLOR, fg=WHITE)
        self._level_label.pack()

        grid_canvas = GridCanvas(self._memory_maze, game_container, bg=PRIMARY_COLOR, highlightthickness=0)
        grid_canvas.pack(fill=tk.BOTH, expand=True, pady=(0, 25))

        game_container.place(relx=0.5, rely=0.5, width=500, height=550, anchor=tk.CENTER)

        self._show_start_frame(grid_canvas)

        grid_canvas.bind(BUTTON_1, lambda event: self.grid_(event, grid_canvas))
        grid_canvas.bind(CONFIGURE, lambda *args: grid_canvas.redraw())
    
    def _show_start_frame(self, grid_canvas):
        """
        Shows the starting screen with the "play" button.

        Arguments:
            grid_canvas (:class:`~GridCanvas`): Grid canvas object.
        """

        frame = tk.Frame(self, bg=PRIMARY_COLOR)
        label_container = tk.Frame(frame, bg=PRIMARY_COLOR)
        logo = tk.PhotoImage(file=MEMORY_MAZE_LOGO)
        logo_label = tk.Label(label_container, image=logo, borderwidth=0)
        logo_label.image = logo
        logo_label.pack(side=tk.TOP, pady=(0, 10))
        play_button_border = tk.Frame(label_container, borderwidth=2, bg=SECONDARY_COLOR, relief=tk.FLAT)
        play_button_padding = tk.Frame(play_button_border, bg=PRIMARY_COLOR)
        play_button_label = tk.Label(play_button_padding, text=PLAY, width=10, bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, font=(None, 16, BOLD), relief=tk.FLAT)
        play_button_label.pack(padx=10, pady=10)
        play_button_padding.pack()
        play_button_border.pack(side=tk.TOP, pady=(20, 0))
        label_container.place(relx=0.5, rely=0.5, relwidth=1, anchor=tk.CENTER)
        frame.place(x=0, y=0, relwidth=1, relheight=1)

        play_button_border.bind(BUTTON_1, lambda *args: self._on_play(frame, grid_canvas))
        play_button_padding.bind(BUTTON_1, lambda *args: self._on_play(frame, grid_canvas))
        play_button_label.bind(BUTTON_1, lambda *args: self._on_play(frame, grid_canvas))
    
    def _show_game_over(self):
        """
        Shows the "game over" frame.

        Arguments:
            grid_canvas (:class:`~GridCanvas`): Grid canvas object.
        """

        frame = tk.Frame(self, bg=PRIMARY_COLOR)
        label_container = tk.Frame(frame, bg=PRIMARY_COLOR)
        logo = tk.PhotoImage(file=MEMORY_MAZE_LOGO)
        logo_label = tk.Label(label_container, image=logo, borderwidth=0)
        logo_label.image = logo
        logo_label.pack(side=tk.TOP, pady=(0, 10))
        play_button_border = tk.Frame(label_container, borderwidth=2, bg=SECONDARY_COLOR, relief=tk.FLAT)
        play_button_padding = tk.Frame(play_button_border, bg=PRIMARY_COLOR)
        play_button_label = tk.Label(play_button_padding, text=PLAY, width=10, bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, font=(None, 16, BOLD), relief=tk.FLAT)
        play_button_label.pack(padx=10, pady=10)
        play_button_padding.pack()
        play_button_border.pack(side=tk.TOP, pady=(20, 0))
        label_container.place(relx=0.5, rely=0.5, relwidth=1, anchor=tk.CENTER)
        frame.place(x=0, y=0, relwidth=1, relheight=1)

        play_button_border.bind(BUTTON_1, lambda *args: self._on_play(frame, grid_canvas))
        play_button_padding.bind(BUTTON_1, lambda *args: self._on_play(frame, grid_canvas))
        play_button_label.bind(BUTTON_1, lambda *args: self._on_play(frame, grid_canvas))
    
    def _on_play(self, start_frame, grid_canvas):
        """
        Called when the "play" button is clicked.

        Arguments:
            start_frame (:class:`~tk.Frame`): :class:`~tk.Frame` for the
                Tkinter start screen.
            grid_canvas (:class:`~GridCanvas`): Grid canvas object.
        """

        start_frame.place_forget()
        grid_canvas.redraw()
        grid_canvas.after(ANIMATION_DELAY, lambda: grid_canvas.show_path())
        self._redraw_variables()
    
    def _on_grid_canvas_click(self, event, grid_canvas):
        """
        Called when the grid is clicked.

        Arguments:
            event: Tkinter click event.
            grid_canvas (:class:`~GridCanvas`): Grid grid_canvas object.
        """

        grid_canvas.on_click(event.x, event.y)
        self._redraw_variables()
    
    def _redraw_variables(self):
        """
        Updates the game state variables, such as level and lives.
        """

        self._level_text.set(str(self._memory_maze.game_state.level))
        self._lives_text.set(str(self._memory_maze.game_state.lives))
