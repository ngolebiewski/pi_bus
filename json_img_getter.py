import json

with open("bus.json", "r") as f:
    matrix = json.load(f)
    
def img_to_8x8_lists(matrix):
    if len(matrix) != 8:
        print("FAIL")
        return
    
    width = len(matrix[0])
    matrix_segments = [] # list of 8x8 2d arrays
    
    for i in range(width -7):
        segment = []
        # print(f"Columns {i}-{i+7}:")
        for row in range(8):
            segment.append(matrix[row][i:i+8])
        matrix_segments.append(segment)
    
    # print(matrix_segments)
    # print(len(matrix_segments))
    return matrix_segments
        
def img_scroller(sections_list):
    [print(section) for section in sections_list]

def hat_img_scroller(matrixes):
    from sense_hat import SenseHat
    import time
    
    sense = SenseHat()
    
    white = (255, 255, 255)
    black = (0, 0, 0)
    
    for section in matrixes:
        # Convert 0/1 matrix to RGB tuples
        colored_section = [
            [white if pixel == 1 else black for pixel in row]
            for row in section
        ]
        
        sense.set_pixels([pixel for row in colored_section for pixel in row])
        time.sleep(0.05)
    
    sense.clear()

def bus_scroller():
    hat_img_scroller(img_to_8x8_lists(matrix))
    

if __name__ == "__main__":
    print(matrix)
    img_scroller(img_to_8x8_lists(matrix))