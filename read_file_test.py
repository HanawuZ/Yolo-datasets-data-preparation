file_path = r"c:\Users;b6302\Desktop\PROGRAMMING\PYTHON\OBJECT-DETECTION\Yolo-datasets-data-preparation\datasets\Elephants_19.v1-v19.yolov7pytorch\train\labels\-30-Minute-Craziest-Security-Camera-Captures-_-Caught-on-Cam-_-Funny-Moments-25-50-screenshot-1-_png.rf.0db7dddc544abdb853dde52c4f57a58e.txt"

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Process the content as needed
        print(content)
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print(f"An error occurred: {e}")
