import math
import time

theta_spacing = 0.07
phi_spacing = 0.02

R1 = 1
R2 = 2
K2 = 5
screen_width = 80
screen_height = 40
K1 = screen_width * K2 * 3 / (8 * (R1 + R2))

def render_frame(A, B):
    """
    Renders a frame of the spinning 3D torus.
    """
    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)

    output = [[' ' for _ in range(screen_width)] for _ in range(screen_height)]
    zbuffer = [[0 for _ in range(screen_width)] for _ in range(screen_height)]

    for theta in [i * theta_spacing for i in range(int(2 * math.pi / theta_spacing))]:
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        for phi in [i * phi_spacing for i in range(int(2 * math.pi / phi_spacing))]:
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z

            xp = int(screen_width / 2 + K1 * ooz * x)
            yp = int(screen_height / 2 - K1 * ooz * y)
            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)
            
            if 0 <= xp < screen_width and 0 <= yp < screen_height:
                if L > 0:
                    if ooz > zbuffer[yp][xp]:
                        zbuffer[yp][xp] = ooz
                        luminance_index = int(L * 8)
                        chars = ".,-~:;=!*#$@"
                        output[yp][xp] = chars[luminance_index]

    # Print the output
    print("\x1b[H", end='')
    for row in output:
        print(''.join(row))

A = 0
B = 0
while True:
    render_frame(A, B)
    A += 0.07
    B += 0.03
    time.sleep(0.03)
