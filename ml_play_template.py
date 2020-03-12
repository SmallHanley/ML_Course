"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False
    x = 75
    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        elif(scene_info.ball[1] < 200 and scene_info.ball[1] > 190 and scene_info.ball[1] > tmp[1]):
            x = (400 - tmp[1]) // (scene_info.ball[1] - tmp[1]) * (scene_info.ball[0] - tmp[0]) + tmp[0]
            if(x > 200):
                x = 400 - x;
            if(x < 0):
                x = -x;
            x -= 25
        elif(scene_info.ball[1] < 380 and scene_info.ball[1] > 200 and scene_info.ball[1] > tmp[1]):
            if(scene_info.platform[0] == x):
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            elif(scene_info.platform[0] > x):
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            elif(scene_info.platform[0] < x):
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        tmp = scene_info.ball
