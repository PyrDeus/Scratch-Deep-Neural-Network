

from window import Screen



if __name__ == "__main__":
    from utils import Color
    import numpy as np

    # w, h = extractMonitorDimensions()
    # w, h = 640, 480
    screen = Screen(selector=True)
    screen.show()

    while True:
        criteria = screen.waitEvent(time=100, verbose=False)
        if criteria == 0:
            break

        #screen.addShape(randomShape())

        screen.update()
    screen.destroyWindow()  # Garde-fou