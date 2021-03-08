from PIL import Image

tg_width = 900
tg_height = 720


def imageToGrayScale(filepath):
    tg = Image.open(filepath)
    tg_grayScaled = tg.convert(mode="LA")

    return tg_grayScaled


def calc_average_grayscale(tg_grayScaled):

    # [y][x]
    outputs = [[a for a in range(20)] for a in range(16)]

    init_x_offset = int((tg_grayScaled.width - tg_width)/2)

    y_offset = 0
    for row in range(16):
        x_offset = 0
        x_offset += init_x_offset
        for col in range(20):
            sum_grayscale = 0
            counter = 0

            for x in range(x_offset, x_offset+int(900/20)):
                for y in range(y_offset, y_offset+int(720/16)):
                    pixel_value = tg_grayScaled.getpixel(xy=(x, y))

                    # Grayscale value is [0]
                    sum_grayscale += pixel_value[0]
                    counter += 1

            x_offset += int(900/20)

            outputs[row][col] = int(sum_grayscale/counter)

        y_offset += int(720/16)
        # print(y_offset)

    _str = ""
    for r in range(16):
        for c in range(20):
            _str += str(f"{outputs[r][c]: 4d}")
        _str += '\n'
    # print(_str)

    return outputs


""" output value to emoji id """


def generateEmojiTable(outputs, white_threshold):
    emoji_table = []

    for row in range(0, 16, 2):
        tmp = []
        for col in range(0, 20, 2):
            res = 0
            # top left white
            if outputs[row][col] > white_threshold:
                res |= 0b1000

            # top right white
            if outputs[row][col+1] > white_threshold:
                res |= 0b0100

            # btm left white
            if outputs[row+1][col] > white_threshold:
                res |= 0b0010

            # btm right white
            if outputs[row+1][col+1] > white_threshold:
                res |= 0b0001

            tmp.append(f"{res:04b}")
        emoji_table.append(tmp)
    return emoji_table


if __name__ == '__main__':
    im = imageToGrayScale("test_images/2030.png")
    res = calc_average_grayscale(im)
    emoji_table = generateEmojiTable(res, 200)
