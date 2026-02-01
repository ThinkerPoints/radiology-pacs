class TextAnnotation:
    def __init__(self, image_pos, text, font, color):
        self.image_pos = image_pos    # QPointF (image space)
        self.text = text
        self.font = font
        self.color = color
