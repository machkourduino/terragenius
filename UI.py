import pygame
import sys
import math
import os
from buttons import Button
from seeds import Seed
import tkinter as tk
from database import plant_database
from options import Option
import subprocess


pygame.init()
sizing_square = (500, 500)

scale = 2

DBL = (26, 43, 60)
SDBL = (3, 68, 83)
BL = (39, 135, 124)
LBL = (67, 150, 145)
W = (251, 251, 210)
P = (228, 193, 153)
LBR = (191, 147, 74)
BR = (111, 87, 77)
DBR = (11, 6, 2)
DO = (162, 72, 23)
O = (253, 120, 43)

R = (255, 50, 54)

x = 0
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
screen = pygame.display.set_mode([1367, 580])

a = 500
b = 500

hypotenuse = 360
angle = 46
seed_radius = 20

stored_seed_positions = []
direction_interval = -1
interval = -0.46
index = 0
mode = 0
calc_bool = False
current_angle = 0

#images
hlock = pygame.image.load("buttons/hlock.png")
lock = pygame.image.load("buttons/lock.png")
hunlock = pygame.image.load("buttons/hunlock.png")
unlock = pygame.image.load("buttons/unlock.png")

hshow = pygame.image.load("buttons/hshow.png")
show = pygame.image.load("buttons/show.png")
hhide = pygame.image.load("buttons/hhide.png")
hide = pygame.image.load("buttons/hide.png")

hchoose = pygame.image.load("buttons/hchoose.png")
choose = pygame.image.load("buttons/choose.png")
hchose = pygame.image.load("buttons/hchose.png")
chose = pygame.image.load("buttons/chose.png")

hupload = pygame.image.load("buttons/hupload.png")
upload = pygame.image.load("buttons/upload.png")

close = pygame.image.load("buttons/x_button.png")
hclose = pygame.image.load("buttons/hx_button.png")

hoption = pygame.image.load("buttons/hoption.png")
option = pygame.image.load("buttons/option.png")

good = pygame.image.load("buttons/good.png")
good = pygame.transform.scale(good, (60,60))
bad = pygame.image.load("buttons/bad.png")
bad = pygame.transform.scale(bad, (60,60))
amazing = pygame.image.load("buttons/amazing.png")
amazing = pygame.transform.scale(amazing, (60,60))
horrible = pygame.image.load("buttons/horrible.png")
horrible = pygame.transform.scale(horrible, (60,60))
neutral = pygame.image.load("buttons/neutral.png")
neutral = pygame.transform.scale(neutral, (60,60))

plant = pygame.image.load("buttons/plant.png")
plant = pygame.transform.scale(plant, (153, 60))
hplant = pygame.image.load("buttons/hplant.png")
hplant = pygame.transform.scale(hplant, (153, 60))

send = pygame.image.load("buttons/send.png")
send = pygame.transform.scale(send, (192, 71))
hsend = pygame.image.load("buttons/hsend.png")
hsend = pygame.transform.scale(hsend, (192, 71))


def send_directions(directions):
    sketch_path = r"C:\Users\Yasser\Documents\Arduino\sketch_nov13b\sketch_nov13b.ino"

    new_input_string = str(calculate_directions(directions))
    print(new_input_string)

    with open(sketch_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if "const char* inputString" in line:
            lines[i] = f'const char* inputString = "{new_input_string}";\n'

    with open(sketch_path, 'w') as file:
        file.writelines(lines)

    print("sketch updated with new input string.")

    board = "arduino:avr:mega"
    port = "COM14"

    compile_command = [
        "C:\\Users\\Yasser\\arduino-cli.exe", "compile",
        "--fqbn", board,
        "C:\\Users\\Yasser\\Documents\\Arduino\\sketch_nov13b"
    ]

    upload_command = [
        "C:\\Users\\Yasser\\arduino-cli.exe", "upload",
        "--fqbn", board,
        "--port", port,
        "C:\\Users\\Yasser\\Documents\\Arduino\\sketch_nov13b"
    ]

    subprocess.run(compile_command, check=True)
    subprocess.run(upload_command, check=True)
    print("sketch uploaded to arduino!! :D")
def calculate_directions(directions):
    string = ""
    points = [(50, 50)] + directions
    last_angle = 45
    flip = -1 #if you want to flip, make this -1
    string_list = []
    string += "a" + str(-470*flip)
    string_list.append(-470*flip)
    for i in range(len(points)-1):
        if points[i][0] == points[i+1][0]:
            if points[i][1] > points[i+1][1]:
                angle = 180
            else:
                angle = 0
        elif points[i][1] == points[i+1][1]:
            angle = 90
        else:
            if points[i][1] > points[i+1][1]:
                angle = math.atan(abs(points[i][1]-points[i+1][1])/abs(points[i][0]-points[i+1][0])) * (180/3.14159) + 90
            else:
                angle = math.atan(abs(points[i][1]-points[i+1][1])/abs(points[i][0]-points[i+1][0])) * (180/3.14159)
        turn_angle = last_angle - angle
        #93 = 90+2+1
        #47 = 45+1+1
        if i != 0:
            if int(turn_angle) != 0:
                if turn_angle < 0:
                    extra_turn = -10
                else:
                    extra_turn = 10
                string += "a" + str(flip*int(extra_turn+(turn_angle*10)+(turn_angle*10*(2/90))))
                string_list.append(flip*int(extra_turn+(turn_angle*10)+(turn_angle*10*(2/90))))
        string += "f" + str(int((math.sqrt((abs(points[i][0]-points[i+1][0]))**2 + (abs(points[i][1]-points[i+1][1]))**2)/(87.5/30))*1000))
        string_list.append(int((math.sqrt((abs(points[i][0]-points[i+1][0]))**2 + (abs(points[i][1]-points[i+1][1]))**2)/(87.5/30))*1000))
        string += "w" + str(int(plant_database[int(water_req_list[i])][4]*10))
        last_angle = angle
    #string list is so that the retracking movement is the same
    string_list.reverse()
    for i in range(len(string_list)):
        if i%2 == 0:
            string += "b" + str(string_list[i])
        else:
            string += "a" + str(-string_list[i])

    return string
def path(step):
    global interval, calc_bool

    interval += 0.1

    for i in range(len(step) - 1):
        if int(interval) == i:
            pygame.draw.lines(screen, R, False, [step[i], step[i + 1]], 5)

        else:
            pygame.draw.lines(screen, P, False, [step[i], step[i + 1]], 1)

    pygame.draw.lines(screen, P, False, [(50, 50), step[0]], 1)
def zigzag_positions(cols, rows, data, special_case):
    zigzag_positions = []

    s = 0
    cols = int(cols)
    rows = int(rows)

    for i in range(int(cols)):
        if i % 2 == 0:
            for j in range(0, int(rows), 1):
                index = i * int(rows) + j
                if index < len(data):
                    zigzag_positions.append(data[index])
        else:
            for j in range(int(rows) - 1, -1, -1):
                index = i * int(rows) + j
                if index < len(stored_seed_positions):
                    zigzag_positions.append(stored_seed_positions[index])

    for i in range(cols):
        if i % 2 != 0:
            right = s + (rows - 2)
            while s < right and right < len(data):
                data[s], data[right] = data[right], \
                                       data[s]
                s += 1
                right -= 1
            s += (rows - 1) // 2 if (rows - 1) % 2 == 0 else (rows - 1) // 2 + 1

        else:
            s += rows

    if special_case == True:
        return data
    else:
        return zigzag_positions
def display_seeds(organization, vertical_space, horizantal_space, radius):
    global step_directions
    if organization == 0:
        x_diff = side_b - (horizantal_space * (radius * 0.99) * 2)
        x_shift = 0

        y_diff = side_a - (vertical_space * (radius * 0.99) * 2)
        horizantal_shift = 0
        stored_seed_positions.clear()
        for col in range(horizantal_space):
            vertical_shift = 0
            y_shift = 0
            for row in range(vertical_space):
                stored_seed_positions.append(
                    (int(50 + radius + horizantal_shift + x_shift), int(50 + radius + vertical_shift + y_shift)))
                pygame.draw.circle(screen, (50, 50, 50),
                                   (50 + radius + horizantal_shift + x_shift, 50 + radius + vertical_shift + y_shift),
                                   seed_radius, 1)
                pygame.draw.circle(screen, (0, 255, 0),
                                   (50 + radius + horizantal_shift + x_shift, 50 + radius + vertical_shift + y_shift),
                                   5, 0)
                vertical_shift += 2 * (radius * 0.99)
                y_shift += y_diff / vertical_space
            horizantal_shift += 2 * (0.99 * radius)
            x_shift += x_diff / horizantal_space
        try:
            step_directions = zigzag_positions(aligned(seed_radius, side_b, side_a)[1], aligned(seed_radius, side_b, side_a)[0],
                                 stored_seed_positions, False)
            path(step_directions)

        except:
            ValueError, IndexError


    elif organization == 1:
        x_diff = side_b - (int(horizantal_space) * (radius*2 - (radius - (math.sqrt((radius**2) - ((radius**2)/3))))))
        x_shift = 0

        horizantal_shift = 0
        stored_seed_positions.clear()
        special_case = False

        for col in range(int(horizantal_space)):

            vertical_shift = 0
            if col % 2 == 1:
                y_shift = radius
                if (vertical_space * radius * 2) + radius < side_a:
                    special_case = False
                    y_diff = 0
                else:
                    special_case = True
                    y_diff = 1
            else:

                y_shift = 0
                y_diff = 0

            for row in range(vertical_space - y_diff):
                stored_seed_positions.append(
                    (int(50 + radius + horizantal_shift + x_shift), int(50 + radius + vertical_shift + y_shift)))
                pygame.draw.circle(screen, (50, 50, 50),
                                   (50 + radius + horizantal_shift + x_shift, 50 + radius + vertical_shift + y_shift),
                                   seed_radius, 1)
                pygame.draw.circle(screen, (57, 255, 57),
                                   (50 + radius + horizantal_shift + x_shift, 50 + radius + vertical_shift + y_shift),
                                   5, 0)

                vertical_shift += 2 * radius
            horizantal_shift += radius*math.sqrt(3)

            x_shift += (side_b-((horizantal_space*radius*math.sqrt(3)) + (2*radius - radius*math.sqrt(3))))/horizantal_space
        try:
            step_directions = zigzag_positions(packed(seed_radius, side_b, side_a)[1], packed(seed_radius, side_b, side_a)[0],
                                  stored_seed_positions, special_case)
            path(step_directions)

        except:
            ValueError, IndexError
def aligned(radius, x, y):
    # x = side_b
    # y = side_a
    vertical_space = int(y / (2 * radius))
    horizantal_space = int(x / (2 * radius))
    return vertical_space, horizantal_space
def packed(radius, x, y):
    horizantal_space = -1
    index = 0
    while x > index*radius*math.sqrt(3) + (2*radius - radius*math.sqrt(3)):
        horizantal_space += 1
        index += 1


    vertical_space = int(y / (2 * radius))

    if math.floor((y/(2*radius))+0.5) == math.floor(y/(2*radius)):
        add_circle = -int(horizantal_space/2)
    else:
        add_circle = 0
    space_count = (vertical_space*horizantal_space + add_circle)



    return vertical_space, horizantal_space
def organization(p_vertical_space, p_horizantal_space, a_vertical_space, a_horizantal_space, radius):
    align_num = 0
    pack_num = 0

    for col in range(a_horizantal_space):
        for row in range(a_vertical_space):
            align_num += 1

    for col in range(int(p_horizantal_space * math.sqrt(3) / 1.5)):
        if col % 2 == 1:
            if (p_vertical_space * radius * 2) + radius < side_a:
                y_diff = 0
            else:
                y_diff = 1
        else:
            y_shift = 0
            y_diff = 0
        for row in range(p_vertical_space - y_diff):
            pack_num += 1

    if align_num > pack_num:
        organization = 0
        # print(align_num, pack_num, "ALIGNED")
    elif align_num < pack_num:
        organization = 1
        # print(align_num, pack_num, "HEXAGONAL")
    else:
        organization = 1
        # print(align_num, pack_num, "EQUAL")

    return organization
def display_hypotenuse(side_b, side_a):
    w = 1
    pygame.draw.line(screen, O, (50, 50), (side_b + 50, side_a + 50), 1)  # hypotenuse
def field(side_b, side_a):
    w = 1
    pygame.draw.line(screen, LBL, (50, 50), (side_b + 50, 50), w)  # side_b top
    pygame.draw.line(screen, LBL, (50, side_a + 50), (side_b + 50, side_a + 50), w)  # side_b bottom
    pygame.draw.line(screen, SDBL, (side_b + 50, side_a + 50), (side_b + 50, 50), w)  # side_a right

    pygame.draw.line(screen, (255, 255, 255), (side_b + 50, 50), (side_b + 30, 50), w)  # corner top right
    pygame.draw.line(screen, (255, 255, 255), (side_b + 50, 50), (side_b + 50, 70), w)  # corner top right

    pygame.draw.circle(screen, (255, 255, 255), (side_b + 50, side_a + 50), 10)  # Navigator 2

    pygame.draw.line(screen, SDBL, (50, 50), (50, side_a + 50), w)  # side_a left
    pygame.draw.circle(screen, (255, 255, 255), (50, 50), 10)  # navigator 1

    pygame.draw.line(screen, (255, 255, 255), (50, side_a + 50), (70, side_a + 50), w)  # corner bot left
    pygame.draw.line(screen, (255, 255, 255), (50, side_a + 50), (50, side_a + 30), w)  # corner bot left
def text(side_a, side_b, hypo, angle, radius):
    font = pygame.font.SysFont('coriernew', 25, False, False)

    side_a_text = font.render("Side_A: " + str(round(side_a, 1)) + " cm", True, SDBL)
    side_a_rect = side_a_text.get_rect(center=(1250, 50))

    side_b_text = font.render("Side_B: " + str(round(side_b, 1)) + " cm", True, LBL)
    side_b_rect = side_b_text.get_rect(center=(1250, 100))

    hypo_text = font.render("Distance: " + str(round(hypo, 1)) + " cm", True, O)
    hypo_rect = hypo_text.get_rect(center=(1250, 150))

    angle_text = font.render("Angle: " + str(round(angle, 1)) + " degrees", True, (255, 255, 255))
    angle_rect = angle_text.get_rect(center=(1250, 200))

    radius_text = font.render("Seed radius: " + str(round(radius, 1)) + " cm", True, (255, 255, 255))
    radius_rect = angle_text.get_rect(center=(1250, 250))

    screen.blit(side_a_text, side_a_rect)
    screen.blit(side_b_text, side_b_rect)
    screen.blit(hypo_text, hypo_rect)
    screen.blit(angle_text, angle_rect)
    screen.blit(radius_text, radius_rect)

indexs = 0

def get_input():
    def submit():
        nonlocal angle, distance, seed_radius
        angle = float(angle_entry.get() or 46)
        distance = float(distance_entry.get() or 260)
        seed_radius = float(seed_radius_entry.get() or 50)
        root.destroy()

    def on_close():
        nonlocal angle, distance, seed_radius

        root.destroy()

    angle = 46
    distance = 360
    seed_radius = 20

    root = tk.Tk()
    root.title("Input Data")
    root.protocol("WM_DELETE_WINDOW", on_close)

    padding = {'padx': 10, 'pady': 10}
    tk.Label(root, text="Enter Angle:").grid(row=0, column=0, **padding)
    angle_entry = tk.Entry(root)
    angle_entry.grid(row=0, column=1, **padding)

    tk.Label(root, text="Enter Distance:").grid(row=1, column=0, **padding)
    distance_entry = tk.Entry(root)
    distance_entry.grid(row=1, column=1, **padding)

    tk.Label(root, text="Enter Seed Radius:").grid(row=2, column=0, **padding)
    seed_radius_entry = tk.Entry(root)
    seed_radius_entry.grid(row=2, column=1, **padding)

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=3, columnspan=2, pady=10)  # Span across two columns

    # Center the window on the screen
    root.update_idletasks()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    root.mainloop()
    return angle, distance, seed_radius

lock_button = Button(922, 49, lock, hlock, unlock, hunlock, (185, 68))
info_button = Button(1206, 278, show, hshow, hide, hhide, (97, 36))
choose_button = Option(909, 146, chose, hchose, choose, hchoose, (215, 203))
upload_button = Button(1220, 332, upload, hupload, scale=(70, 70))
x_button = Button(1276, 35, close, hclose, scale=(47, 47))
plant_button = Button(1056, 29, plant, hplant, scale=(153, 60))
send_button = Button(28, 471, send, hsend, scale=(192, 71))



buttons_list = []
buttons_list.append(lock_button)
buttons_list.append(info_button)

buttons_list.append(upload_button)
buttons_list.append(send_button)
all_buttons = pygame.sprite.Group()
all_buttons.add(buttons_list)

chose_list = []
chose_sprite = pygame.sprite.Group()
chose_list.append(choose_button)
chose_sprite.add(chose_list)


plant_sprite = pygame.sprite.Group()


x_sprites = pygame.sprite.Group()
x_list = []

seed_list = []
seed_sprites = pygame.sprite.Group()

selected_options = []



list_of_plants = ["Carrot", "Onion", "Radish", "Potato", "Tomato", "Basil", "Lettuce", "Bell pepper", "Cucumber", "Dill", "Spinach", "Marigold", "Cabbage", "Eggplant", "Beet", "Broccoli", "Garlic"]

def check_selections(menu_on):
    check = 0
    saved_seed = []
    if menu_on == True:
        for i in range(len(seed_sprites)):
            if seed_sprites.sprites()[i].toggle() == False:
                check += 1
                saved_seed.append(i)
    else:
        check = 0
        saved_seed = []

    return check, saved_seed
def get_compatible_indexes(plant):
    compatible = []
    incompatible = []

    for i in plant_database[plant][1]:
        compatible.append(list_of_plants.index(i))

    for i in plant_database[plant][2]:
        incompatible.append(list_of_plants.index(i))


    return compatible, incompatible
def draw_compatibility(plants, scroll):
    positions = []
    for x in range(len(plants)):
        if len(plants) > 0 and len(plants) < 3:
            if get_compatible_indexes(plants[x])[0]:
                for m in get_compatible_indexes(plants[x])[0]:
                    index = 0
                    for i in range(10):
                        for j in range(4):
                            if index < len(list_of_plants):
                                if index == m:
                                    #add position to list
                                    positions.append((j, i, True))
                                    if positions.count((j, i, True)) == 2:
                                        screen.blit(amazing, (89 + (325 * j), 115 + (100 * i) + scroll))
                                    elif positions.count((j, i, False)) == 1 and positions.count((j, i, True)) == 1:
                                        screen.blit(neutral, (89 + (325 * j), 115 + (100 * i) + scroll))
                                    else:
                                        screen.blit(good, (89 + (325 * j), 115 + (100 * i) + scroll))
                                #seed_list.append(Seed(True, list_of_plants[index], 82 + (325*j), 109 + (100*i), option, hoption, (217, 74)))
                                index += 1
            if get_compatible_indexes(plants[x])[1]:
                for m in get_compatible_indexes(plants[x])[1]:
                    index = 0
                    for i in range(10):
                        for j in range(4):
                            if index < len(list_of_plants):
                                if index == m:
                                    positions.append((j, i, False))
                                    if positions.count((j, i, False)) == 2:
                                        screen.blit(horrible, (89 + (325*j), 115 + (100*i) + scroll))
                                    elif positions.count((j, i, False)) == 1 and positions.count((j, i, True)) == 1:
                                        screen.blit(neutral, (89 + (325 * j), 115 + (100 * i) + scroll))
                                    else:
                                        screen.blit(bad, (89 + (325 * j), 115 + (100 * i) + scroll))
                                #seed_list.append(Seed(True, list_of_plants[index], 82 + (325*j), 109 + (100*i), option, hoption, (217, 74)))
                                index += 1

size = 1
test_img = send
fix_delay = 0
beep = 0
angle = 46
distance = 360
seed_radius = 53
menu = pygame.image.load('buttons/menu.png')
menu = pygame.transform.scale(menu, (1347, 570))
menu_rect = pygame.Rect([0, 0, 1347, 100])
menu_surface = pygame.Surface(menu_rect.size)
menu_surface.blit(menu, (0, 0), menu_rect)

menu_on = False
scroll = 0
scroll_pos = 0
rows = 0
filled = False

final_seeds = []
print_seed_list = []
diff_stored_seed_positions = []
trans = 0
upload_count = 0
water_req_list = []
water_index = 0


def reverse_every_other_group(stored_seed_positions):
    from itertools import groupby

    grouped_positions = {x: list(group) for x, group in groupby(stored_seed_positions, key=lambda pos: pos[0])}

    keys = list(grouped_positions.keys())

    for i in range(1, len(keys), 2):  # start from the second group
        grouped_positions[keys[i]].reverse()

    result = [pos for key in keys for pos in grouped_positions[key]]
    return result

def draw_text(text, position, font_size=30, color=(255, 255, 255)):
    font = pygame.font.SysFont('Arial', font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

while True:
    for event in pygame.event.get():
        x_button.check_click(event)
        if len(seed_sprites) > 0:
            if check_selections(menu_on)[0] == 3:
                plant_button.check_click(event)
            for i in range(len(seed_list)):
                if i in check_selections(menu_on)[1]:
                    seed_sprites.sprites()[i].check_click(event) #checks if plant already clicked
                else:
                    if check_selections(menu_on)[0] < 3:
                        seed_sprites.sprites()[i].check_click(event)



        if menu_on == False:
            scroll = 0
            info_button.check_click(event)
            lock_button.check_click(event)
            if filled == True:
                send_button.check_click(event)


                #

            if all_buttons.sprites()[0].toggle() == False:
                upload_button.check_click(event)
                filled = False
                #clear plant data
            else:
                choose_button.check_click(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 4:  # scroll up
                size += 0.01

            elif event.button == 5:  # scroll down
                size = max(0.01, size - 0.01)


    side_a = hypotenuse * math.cos(math.radians(angle))
    side_b = hypotenuse * math.sin(math.radians(angle))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.quit()

    if keys[pygame.K_t]:
        trans = 1
    elif keys[pygame.K_g]:
        trans = 0

    if all_buttons.sprites()[0].toggle() == False:
        if keys[pygame.K_RIGHT]:
            angle += 0.1
        elif keys[pygame.K_LEFT]:
            angle -= 0.1

        if keys[pygame.K_a]:
            seed_radius += 0.05
        elif keys[pygame.K_s]:
            seed_radius -= 0.05

        if keys[pygame.K_UP]:
            hypotenuse += 1

        elif keys[pygame.K_DOWN]:
            hypotenuse -= 1


    screen.fill(DBR)
    display_hypotenuse(side_b, side_a)

    if all_buttons.sprites()[2].is_clicked() == True:
        angle, hypotenuse, seed_radius = get_input()







    text(side_a, side_b, hypotenuse, angle, int(seed_radius))
    if organization(packed(seed_radius, side_b, side_a)[0], packed(seed_radius, side_b, side_a)[1],
                    aligned(seed_radius, side_b, side_a)[0], aligned(seed_radius, side_b, side_a)[1], seed_radius) == 0:
        display_seeds(0, aligned(seed_radius, side_b, side_a)[0], aligned(seed_radius, side_b, side_a)[1], seed_radius)

    if organization(packed(seed_radius, side_b, side_a)[0], packed(seed_radius, side_b, side_a)[1],
                    aligned(seed_radius, side_b, side_a)[0], aligned(seed_radius, side_b, side_a)[1], seed_radius) == 1:
        display_seeds(1, packed(seed_radius, side_b, side_a)[0], packed(seed_radius, side_b, side_a)[1], seed_radius)
    field(side_b, side_a)




    if all_buttons.sprites()[1].toggle() == True:
        pygame.draw.rect(screen, DBR, [1159, 36, 180, 230])

    all_buttons.update()
    all_buttons.draw(screen)
    chose_sprite.update(filled)
    chose_sprite.draw(screen)
    if filled == False:
        pygame.draw.rect(screen, DBR, [28, 471, 192, 71])


    if chose_sprite.sprites()[0].is_clicked() == True:
        menu_on = True
        x_list.append(x_button)
        x_sprites.add(x_list)
        plant_sprite.add(plant_button)
        if plant_sprite.sprites()[0].is_clicked() == True:
            filled = True
            if check_selections(menu_on)[0] == 3:
                final_seeds.append(check_selections(menu_on)[1])
                diff_stored_seed_positions = step_directions
        if x_sprites.sprites()[0].is_clicked() == False and plant_sprite.sprites()[0].is_clicked() == False:


            if menu_on == True:
                screen.blit(menu, (10, 0))
        else:
            menu_on = False
            x_sprites.empty()
            plant_sprite.empty()
            #dont change plants



    if menu_on == True:
        if keys[pygame.K_DOWN] and scroll_pos > -(100*(rows-3)):
            scroll = -10
        elif keys[pygame.K_UP] and scroll_pos < 0:
            scroll = 10
        else:
            scroll = 0
        scroll_pos += scroll
        #show all options
        #allow for picking options
        index = 0
        if len(seed_sprites) < 1:
            for i in range(10):
                for j in range(4):
                    if index < len(list_of_plants):
                        seed_list.append(Seed(True, list_of_plants[index], 82 + (325*j), 109 + (100*i), option, hoption, (217, 74)))
                        index += 1
                        rows = i
            seed_sprites.add(seed_list)
    else:
        seed_sprites.empty()
        seed_list.clear()
        #you need to print out the toggling of each sprite, since it is not resetting to True


    seed_sprites.update(scroll)
    seed_sprites.draw(screen)




    if len(seed_sprites) > 0:
        draw_compatibility(check_selections(menu_on)[1], scroll_pos)

    new_size = (int(test_img.get_width() * size), int(test_img.get_height() * size))
    scaled_image = pygame.transform.scale(test_img, new_size)


    if menu_on == True:
        pygame.draw.rect(screen, (62, 69, 93), [80, 500, 1200, 70])

        pygame.draw.rect(screen, (0,0,0), [80, 570, 1200, 10])
        screen.blit(menu_surface, (10, 0))


    # Center the image on the screen
    mouse_pos = pygame.mouse.get_pos()
    x_sprites.update()
    x_sprites.draw(screen)
    plant_sprite.update()
    plant_sprite.draw(screen)



    font = pygame.font.SysFont('coriernew', int(seed_radius), False, False)

    if len(final_seeds) == 1:
        alpha = 0
        indexs = 0

        for i in range(len(diff_stored_seed_positions)):
            print(len(diff_stored_seed_positions))
            water_index += 1
            if indexs > 2:
                indexs = 0

            seed_text = font.render(str(list_of_plants[final_seeds[0][indexs]]), True, (255, 255, 255)).convert_alpha()
            if water_index < 5:
                water_req_list.append(final_seeds[0][indexs])
            text_x = diff_stored_seed_positions[i][0]
            text_y = diff_stored_seed_positions[i][1] + (seed_radius / 3)
            distance = math.sqrt((mouse_pos[0] - text_x) ** 2 + (mouse_pos[1] - text_y) ** 2)
            if trans == 0:
                alpha = 255-((distance/0.6)-255)
            else:
                alpha = 255
            seed_rect = seed_text.get_rect(center=(text_x, text_y))

            seed_text.set_alpha(alpha)
            indexs += 1
            screen.blit(seed_text, seed_rect)
        print(water_req_list)

    if menu_on == False:
        if filled == True:
            if all_buttons.sprites()[3].toggle() == True:
                if upload_count < 5:
                    draw_text("Uploading...", (250, 490))
                if upload_count == 5:
                    send_directions(step_directions)
                if upload_count > 5 and upload_count < 1000:
                    draw_text("Done Uploading!", (250, 490))
                upload_count += 1
    # screen.blit(scaled_image, mouse_pos)
    #
    # print(new_size, mouse_pos)
    pygame.display.update()
