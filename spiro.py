import math
import random, argparse
from datetime import datetime
import turtle
from PIL import Image
import fractions


class Spiro:
    def __init__(self, x, y, color, R, r, l):
        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.step = 5
        self.drawing_complete = False

        self.setparams(x, y, color, R, r, l)
        self.restart()

    def setparams(self, x, y, color, R, r, l):
        self.x = x
        self.y = y
        self.color = color
        self.R = R
        self.r = r
        self.l = l
        #reducing r/R to its smallest by using gcd
        gcdVal = math.gcd(int(self.R), int(self.r))
        self.nRot = int(self.r/gcdVal)
        self.k = r/float(R)
        self.t.color(*color)
        self.a = 0

    def restart(self):
        self.drawing_complete = False
        self.t.showturtle()
        #goes up
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.x + x, self.y + y)
        self.t.down()

    def draw(self):
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360 * self.nRot + 1, self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
            self.t.setpos(self.x + x, self.y + y)
        self.t.hideturtle()

    def update(self):
        if self.drawing_complete:
            return

        self.a += self.step
        R, k, l = self.R, self.k, self.l
        a = math.radians(self.a)
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.x + x, self.y + y)

        if self.a >= 360*self.nRot:
            self.drawing_complete = True
            self.t.hideturtle()


class SpiroAnimator:
    def __init__(self, N):
        self.deltaT = 10
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        #create the Spiro objects
        self.spiros = []
        for i in range(N):
            #generate random parameters
            random_params = self.genRandomParams()
            spiro = Spiro(*random_params)
            self.spiros.append(spiro)
        turtle.ontimer(self.update, self.deltaT)

    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        x = random.randint(-width//2, width//2)
        y = random.randint(-height//2, height//2)
        color = (random.random(), random.random(), random.random())
        return x, y, color, R, r, l

    def restart(self):
        for spiro in self.spiros:
            spiro.clear()
            random_params = self.genRandomParams()
            spiro.setparams(*random_params)
            spiro.restart()

    def update(self):
        nComplete = 0
        for spiro in self.spiros:
            spiro.update()
            if spiro.drawing_complete:
                nComplete += 1
        if nComplete == len(self.spiros):
            self.restart()
        turtle.ontimer(self.update, self.deltaT)

    def toggle_turtle(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()


def saveDrawing():
    turtle.hideturtle()
    dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    fileName = 'spiro-' + dateStr
    print('saving to file')
    canvas = turtle.getcanvas()
    canvas.postscript(file=fileName+'.eps')
    img = Image.open(fileName+'.eps')
    img.save(fileName + '.png', 'png')
    turtle.showturtle()


def main():
    descStr = """This program draws Spirographs using the Turtle module.     When run with no arguments, this program draws random Spirographs.    Terminology:    R: radius of outer circle    r: radius of inner circle    l: ratio of hole distance to r    """
    parser = argparse.ArgumentParser(description=descStr)
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False, help="The three arguments in sparams: R, r, l.")
    args = parser.parse_args()
    turtle.setup(width=0.8)
    turtle.shape('turtle')
    turtle.title("Spirographs")
    turtle.onkey(saveDrawing, "s")
    turtle.listen()

    turtle.hideturtle()

    if args.sparams:
        params = [float(x) for x in args.sparams]
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        spiroAnim = SpiroAnimator(4)
        turtle.onkey(spiroAnim.toggle_turtle, "t")
        turtle.onkey(spiroAnim.restart, "space")

    turtle.mainloop()

if __name__ == '__main__':
    main()
