from roboflow import Roboflow

#https://universe.roboflow.com/ib-personal-project/galaxy-detection/dataset/3
def galaxy_detection():
    rf = Roboflow(api_key="unauthorized")
    project = rf.workspace("ib-personal-project").project("galaxy-detection")
    version = project.version(3)
    dataset = version.download("yolov11")

def galaxy_detection2(api_key):
    rf = Roboflow(api_key=api_key)
    project = rf.workspace("kaustubh-kambli").project("galaxy-classification-using-deep-learning")
    version = project.version(4)
    dataset = version.download("yolov11")
                    