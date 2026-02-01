import matplotlib.pyplot as plt
import math

# --- Variabel global untuk status bentuk terakhir ---
current_shape_data = None
current_patch = None

# --- Fungsi Gambar (mengembalikan data geometri) ---
def draw_square(ax):
    try:
        side = float(input("Masukkan panjang sisi bujursangkar: "))
        x_start = float(input("Masukkan koordinat X pojok kiri bawah: "))
        y_start = float(input("Masukkan koordinat Y pojok kiri bawah: "))
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
        return None
    if side <= 0:
        print("Panjang sisi harus lebih besar dari nol.")
        return None
    vertices = [
        (x_start, y_start),
        (x_start + side, y_start),
        (x_start + side, y_start + side),
        (x_start, y_start + side)
    ]
    print(f"Bujursangkar dengan sisi {side} digambar mulai dari ({x_start}, {y_start}).")
    return {"type": "polygon", "vertices": vertices, "color": "blue", "facecolor": "lightblue"}

def draw_triangle(ax):
    try:
        x1 = float(input("Masukkan koordinat X titik pertama: "))
        y1 = float(input("Masukkan koordinat Y titik pertama: "))
        x2 = float(input("Masukkan koordinat X titik kedua: "))
        y2 = float(input("Masukkan koordinat Y titik kedua: "))
        x3 = float(input("Masukkan koordinat X titik ketiga: "))
        y3 = float(input("Masukkan koordinat Y titik ketiga: "))
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
        return None
    vertices = [(x1, y1), (x2, y2), (x3, y3)]
    print(f"Segitiga digambar dengan titik-titik: ({x1}, {y1}), ({x2}, {y2}), ({x3}, {y3}).")
    return {"type": "polygon", "vertices": vertices, "color": "red", "facecolor": "salmon"}

def draw_rectangle(ax):
    try:
        width = float(input("Masukkan panjang (lebar) persegi panjang: "))
        height = float(input("Masukkan lebar (tinggi) persegi panjang: "))
        x_bottom_left = float(input("Masukkan koordinat X pojok kiri bawah: "))
        y_bottom_left = float(input("Masukkan koordinat Y pojok kiri bawah: "))
        if width <= 0 or height <= 0:
            print("Panjang dan lebar harus lebih besar dari nol.")
            return None
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
        return None
    vertices = [
        (x_bottom_left, y_bottom_left),
        (x_bottom_left + width, y_bottom_left),
        (x_bottom_left + width, y_bottom_left + height),
        (x_bottom_left, y_bottom_left + height)
    ]
    print(f"Persegi panjang dengan panjang {width} dan lebar {height} digambar mulai dari ({x_bottom_left}, {y_bottom_left}).")
    return {"type": "polygon", "vertices": vertices, "color": "green", "facecolor": "lightgreen"}

def draw_circle(ax):
    try:
        center_x = float(input("Masukkan koordinat X pusat lingkaran: "))
        center_y = float(input("Masukkan koordinat Y pusat lingkaran: "))
        radius = float(input("Masukkan jari-jari lingkaran: "))
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
        return None
    if radius <= 0:
        print("Jari-jari harus lebih besar dari nol.")
        return None
    print(f"Lingkaran dengan pusat ({center_x}, {center_y}) dan jari-jari {radius} digambar.")
    return {"type": "circle", "center": (center_x, center_y), "radius": radius, "color": "purple", "facecolor": "violet"}

def draw_trapezoid(ax):
    try:
        x_start = float(input("Masukkan koordinat X pojok kiri bawah trapesium: "))
        y_start = float(input("Masukkan koordinat Y pojok kiri bawah trapesium: "))
        bottom_base = float(input("Masukkan panjang alas bawah trapesium: "))
        top_base = float(input("Masukkan panjang alas atas trapesium: "))
        height = float(input("Masukkan tinggi trapesium: "))
        offset_left = float(input("Masukkan offset horizontal kiri untuk alas atas: "))
        offset_right = float(input("Masukkan offset horizontal kanan untuk alas atas: "))
        if bottom_base <= 0 or top_base <= 0 or height <= 0:
            print("Panjang alas bawah, alas atas, dan tinggi harus lebih besar dari nol.")
            return None
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
        return None
    v1 = (x_start, y_start)
    v2 = (x_start + bottom_base, y_start)
    v3 = (x_start + offset_left, y_start + height)
    v4 = (x_start + offset_left + top_base, y_start + height)
    vertices = [v1, v2, v4, v3]
    print(f"Trapesium digambar dengan alas bawah {bottom_base}, alas atas {top_base}, tinggi {height},")
    print(f"dimulai dari ({x_start}, {y_start}), dengan offset kiri {offset_left} dan offset kanan {offset_right}.")
    return {"type": "polygon", "vertices": vertices, "color": "orange", "facecolor": "gold"}

# --- Utility: Plot shape on axes ---
def plot_shape_on_ax(ax, shape_data, clear_previous=True):
    global current_patch
    if clear_previous:
        for p in ax.patches:
            p.remove()
        for txt in ax.texts:
            txt.remove()
    patch = None
    shape_type = shape_data.get('type')
    edgecolor = shape_data.get('color', 'black')
    facecolor = shape_data.get('facecolor', 'lightgray')
    alpha = shape_data.get('alpha', 0.5)
    if shape_type == 'polygon':
        vertices = shape_data.get('vertices')
        if vertices:
            patch = plt.Polygon(vertices, closed=True, edgecolor=edgecolor, facecolor=facecolor, alpha=alpha)
    elif shape_type == 'circle':
        center = shape_data.get('center')
        radius = shape_data.get('radius')
        if center and radius is not None:
            patch = plt.Circle(center, radius, edgecolor=edgecolor, facecolor=facecolor, alpha=alpha)
    else:
        print(f"Error: Unknown shape type '{shape_type}'")
        return None
    if patch:
        ax.add_patch(patch)
        current_patch = patch
    return patch

# --- Transformasi ---
def apply_scaling(ax):
    global current_shape_data, current_patch
    if current_shape_data is None:
        print("Tidak ada bentuk yang digambar untuk ditransformasi. Harap gambar bentuk terlebih dahulu.")
        return
    try:
        sx = float(input("Masukkan faktor skala untuk sumbu X (sx): "))
        sy = float(input("Masukkan faktor skala untuk sumbu Y (sy): "))
        pivot_x = float(input("Masukkan koordinat X titik referensi/pusat penskalaan: "))
        pivot_y = float(input("Masukkan koordinat Y titik referensi/pusat penskalaan: "))
        if sx == 0 or sy == 0:
            print("Faktor skala tidak boleh nol.")
            return
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
        return
    new_shape_data = current_shape_data.copy()
    if new_shape_data['type'] == 'polygon':
        transformed_vertices = []
        for x, y in new_shape_data['vertices']:
            x_prime = x - pivot_x
            y_prime = y - pivot_y
            scaled_x_prime = x_prime * sx
            scaled_y_prime = y_prime * sy
            new_x = scaled_x_prime + pivot_x
            new_y = scaled_y_prime + pivot_y
            transformed_vertices.append((new_x, new_y))
        new_shape_data['vertices'] = transformed_vertices
    elif new_shape_data['type'] == 'circle':
        center_x, center_y = new_shape_data['center']
        radius = new_shape_data['radius']
        cx_prime = center_x - pivot_x
        cy_prime = center_y - pivot_y
        scaled_cx_prime = cx_prime * sx
        scaled_cy_prime = cy_prime * sy
        new_cx = scaled_cx_prime + pivot_x
        new_cy = scaled_cy_prime + pivot_y
        new_radius = radius * (abs(sx) + abs(sy)) / 2
        if new_radius <= 0:
            print("Radius setelah penskalaan menjadi nol atau negatif, tidak dapat digambar.")
            return
        new_shape_data['center'] = (new_cx, new_cy)
        new_shape_data['radius'] = new_radius
    else:
        print(f"Transformasi penskalaan tidak didukung untuk jenis bentuk: {new_shape_data['type']}")
        return
    current_shape_data = new_shape_data
    plot_shape_on_ax(ax, current_shape_data, clear_previous=True)
    print(f"Bentuk telah diskalakan dengan faktor sx={sx}, sy={sy} sekitar titik ({pivot_x}, {pivot_y}).")

def apply_reflection(ax):
    global current_shape_data, current_patch
    if current_shape_data is None:
        print("Tidak ada bentuk yang digambar untuk ditransformasi. Harap gambar bentuk terlebih dahulu.")
        return
    print("\nPilih sumbu cerminan:")
    print("1. Sumbu X")
    print("2. Sumbu Y")
    print("3. Titik Asal (Origin)")
    reflection_choice = input("Masukkan pilihan (1, 2, atau 3): ")
    new_shape_data = current_shape_data.copy()
    reflection_type_str = ""
    if new_shape_data['type'] == 'polygon':
        transformed_vertices = []
        for x, y in new_shape_data['vertices']:
            new_x, new_y = x, y
            if reflection_choice == '1':
                new_y = -y
                reflection_type_str = "sumbu X"
            elif reflection_choice == '2':
                new_x = -x
                reflection_type_str = "sumbu Y"
            elif reflection_choice == '3':
                new_x = -x
                new_y = -y
                reflection_type_str = "titik asal"
            else:
                print("Pilihan sumbu cerminan tidak valid.")
                return
            transformed_vertices.append((new_x, new_y))
        new_shape_data['vertices'] = transformed_vertices
    elif new_shape_data['type'] == 'circle':
        center_x, center_y = new_shape_data['center']
        new_cx, new_cy = center_x, center_y
        if reflection_choice == '1':
            new_cy = -center_y
            reflection_type_str = "sumbu X"
        elif reflection_choice == '2':
            new_cx = -center_x
            reflection_type_str = "sumbu Y"
        elif reflection_choice == '3':
            new_cx = -center_x
            new_cy = -center_y
            reflection_type_str = "titik asal"
        else:
            print("Pilihan sumbu cerminan tidak valid.")
            return
        new_shape_data['center'] = (new_cx, new_cy)
    else:
        print(f"Transformasi pencerminan tidak didukung untuk jenis bentuk: {new_shape_data['type']}")
        return
    current_shape_data = new_shape_data
    plot_shape_on_ax(ax, current_shape_data, clear_previous=True)
    print(f"Bentuk telah dicerminkan terhadap {reflection_type_str}.")

def apply_rotation(ax):
    global current_shape_data, current_patch
    if current_shape_data is None:
        print("Tidak ada bentuk yang digambar untuk ditransformasi. Harap gambar bentuk terlebih dahulu.")
        return
    try:
        angle_degrees = float(input("Masukkan sudut rotasi dalam derajat: "))
        pivot_x = float(input("Masukkan koordinat X titik referensi/pusat rotasi: "))
        pivot_y = float(input("Masukkan koordinat Y titik referensi/pusat rotasi: "))
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
        return
    angle_rad = math.radians(angle_degrees)
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)
    new_shape_data = current_shape_data.copy()
    if new_shape_data['type'] == 'polygon':
        transformed_vertices = []
        for x, y in new_shape_data['vertices']:
            x_prime = x - pivot_x
            y_prime = y - pivot_y
            new_x_prime = x_prime * cos_angle - y_prime * sin_angle
            new_y_prime = x_prime * sin_angle + y_prime * cos_angle
            new_x = new_x_prime + pivot_x
            new_y = new_y_prime + pivot_y
            transformed_vertices.append((new_x, new_y))
        new_shape_data['vertices'] = transformed_vertices
    elif new_shape_data['type'] == 'circle':
        center_x, center_y = new_shape_data['center']
        cx_prime = center_x - pivot_x
        cy_prime = center_y - pivot_y
        new_cx_prime = cx_prime * cos_angle - cy_prime * sin_angle
        new_cy_prime = cx_prime * sin_angle + cy_prime * cos_angle
        new_cx = new_cx_prime + pivot_x
        new_cy = new_cy_prime + pivot_y
        new_shape_data['center'] = (new_cx, new_cy)
    else:
        print(f"Transformasi rotasi tidak didukung untuk jenis bentuk: {new_shape_data['type']}")
        return
    current_shape_data = new_shape_data
    plot_shape_on_ax(ax, current_shape_data, clear_previous=True)
    print(f"Bentuk telah dirotasi {angle_degrees} derajat sekitar titik ({pivot_x}, {pivot_y}).")

# --- Main Loop ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.grid(True)
ax.set_aspect('equal')
plt.title('Interactive Drawing and Transformation Application')
plt.ion()
plt.show()

while True:
    print("\n--- Menu Menggambar & Transformasi Bentuk ---")
    print("1. Menggambar Bujursangkar (Square)")
    print("2. Menggambar Segitiga (Triangle)")
    print("3. Menggambar Persegi Panjang (Rectangle)")
    print("4. Menggambar Lingkaran (Circle)")
    print("5. Menggambar Trapesium (Trapezoid)")
    print("---")
    print("6. Terapkan Penskalaan (Scale)")
    print("7. Terapkan Pencerminan (Reflect)")
    print("8. Terapkan Rotasi (Rotate)")
    print("---")
    print("9. Hapus Semua Bentuk (Clear All Shapes)")
    print("10. Keluar (Exit)")
    choice = input("Pilih opsi (1-10): ")
    shape_data = None
    if choice == '1':
        shape_data = draw_square(ax)
    elif choice == '2':
        shape_data = draw_triangle(ax)
    elif choice == '3':
        shape_data = draw_rectangle(ax)
    elif choice == '4':
        shape_data = draw_circle(ax)
    elif choice == '5':
        shape_data = draw_trapezoid(ax)
    elif choice == '6':
        apply_scaling(ax)
    elif choice == '7':
        apply_reflection(ax)
    elif choice == '8':
        apply_rotation(ax)
    elif choice == '9':
        for p in ax.patches:
            p.remove()
        for txt in ax.texts:
            txt.remove()
        current_shape_data = None
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_aspect('equal')
        ax.grid(True)
        plt.title('Interactive Drawing and Transformation Application')
        print("Semua bentuk telah dihapus.")
    elif choice == '10':
        print("Keluar dari aplikasi. Sampai jumpa!")
        break
    else:
        print("Pilihan tidak valid. Harap masukkan angka antara 1 dan 10.")
    if choice in ['1', '2', '3', '4', '5'] and shape_data is not None:
        current_shape_data = shape_data
        plot_shape_on_ax(ax, current_shape_data, clear_previous=True)
    plt.draw()
    plt.pause(0.1)

plt.close(fig)
print("Aplikasi gambar telah ditutup.")
