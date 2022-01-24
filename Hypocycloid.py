"""
Hypocycloid animation by Bennett Kaufmann
Example project using manim, and containing a lot of different python syntax.
Requires manim to run.
"""

from manim import *

class Roll(Animation):
    """Animation for moving along a circle from an origin point

    Takes an Mobject, starting angle, and origin point, then moves
    along the given circle by alpha.
    """
    def __init__(self, shape, angle, origin=ORIGIN, **kwargs):
        super().__init__(shape, **kwargs)
        
        self.start = shape.get_center()
        self.angle = angle
        self.origin = origin
    
    def interpolate_mobject(self, alpha):
        # Smooth motion
        alpha = smooth(alpha, 7)
        # Calculate initial polar position and angle        
        rad = np.linalg.norm(self.start - self.origin)
        th = np.arctan2(self.start[1], self.start[0])

        # Get rectangular position for alpha
        x, y = rad * np.cos(th + self.angle * alpha), rad * np.sin(th + self.angle * alpha)
        
        self.mobject.move_to(self.origin + [x, y, 0])

class Trace(Animation):
    """Animation for tracing a point across the path of the edge

    Takes in a Point, and the n ratio between circles, then moves
    the point along the path that the point would follow.
    """
    def __init__(self, point, n, origin=ORIGIN, **kwargs):
        super().__init__(point, **kwargs)
        
        self.origin = origin
        self.n = n
    
    # Get position at point t over [0, 1]
    @staticmethod
    def position(t, n):
        # Smooth motion
        t = smooth(t, 7) * 2*PI
        return ((-(n - 1) * np.sin(t) + np.sin((n - 1) * t))/(n/2), ((n - 1) * np.cos(t) + np.cos((n - 1) * t))/(n/2), 0)
    
    def interpolate_mobject(self, alpha):
        self.mobject.move_to(self.origin + self.position(alpha, self.n))

class Hypocycloid(Scene):
    """Scene object that contains the manim animation."""
    def construct(self):
        # Title
        t = Text("Hypocycloids").move_to(UP * 2.7)
        
        self.play(Write(t), run_time=3)
        self.wait(1)
        
        # Create circles
        inner = Circle().set_stroke(color=BLUE).set_fill(BLUE, opacity=0.5).shift(UP * 0.2)
        outer = Circle(radius=2).shift(DOWN * 0.8)
        
        self.play(Create(inner), Write(outer))
        self.wait(0.2)
        
        # Create point
        p = Dot(color=YELLOW).shift(UP * 1.2)
        self.play(Create(p), run_time=0.5)
        self.wait(0.3)
        
        # Create caption
        cap = Text(f"n = 2", font_size=28).shift(UP * 2)
        self.play(Write(cap))
        self.wait(0.3)

        # Go through values of n, where the bigger circle is n times bigger
        for n in range(2, 7):
            if n > 2:
                # Shrink inner circle and update caption
                self.play(
                    Transform(inner, Circle(radius=2/n).set_stroke(color=BLUE).set_fill(BLUE, opacity=0.5).align_to(outer, UP)),
                    Transform(p, Dot(color=YELLOW).shift(UP * 1.2)),
                    Transform(cap, Text(f"n = {n}", font_size=28).shift(UP * 2))
                )

            # Create parametric
            self.wait(0.8)
            p_func = Trace(p, n, DOWN * 0.8)
            c_func = Roll(inner, 2*PI, DOWN * 0.8)
            
            curve = ParametricFunction(lambda t: Trace.position(t, n), color=YELLOW).shift(DOWN * 0.8)

            # Draw rolling
            self.play(c_func, p_func, Create(curve), run_time=5, rate_func=linear)

            self.wait(0.2)
            self.play(FadeOut(curve))
            self.wait(0.2)
        
        self.wait(0.5)
