import math

def calculate_directions(coordinates):
    coordinates = [(50, 50)] + coordinates
    directions = []
    current_position = coordinates[0]
    current_orientation = 90  # Starting orientation: down

    for next_position in coordinates[1:]:
        dx = next_position[0] - current_position[0]
        dy = next_position[1] - current_position[1]

        distance = math.sqrt(dx ** 2 + dy ** 2)
        angle = math.degrees(math.atan2(dy, dx))

        # Calculate angle difference between current orientation and required orientation
        angle_diff = angle - current_orientation
        angle_diff = (angle_diff + 180) % 360 - 180  # Normalize angle to -180 to 180 degrees

        # Determine the direction (left or right) and angle to turn
        if angle_diff > 0:
            turn_direction = "l"
            turn_angle = angle_diff
        else:
            turn_direction = "r"
            turn_angle = -angle_diff

        # Add turn action to directions
        directions.append([turn_direction, turn_angle])

        # Add forward action to directions
        directions.append(["f", distance/10])

        # Update current position and orientation
        current_position = next_position
        current_orientation = angle

    reversed_list = [[item[0], -item[1]] for item in reversed(directions)]

    # Step 3: Append the reversed version to the original list
    directions.extend(reversed_list)

    new_list = []
    for item in directions:
        new_list.append(item)
        if item[0] == 'f':
            new_list.append(['s', 10])

    opposite_angle = {'r': 'l', 'l': 'r'}

    for i in range(len(new_list) - 1):
        if new_list[i][0] in opposite_angle and new_list[i + 1][1] < 0:
            new_list[i][0] = opposite_angle[new_list[i][0]]
            new_list[i][1] = abs(new_list[i][1])



    new_list[-1] = ['l', 45.0]

    for i in range(1, len(new_list) - 1):
        if new_list[i][0] == 'f' and new_list[i][1] < 0:
            new_list[i][0] = 'b'  # Replace 'f' with 'b'
            new_list[i][1] = abs(new_list[i][1])  # Make the next value positive

    filtered_commands = [cmd for cmd in new_list if cmd != ['r', -0.0]]



    return filtered_commands

# Example usage
coordinates = [(70, 70), (70, 110), (70, 150), (105, 170), (105, 130), (105, 90), (140, 70), (140, 110), (140, 150), (175, 170), (175, 130), (175, 90), (210, 70), (210, 110), (210, 150), (245, 170), (245, 130), (245, 90), (280, 70), (280, 110), (280, 150), (315, 170), (315, 130), (315, 90)]


commands = calculate_directions(coordinates)
print(commands)