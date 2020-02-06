def calculate_min_power(input_velocity, data):
    km = 1.36
    velocity = input_velocity * 10 / 36
    coefficient_of_friction = 0.016
    density_of_air = 1.2
    g = 9.81
    min_power = ((0.5 * density_of_air * velocity * velocity * data['area'] * data['coefficient']) +
                 (coefficient_of_friction * data['mass'] * g)) * velocity / 1000
    min_power *= km
    return min_power


def calculate_rest_power(min_power, data, target_velocity, input_velocity):
    in_velocity = input_velocity * 10 / 36
    tar_velocity = target_velocity * 10 / 36
    if tar_velocity < in_velocity:
        return -data['power'] * 2 / 3
    return data['power'] - min_power


def calculate_acceleration(power, input_velocity, data):
    kW = 1 / 1.36
    velocity = input_velocity * 10 / 36
    if power < 0:
        accelerate = (-power * kW * 1000) / (velocity * data['mass'])
    else:
        accelerate = (power * kW * 1000) / (velocity * data['mass'])
    return accelerate


def calculate_new_velocity(input_velocity, accelerate, target_velocity):
    current_velocity = input_velocity * 10 / 36
    a = accelerate / 100
    if target_velocity * 10 / 36 < current_velocity:
        return (current_velocity - a) * 36 / 10

    if a + current_velocity >= target_velocity * 10 / 36:
        return target_velocity
    else:
        return (a + current_velocity) * 36 / 10


def make_data(n, duration, velocity_start, target_velocity, input_data, graph_data):
    if n == 0:
        min_power = calculate_min_power(velocity_start, input_data)
        graph_data = dict(
            x=[x / 100 for x in range(0, duration * 100)],
            y_range=[0, velocity_start * 1.3],
            power=[min_power / input_data['power']],
            velocity=[velocity_start],
        )

    elif n < 100 * duration:
        min_power = calculate_min_power(graph_data['velocity'][-1], input_data)
        rest_power = calculate_rest_power(min_power, input_data, target_velocity, graph_data['velocity'][-1])
        acceleration = calculate_acceleration(rest_power, graph_data['velocity'][-1], input_data)
        new_velocity = calculate_new_velocity(graph_data['velocity'][-1], acceleration, target_velocity)
        graph_data['power'].append(min_power / input_data['power'])
        graph_data['velocity'].append(new_velocity)
    else:
        min_power = calculate_min_power(graph_data['velocity'][-1], input_data)
        rest_power = calculate_rest_power(min_power, input_data, target_velocity, graph_data['velocity'][-1])
        acceleration = calculate_acceleration(rest_power, graph_data['velocity'][-1], input_data)
        new_velocity = calculate_new_velocity(graph_data['velocity'][-1], acceleration, target_velocity)
        graph_data['x'].pop(0)
        graph_data['power'].pop(0)
        graph_data['velocity'].pop(0)
        graph_data['x'].append(n / 100)
        graph_data['power'].append(min_power / input_data['power'])
        graph_data['velocity'].append(new_velocity)
    graph_data['x_range'] = [graph_data['x'][0], graph_data['x'][-1]]
    graph_data['y_range'][1] = max(graph_data['velocity']) * 1.3
    return graph_data
