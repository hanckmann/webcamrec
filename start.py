import cv2
import time
from pathlib import Path
from datetime import datetime

from threading import Thread
import queue

from typing import Union


def dt_name(dt: datetime) -> str:
    """Convert datetime object to path string."""
    return dt.strftime('%Y%m%d-%H%M%S-%f')


def create_path(root: Path, subfolder: Union[str, Path]) -> Path:
    """Set up path and ensure it exists."""
    newpath = root
    if not newpath.is_dir():
        raise ValueError('Root path does not exist: {}'.format(str(root)))
    newpath = newpath.joinpath(subfolder)
    if not newpath.is_dir():
        newpath.mkdir()
    return newpath


class CVReader():
    """OpenCV webcam reader."""

    def __init__(self, image_queue: queue.Queue()):
        """Init."""
        self.image_queue = image_queue
        self._running = False

    def terminate(self):
        """Terminate thread."""
        self.stop()

    def stop(self):
        """Stop webcam capturing."""
        self._running = False

    def run(self):
        """Start webcam capturing."""
        cam = cv2.VideoCapture(0)
        self._running = True
        while self._running:
            # Read frame
            ret, frame = cam.read()
            if not ret:
                print('ERROR: Failed to grab frame.')
                time.sleep(0.01)
                continue
            self.image_queue.put((frame, datetime.now()))
        cam.release()


def record_images(root_folder: Union[str, Path]):
    """Use opencv to record timestamped images from the webcam."""
    # Setup paths
    if not root_folder:
        root_folder = Path.cwd()
    root_folder = create_path(root_folder, 'data')
    current_subfolder = create_path(root_folder, dt_name(datetime.now()))
    print('Starting in new folder:', current_subfolder)
    # Setup Window
    cv2.namedWindow(__file__)
    # Setup queue and thread
    image_queue = queue.Queue()
    cvreader = CVReader(image_queue=image_queue)
    cvreader_thread = Thread(target = cvreader.run) 
    cvreader_thread.start()
    while True:
        # Get frame
        frame = None
        while not image_queue.empty():
            try:
                (frame, dt) = image_queue.get(block=True, timeout=1)
            except queue.Empty:
                frame = None
                continue

            if frame is not None:
                # Store frame
                img_name = current_subfolder.joinpath('frame_{}.png'.format(dt_name(dt)))
                cv2.imwrite(str(img_name), frame) 

        # Only the last frame in a queue is shown (else the queue will grow)
        if frame is not None:
            # Show frame
            cv2.imshow(__file__, frame)

        # User interfaction
        key = cv2.waitKey(33)
        if key == -1:
            # No key pressed
            continue
        elif key in (27, ord('q')):
            # Quit (ESC, q)
            cvreader.terminate()  
            print('Quit with:', key)
            break
        elif key in (13, 32):
            # Start in new folder (ENTER, SPACE)
            current_subfolder = create_path(root_folder, dt_name(datetime.now()))
            print('Starting in new folder:', current_subfolder)

    cv2.destroyAllWindows()
    cvreader_thread.join()


if __name__ == '__main__':
    record_images()
