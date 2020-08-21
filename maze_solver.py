import sys
from functions import find_solution, draw_solution
from cv2 import imread, circle
import matplotlib.pyplot as plt


def maze_solver(selected_maze: str):
    # SELECTING MAZE
    img = imread(f'{selected_maze}')
    try:
        height, width = img.shape[0], img.shape[1]
    except AttributeError:
        print("Incorrect image name.")
        exit()

    # SETTING START AND FINISH POINTS
    while True:
        coordinates_input = (input("Do you want to input the start and finish point coordinates?[Y/N]. Answer: "))
        if coordinates_input.lower() == "y":
            try:
                start_x = int(input("Enter start point x coordinate: "))
                start_y = int(input("Enter start point y coordinate: "))
                start = (start_x, start_y)

                finish_x = int(input("Enter finish point x coordinate: "))
                finish_y = int(input("Enter finish point y coordinate: "))
                finish = (finish_x, finish_y)
                print(f"Executing the program with following point: start({start_x},{start_y}) & "
                      f"finish({finish_x},{finish_y})")
                break

            except ValueError:
                print("The coordinates should be numerical (integer or floating point). Please, try again.")
                continue

        elif coordinates_input.lower() == "n":
            start = (6, 4)
            finish = (width - 6, height - 4)
            print("Executing the program with default start and finish points.")
            break

        else:
            print("Incorrect answer. The answer should be 'Y' or 'N'. Please, try again.")

    # IMAGE PROCESSING
    circle(img, start, 2, (0, 255, 0), -1)
    circle(img, finish, 2, (255, 0, 0), -1)

    fig = plt.figure(f'Solution to the {selected_maze}', figsize=(14, 6))
    fig.suptitle(f'Solution to the {selected_maze}', fontsize=15)
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.title.set_text('Unsolved maze')
    plt.xlabel('x axis', size=10)
    plt.ylabel('y axis', size=10)
    ax1.imshow(img)

    p = find_solution(img, start, finish)
    draw_solution(img, p)

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.title.set_text('Solved maze')
    plt.xlabel('x axis', size=10)
    plt.ylabel('y axis', size=10)
    ax2.imshow(img)

    plt.show()
    fig.savefig(f'solution_to_the_{selected_maze}')


def main():
    if len(sys.argv) == 1:
        maze_solver(input("Enter the image of maze name: "))
    else:
        eval(f"maze_solver('{sys.argv[1]}')")


if __name__ == '__main__':
    main()
