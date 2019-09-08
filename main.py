import arcade
import random
import PIL

ROW_COUNT = 15
COLUMN_COUNT = 15
WIDTH = 30
HEIGHT = 30
MARGIN = 1

SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN


colors = [
          # Empty cell - White
          (255,   255,   255),
          # Wall - Brown
          (133, 87, 37),
          # Apple - Red
          (255,   0, 0),
          # Snake - Green
          (166,   200,   64)
          ]


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("Snake Game", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.BLACK, 54, align="center",
                         anchor_x="center", anchor_y="center")
        arcade.draw_text("Click to start", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 48, arcade.color.GRAY, 24,
                         align="center", anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        self.board = None
        self.frame_count = 0
        self.game_over = False
        self.paused = False
        self.board_sprite_list = None
        self.direction = (0, 1)
        self.apple_col = int(random.randint(0, COLUMN_COUNT-1))
        self.apple_row = int(random.randint(0, ROW_COUNT-1))
        self.snake = [(COLUMN_COUNT//2, ROW_COUNT//2)]
        self.texture_list = self.create_textures()
        self.dt = 0

    def create_textures(self):
        texture_list = []
        for color in colors:
            image = PIL.Image.new('RGB', (WIDTH, HEIGHT), color)
            texture_list.append(arcade.Texture(str(color), image=image))
        return texture_list

    def new_board(self):
        board = [[1 for x in range(COLUMN_COUNT)]]
        board += [[1] + [0 for x in range(COLUMN_COUNT - 2)] + [1] for y in range(ROW_COUNT - 2)]
        board += [[1 for x in range(COLUMN_COUNT)]]
        return board

    def setup(self):

        self.board = self.new_board()
        self.board_sprite_list = arcade.SpriteList()

        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                sprite = arcade.Sprite()
                for texture in self.texture_list:
                    sprite.append_texture(texture)
                sprite.set_texture(0)
                sprite.center_x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                sprite.center_y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                self.board_sprite_list.append(sprite)

        self.new_apple()
        self.update_board()

    def update(self, dt):
        self.dt += abs(dt)
        if self.dt > 0.3:
            self.move()
            self.dt -= 0.3

    def move(self):
        next_pos = tuple([x + y for x, y in zip(self.snake[0], self.direction)])
        new_x, new_y = next_pos
        new_pos_val = self.board[new_x][new_y]
        # Next = apple
        if new_pos_val == 2:
            self.window.total_score += 1
            self.board[new_x][new_y] = 3
            self.snake = [next_pos] + [x for x in self.snake]
            self.new_apple()
        # Next = tail or wall
        elif new_pos_val == 1 or new_pos_val == 3:
            game_view = GameOverView()
            self.window.show_view(game_view)
        # Next = empty
        else:
            clr_x, clr_y = self.snake[-1]
            self.board[clr_x][clr_y] = 0
            self.board[new_x][new_y] = 3
            if len(self.snake) > 1:
                self.snake = [next_pos] + [x for x in self.snake[0:len(self.snake)-1]]
            else:
                self.snake = [next_pos]
        self.update_board()

    def new_apple(self):
        self.apple_col = int(random.randint(0, COLUMN_COUNT - 1))
        self.apple_row = int(random.randint(0, ROW_COUNT - 1))
        if self.board[self.apple_col][self.apple_row] != 0:
            self.new_apple()
        else:
            self.board[self.apple_col][self.apple_row] = 2

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            if self.direction != (0, 1):
                self.direction = (0, -1)
        elif key == arcade.key.RIGHT:
            if self.direction != (0, -1):
                self.direction = (0, 1)
        elif key == arcade.key.UP:
            if self.direction != (-1, 0):
                self.direction = (1, 0)
        elif key == arcade.key.DOWN:
            if self.direction != (1, 0):
                self.direction = (-1, 0)

    def update_board(self):
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                v = self.board[row][column]
                i = row * COLUMN_COUNT + column
                self.board_sprite_list[i].set_texture(v)

    def on_draw(self):
        arcade.start_render()
        self.board_sprite_list.draw()


class GameOverView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, arcade.color.WHITE, 54, align="center",
                         anchor_x="center", anchor_y="center")
        arcade.draw_text("Click to restart", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 48, arcade.color.WHITE, 24,
                         align="center", anchor_x="center", anchor_y="center")

        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_mouse_press(self, x, y, button, modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake")
    window.total_score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
