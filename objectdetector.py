#
"""
Use:
python objectdetector.py -v d:/video/DJI_0008.mpg -t csrt
or
python objectdetector.py -v d:/video/car_road.avi -t csrt
or
python objectdetector.py -v ./static/car_video.mp4 -t mosse
or
python objectdetector.py -v d:/video/FlightTest/Video_2020_01_23_21_31_54.mp4 -t tld

Press "S" to stop stream and select ROI to tracking
Mouse left button select ROI than tap SPACE
Have a fun !!!
 """
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import datetime
import cv2
import sys
import time

# this is required at the time of execution
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
                help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="mosse",
                help="OpenCV object tracker type")
args = vars(ap.parse_args())

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}
tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
print("tracker: ", args["tracker"])
initBB = None

if not args.get("video", False):
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)

else:
    vs = cv2.VideoCapture(args["video"])

fps = None


def crosshire():
    cv2.line(frame, (310, 230), (330, 230), (255, 255, 0), 1)
    cv2.line(frame, (360, 230), (380, 230), (255, 255, 0), 1)
    cv2.line(frame, (330, 230), (330, 235), (255, 255, 0), 1)
    cv2.line(frame, (360, 230), (360, 235), (255, 255, 0), 1)
    return


while True:
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    if frame is None:
        print('No video file')
        break

    frame = imutils.resize(frame, width=720)
    (H, W) = frame.shape[:2]
    if initBB is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)

        # check to see if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (255, 255, 250), 1)
            crosshire()

        # update the FPS counter
        fps.update()
        fps.stop()

        # initialize the set of information we'll be displaying on
        # the frame
        info = [
            ("Tracker", args["tracker"]),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]
        dt = str(datetime.datetime.now())
        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(frame, dt, (W - 315, H - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_8)

    # show the output frame
    cv2.imshow("Start Tracking", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        initBB = cv2.selectROI("Start Tracking", frame, showCrosshair=True, fromCenter=False)
        tracker.init(frame, initBB)
        fps = FPS().start()


    elif key == ord("l"):
        initBB = cv2.selectROI("Start Tracking", frame, showCrosshair=True, fromCenter=False)
        imCrop = frame[int(initBB[1]):int(initBB[1] + initBB[3]), int(initBB[0]):int(initBB[0] + initBB[2])]
        cv2.imshow("Preview", imCrop)
        fps = FPS().start()
        cv2.waitKey(1)  # ESC pressed

    elif key == ord("x"):
        def crosshire():
            return None

    elif key == ord("c"):
        def crosshire():
            cv2.line(frame, (310, 230), (330, 230), (255, 255, 0), 1)
            cv2.line(frame, (360, 230), (380, 230), (255, 255, 0), 1)
            cv2.line(frame, (330, 230), (330, 235), (255, 255, 0), 1)
            cv2.line(frame, (360, 230), (360, 235), (255, 255, 0), 1)
            return


    elif key == ord('q'):
        print("Tracking stop by customer... ")
        break
