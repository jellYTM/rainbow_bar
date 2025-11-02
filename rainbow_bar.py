import cv2
import numpy as np

value_list = [0]
hsv_resize_rate = 3


def main(path, ksize=(21, 21)):
    frame = cv2.imread(path)
    hsv_original = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    value_original = cv2.GaussianBlur(hsv_original[:, :, 2], ksize, 1, cv2.BORDER_REPLICATE)

    cv2.namedWindow("hsv")
    cv2.setMouseCallback('hsv', onMouse, (value_original, hsv_resize_rate))

    while True:
        hsv = hsv_original.copy()
        hsv[:, :, 1] = np.ones_like(hsv[:, :, 1]) * 255

        for i, value in enumerate(value_list):
            mask = np.where(value_original >= value, True, False)
            hue = 179 / len(value_list) * i
            hsv[:, :, 0][mask] = hue

        resize_and_show_window("raw", frame)
        show_hsv(hsv, hsv_resize_rate)

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    rgb_result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    cv2.imwrite(f"{path.split(".")[0]}_rainbow.{path.split(".")[1]}", rgb_result)


def onMouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global value_list

        value_channel, resize_rate = params

        orig_x = x * resize_rate
        orig_y = y * resize_rate

        height, width = value_channel.shape

        if 0 <= orig_x < width and 0 <= orig_y < height:
            value_list.append(value_channel[orig_y, orig_x])
            value_list = list(set(value_list))
            value_list.sort()

            print(f"value_list: {value_list}")


def resize_and_show_window(window_name, frame, resize_rate=8):
    frame = cv2.resize(frame, (frame.shape[1] // resize_rate, frame.shape[0] // resize_rate))
    cv2.imshow(window_name, frame)


def show_hsv(hsv, resize_rate, name="hsv"):
    rgb_result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    resize_and_show_window(f"{name}", rgb_result, resize_rate=resize_rate)


if __name__ == "__main__":
    path = "electrophoresis.jpg"
    main(path)
