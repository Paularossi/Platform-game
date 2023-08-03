import arcade

SCREEN_TITLE = "Platformer"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
VIEWPORT_MARGIN = 40

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.6
TILE_SCALING = 1
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
# Player starting position
PLAYER_START_X = 64
PLAYER_START_Y = 225

# Layer Names from our TileMap
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_HIDDEN_COINS = "Hidden Coins"
LAYER_NAME_NEXT_LEVEL = "Next level"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_DONT_TOUCH = "Don't Touch"

# D:\python files\Platform-game\resources\maps\icons\background.tsx
# resources\maps\icons\background.tsx

class MyGame(arcade.Window):

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        self.tile_map = None
        self.scene = None

        self.player_sprite = None
        self.physics_engine = None
        self.map_width = 0
        self.map_height = 0
        self.game_over = False

        self.camera = None
        self.gui_camera = None

        self.score = 0
        self.reset_score = True
        self.level = 1


    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Map name
        #map_name = f":resources:tiled_maps/map2_level_{self.level}.json"
        map_name = "./resources/maps/grass map/newmap.json"

        # Layer specific options are defined based on Layer names in a dictionary
        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_DONT_TOUCH: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_NEXT_LEVEL: {
                "use_spatial_hash": True,
            }
        }


        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = arcade.Sprite("./resources/other/female_idle.png", CHARACTER_SCALING)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        # Set up the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        # Center camera on user
        self.center_camera_to_player()

        # Calculate the total width and height of the map in pixels
        self.map_width = self.tile_map.width * GRID_PIXEL_SIZE
        self.map_height = self.tile_map.height * GRID_PIXEL_SIZE # top of map    

        # # Set the window size to match the size of the map
        # self.set_size(map_width_pixels, map_height_pixels)

        # # Set the boundaries for the camera
        # self.set_viewport(0, map_width_pixels, 0, map_height_pixels)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Initially, hide the "Hidden Coins" layer
        self.scene[LAYER_NAME_HIDDEN_COINS].visible = False

        # Keep track of the score, make sure we keep the score if the player finishes a level
        if self.reset_score:
            self.score = 0
        self.reset_score = True

        self.hidden_coins_list = arcade.SpriteList()

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant=GRAVITY,
            walls=self.scene[LAYER_NAME_PLATFORMS],
        )
        self.game_over = False

    def on_resize(self, width, height):
        self.camera.resize(width, height)
        self.gui_camera.resize(width, height)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.BLACK, 18)


    def on_key_press(self, key, modifiers):
        # Jump
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        # Left
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        # Right
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Check if the player is colliding with the door and presses Enter
        if key == arcade.key.ENTER and arcade.check_for_collision_with_list(self.player_sprite, 
                                                                  self.scene[LAYER_NAME_HIDDEN_COINS]):
            self.advance_to_next_level()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        # Find where player is, then calculate lower left corner from that
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # Set some limits on how far we scroll
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        # Here's our center, move to it
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)
        """     # Find where the player is
        player_center_x = self.player_sprite.center_x
        player_center_y = self.player_sprite.center_y

        # Get the dimensions of the map
        map_width = self.tile_map.width * GRID_PIXEL_SIZE
        map_height = self.tile_map.height * GRID_PIXEL_SIZE

        # Get the dimensions of the window
        window_width = self.width
        window_height = self.height

        # Calculate the left and right boundaries of the camera
        left_boundary = window_width // 2
        right_boundary = map_width - window_width // 2

        # Calculate the bottom and top boundaries of the camera
        bottom_boundary = window_height // 2
        top_boundary = map_height - window_height // 2

        # Calculate the new camera center
        camera_center_x = min(max(player_center_x, left_boundary), right_boundary)
        camera_center_y = min(max(player_center_y, bottom_boundary), top_boundary)

        # Set the new camera center
        self.camera.center_x = camera_center_x
        self.camera.center_y = camera_center_y """
 
    def on_update(self, delta_time):
        """Movement and game logic"""

        if self.player_sprite.right >= self.map_width:
            self.game_over = True

        # Call update on all sprites
        if not self.game_over:
            self.physics_engine.update()

        # See if we hit any coins
        coins_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_COINS]
        )
        # Check for collisions between the player and the hidden coins layer
        hidden_coins_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_HIDDEN_COINS]
        )

        # If the player collides with any hidden coins, make the "Hidden Coins" layer visible
        if hidden_coins_hit:
            self.scene[LAYER_NAME_HIDDEN_COINS].visible = True

        # Loop through each coin we hit (if any) and remove it
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 1

        # Loop through each hidden coin we hit (if any) and remove it from both lists
        for hidden_coin in hidden_coins_hit:
            hidden_coin.remove_from_sprite_lists()
            # Increment the score for collecting hidden coins (if desired)
            self.score += 1

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
           self.player_sprite.center_x = PLAYER_START_X
           self.player_sprite.center_y = PLAYER_START_Y

            #arcade.play_sound(self.game_over)

        # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_DONT_TOUCH]
        ):  
            #self.camera.shake((4, 7))
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

        # Position the camera
        self.center_camera_to_player()

    def advance_to_next_level(self):
        # Increase the level
        self.level += 1

        # Make sure to keep the score from this level when setting up the next level
        self.reset_score = False
        print("Next level loading")
        # Load the next level
        #self.setup()

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()