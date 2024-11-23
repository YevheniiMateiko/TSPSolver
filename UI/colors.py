from matplotlib import colormaps

def generate_colors(num_colors: int):
    colormap = colormaps['tab10']
    return [colormap(i / num_colors) for i in range(num_colors)]

def rgba_to_hex(color):
    r, g, b, _ = color
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
