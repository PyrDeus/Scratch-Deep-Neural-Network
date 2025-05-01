

from level import Level


if __name__ == "__main__":
    level = Level()

    while True:
        criteria = level.waitEvent(time=100, verbose=False)
        if criteria == 0:
            break
        elif criteria == 2:
            level.addRandomShape()

    level.end()