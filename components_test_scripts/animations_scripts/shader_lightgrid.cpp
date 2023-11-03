#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <vector>
#include <random>
#include <algorithm>

const int GRID_SIZE = 16;
const int WINDOW_SIZE = 64;
const float SQUARE_SIZE = 2.0f / GRID_SIZE;
const int MAX_SQUARES = GRID_SIZE * GRID_SIZE;
const int MIN_EMPTY_SQUARES = MAX_SQUARES / 5; // 20% of the pixels

struct Square {
    float x, y;
    float r, g, b;
    float alpha;
    float fadeSpeed;
};

std::vector<Square> squares;
std::default_random_engine generator;
std::uniform_real_distribution<float> distribution(0.0f, 1.0f);
std::uniform_int_distribution<int> gridDistribution(0, GRID_SIZE - 1);

void addSquare() {
    if (squares.size() < MAX_SQUARES - MIN_EMPTY_SQUARES) {
        Square square;
        square.x = (gridDistribution(generator) + 0.5f) * SQUARE_SIZE - 1.0f;
        square.y = (gridDistribution(generator) + 0.5f) * SQUARE_SIZE - 1.0f;
        square.r = distribution(generator);
        square.g = distribution(generator);
        square.b = distribution(generator);
        square.alpha = 1.0f;
        square.fadeSpeed = 0.1f * distribution(generator);
        squares.push_back(square);
    }
}

const char* vertex_shader_source = R"(
#version 330 core
layout (location = 0) in vec2 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in float aAlpha;
out vec3 ourColor;
out float ourAlpha;
void main() {
    gl_Position = vec4(aPos, 0.0, 1.0);
    ourColor = aColor;
    ourAlpha = aAlpha;
}
)";

const char* fragment_shader_source = R"(
#version 330 core
out vec4 FragColor;
in vec3 ourColor;
in float ourAlpha;
void main() {
    FragColor = vec4(ourColor, ourAlpha);
}
)";

int main() {
    if (!glfwInit()) {
        std::cerr << "Failed to initialize GLFW" << std::endl;
        return -1;
    }

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(WINDOW_SIZE, WINDOW_SIZE, "Random Squares", NULL, NULL);
    if (!window) {
        std::cerr << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);

    if (glewInit() != GLEW_OK) {
        std::cerr << "Failed to initialize GLEW" << std::endl;
        return -1;
    }

    glViewport(0, 0, WINDOW_SIZE, WINDOW_SIZE);

    unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertex_shader_source, NULL);
    glCompileShader(vertexShader);

    unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragment_shader_source, NULL);
    glCompileShader(fragmentShader);

    unsigned int shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);

    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    float vertices[] = {
        SQUARE_SIZE, SQUARE_SIZE, 1.0f, 0.0f, 0.0f, 1.0f,
        SQUARE_SIZE, -SQUARE_SIZE, 0.0f, 1.0f, 0.0f, 1.0f,
        -SQUARE_SIZE, -SQUARE_SIZE, 0.0f, 0.0f, 1.0f, 1.0f,
        -SQUARE_SIZE, SQUARE_SIZE, 1.0f, 1.0f, 0.0f, 1.0f
    };

    unsigned int indices[] = {
        0, 1, 3,
        1, 2, 3
    };

    unsigned int VBO, VAO, EBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glGenBuffers(1, &EBO);

    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(2 * sizeof(float)));
    glEnableVertexAttribArray(1);

    glVertexAttribPointer(2, 1, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(5 * sizeof(float)));
    glEnableVertexAttribArray(2);

    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindVertexArray(0);

    float lastTime = 0.0f;
    float deltaTime = 0.0f;
    float lastSquareTime = 0.0f;
    float nextSquareTime = 1.0f + distribution(generator) - 0.5f;

    while (!glfwWindowShouldClose(window)) {
        float currentTime = glfwGetTime();
        deltaTime = currentTime - lastTime;
        lastTime = currentTime;

        if (currentTime - lastSquareTime >= nextSquareTime) {
            addSquare();
            lastSquareTime = currentTime;
            nextSquareTime = 1.0f + distribution(generator) - 0.5f;
        }

        glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        glUseProgram(shaderProgram);
        glBindVertexArray(VAO);

        for (auto it = squares.begin(); it != squares.end();) {
            it->alpha -= it->fadeSpeed * deltaTime;
            if (it->alpha <= 0.0f) {
                it = squares.erase(it);
            } else {
                float model[16] = {
                    SQUARE_SIZE, 0.0f, 0.0f, 0.0f,
                    0.0f, SQUARE_SIZE, 0.0f, 0.0f,
                    0.0f, 0.0f, 1.0f, 0.0f,
                    it->x, it->y, 0.0f, 1.0f
                };
                glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "model"), 1, GL_FALSE, model);
                glUniform3f(glGetUniformLocation(shaderProgram, "ourColor"), it->r, it->g, it->b);
                glUniform1f(glGetUniformLocation(shaderProgram, "ourAlpha"), it->alpha);
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
                ++it;
            }
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteBuffers(1, &EBO);
    glDeleteProgram(shaderProgram);
    glfwSetErrorCallback([](int error, const char* description) {
        std::cerr << "GLFW Error: " << description << std::endl;
    });
    glfwTerminate();
    return 0;
}
