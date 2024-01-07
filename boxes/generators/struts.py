# Copyright (C) 2013-2016 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *

class Struts(Boxes):
    """Things with Struts"""

    ui_group = "Unstable" # see ./__init__.py for names

    def __init__(self) -> None:
        Boxes.__init__(self)
        # Uncomment the settings for the edge types you use
        # use keyword args to set default values
        self.addSettingsArgs(edges.FingerJointSettings, finger=1.0,space=1.0)

        # remove cli params you do not need
        self.buildArgParser(x=150, y=100)
        # Add non default cli params if needed (see argparse std lib)
        self.argparser.add_argument(
            "--strutx", action="store", type=float, default=10,
            help="Strut dimension in x direction (multiples of thickness)")

        self.argparser.add_argument(
            "--struty", action="store", type=float, default=10,
            help="Strut dimension in y direction (multiples of thickness)")

        self.argparser.add_argument(
            "--strength",  action="store", type=float, default=3,
            help="Strength of the struts")
        self.argparser.add_argument(
            "--factor",  action="store", type=float, default=1.4,
            help="Factor for diagonal struts")
        self.argparser.add_argument(
            "--nx", action="store", type=int, default=2,
            help="Number of triangle pairs in x direction")
        self.argparser.add_argument(
            "--ny", action="store", type=int, default=2,
            help="Number of triangle pairs in y direction")
        self.argparser.add_argument(
            "--spacerdir", action="store", type=str, default="rect",
            help="Direction of spacers (diag, rect)"
        )
        self.argparser.add_argument(
            "--axleradius",  action="store", type=float, default=8.0,
            help="Diameter to hold axle")
        self.argparser.add_argument(
            "--axler1", action="store", type=float, default=10.0,
            help="Diameters of axle r1 (outer)")
        self.argparser.add_argument(
            "--axler2", action="store", type=float, default=8.0,
            help="Diameters of axle r2 (for gear)")
        self.argparser.add_argument(
            "--axler3", action="store", type=float, default=5.0,
            help="Diameters of axle r3 (for ends)")
        self.argparser.add_argument(
            "--axlespec", action="store", type=str, default="5,10,8,7*7,4*5",
            help="Spec for the axle. Comma seperated list of radius each of thickness. Use x*r to have x-times radius segments"
        )
        self.argparser.add_argument(
            "--axlelength", action="store", type=float, default=40.0,
            help="Total length of axle")
        self.argparser.add_argument(
            "--teeth1",  action="store", type=int, default=12,
            help="number of teeth")
        self.argparser.add_argument(
            "--shaft1", action="store", type=float, default=6.,
            help="diameter of the shaft 1")
        self.argparser.add_argument(
            "--dpercentage1", action="store", type=float, default=75,
            help="percent of the D section of shaft 1 (100 for round shaft)")

        self.argparser.add_argument(
            "--teeth2",  action="store", type=int, default=32,
            help="number of teeth in the other size of gears")
        self.argparser.add_argument(
            "--shaft2", action="store", type=float, default=0.0,
            help="diameter of the shaft2 (zero for same as shaft 1)")
        self.argparser.add_argument(
            "--dpercentage2", action="store", type=float, default=0,
            help="percent of the D section of shaft 1 (0 for same as shaft 1)")

        self.argparser.add_argument(
            "--modulus",  action="store", type=float, default=2,
            help="size of teeth (diameter / #teeth) in mm")
        self.argparser.add_argument(
            "--pressure_angle",  action="store", type=float, default=20,
            help="angle of the teeth touching (in degrees)")
        self.argparser.add_argument(
            "--profile_shift",  action="store", type=float, default=20,
            help="in percent of the modulus")


    def expandAxleSpec(self, spec, thickness):
        finalSpec = []
        foundGrow = False
        for e in spec.split(","):
            if '*' in e:
                a,b = e.split("*")
                finalSpec.append((float(b), thickness * float(a)))
            else:
                finalSpec.append((float(e), thickness))

        return finalSpec

    def getSpecLength(self, spec):
        l = 0
        for i, e in enumerate(spec):
            l += e[1]
        return l

    def getSpecHeight(self, spec):
        rmax = 0
        for i,e in enumerate(spec):
            if e[0] > rmax:
                rmax = e[0]
        return 2.0 * rmax

    def drawAxleSide(self, spec):
        n = len(spec)
        for i, e in enumerate(spec):
            self.edge(e[1])
            if i < (n-1):
                step = e[0] - spec[i+1][0]
                # Not the last one
                if step < 0:
                    # Next radius is smaller
                    self.corner(-90)
                    self.edge(-1.0*step)
                    self.corner(90)
                else:
                    self.corner(90)
                    self.edge(step)
                    self.corner(-90)
        self.corner(90)

    def drawIncut(self, spec, incut):
        self.edge(spec[-1][0] - self.thickness/2.0)
        self.corner(90)
        self.edge(incut)
        self.corner(-90)
        self.edge(self.thickness)
        self.corner(-90)
        self.edge(incut)
        self.corner(90)
        self.edge(spec[-1][0] - self.thickness/2.0)
        self.corner(90)

    def axleOutline(self, spec, reverse, move, label=None):
        spec = self.expandAxleSpec(spec, self.thickness)
        if reverse:
            spec.reverse()
        l = self.getSpecLength(spec)
        h = self.getSpecHeight(spec)

        if self.move(l, h, move, before=True, label=label):
            return

        incut = l * 0.5
        self.moveTo(0, h/2.0 - spec[0][0], 0)

        self.drawAxleSide(spec)
        self.drawIncut(spec, incut)
        spec.reverse()
        self.drawAxleSide(spec)
        self.edge(2.0 * spec[-1][0])
        self.corner(90)
        self.move(l, h, move, label=label)

    def crosshole(self, radius):

        def fragment(f1, f2):
            self.edge(radius - 0.5 * self.thickness)
            self.corner(-1.0 * f1 * 90)
            self.edge(radius - 0.5 * self.thickness)
            self.corner(f2 * 90.0)

        self.moveTo(radius, 0.5*self.thickness, 180)
        for i in range(4):
            fragment(1.0, 1.0)
            self.edge(self.thickness)
            self.corner(90)

    def axleEnd(self, rCrosshole, axleradius, move, label=None):
        if self.move(self.spacing + 2.0 * axleradius, self.spacing + 2.0 * axleradius, where=move, before=True, label=label):
            return

        self.moveTo(axleradius + 0.5 * self.spacing, axleradius +  0.5 * self.spacing)
        self.circle(0.0, 0.0, axleradius)

        self.crosshole(rCrosshole)
        self.move(self.spacing + 2.0 * axleradius, self.spacing + 2.0 * axleradius, where=move, label=label)

    def axlePulley(self, x, y, rCrosshole, move):
        if self.move(self.spacing + x, self.spacing + y, where=move, before=True):
            return

        self.edge(x)
        self.corner(90)
        self.edge(y)
        self.corner(90)
        self.edge(x)
        self.corner(90)
        self.edge(y)
        self.corner(90)

        self.moveTo(2*rCrosshole, y/2)

        self.crosshole(rCrosshole)
        self.move(self.spacing + x, self.spacing + y, where=move)

    def render(self):
        # adjust to the variables you want in the local scope
        x, y = self.x, self.y
        strutx, struty = self.strutx * self.thickness, self.struty * self.thickness
        t = self.thickness
        s = self.strength
        f = self.factor
        nx = self.nx
        ny = self.ny

        # Triangle measurements
        tri_x = (strutx - s)/float(nx) - s - f * s
        tri_y = (struty - s) / float(ny) - s
        tri_h = math.sqrt(tri_x**2 + tri_y**2)

        alpha = math.atan2(tri_x, tri_y) / math.pi / 2.0 * 360.0

        # Create new Edges here if needed E.g.:
        fjs = edges.FingerJointSettings(self.thickness, style="springs", relative=False,
                                      space = 10, finger=10,
                                      width=self.thickness)

        self.p = edges.FingerJointEdge(self, fjs)
        self.p.char = "a" # 'a', 'A', 'b' and 'B' is reserved for being used within generators
        self.addPart(self.p)
        def struts(edge_num):
            def draw_tri_even(inv=1.0):
                self.polyline(tri_y, -90, tri_x, -90 - alpha, tri_h, 180 + alpha)
                self.moveTo(tri_y, -1.0 * (tri_x + s * f), 180)
                self.polyline(tri_y, -90, tri_x, -90 - alpha, tri_h, 180 + alpha)
                self.moveTo(tri_y, s, 180)
            def draw_tri_odd(inv=1.0):
                self.polyline(tri_y, -180 + alpha, tri_h, -90 - alpha, tri_x, -90)
                self.moveTo(tri_y, -f * s, -90)
                self.polyline(tri_x, -90, tri_y, 180+alpha, tri_h, -alpha)
                self.moveTo(-tri_y, -tri_x - s)

            if edge_num != 0:
                return

            self.moveTo(s, s, 90)

            for j in range(ny):
                for i in range(nx):
                    if (i+j) % 2 == 0:
                        draw_tri_even()
                    else:
                        draw_tri_odd()
                self.moveTo(tri_y + s, (nx * tri_x + nx * f * s + nx * s))

        def fingerHolesDiag(edge_num):

            if edge_num == 0:
                self.circle(x / 3, y / 2, self.axleradius)
                with self.saved_context():
                    self.set_source_color(Color.ANNOTATIONS)
                    sx = 1.0 / math.sqrt(2.0) * strutx
                    sy = 1.0 / math.sqrt(2.0) * struty
                    self.moveTo(sx, sy)
                    self.rectangularWall(x - 2 * sx, y - 2 * sy)

            self.moveTo(0.0, 0.0, -45)
            self.fingerHolesAt(0.0, 0.0, strutx)

        def fingerHolesRect(edge_num):

            if edge_num == 0:
                self.circle(x / 3, y / 2, self.axleradius)
                self.circle(x / 3 + self.gearr1 + self.gearr2, y / 2, self.axleradius)
                with self.saved_context():
                    self.set_source_color(Color.ANNOTATIONS)
                    sx = 3*self.thickness
                    sy = 3*self.thickness
                    self.moveTo(sx, sy)
                    self.rectangularWall(x - 2 * sx, y - 2 * sy)

            with self.saved_context():
                self.moveTo(2*self.thickness, 3*self.thickness, 0)
                self.fingerHolesAt(0.0, 0.0, strutx)

            with self.saved_context():
                self.moveTo(3*self.thickness, 2*self.thickness, -90)
                self.fingerHolesAt(0.0, 0.0, strutx)


        self.debug = True
        self.gears(teeth=self.teeth1, dimension=self.modulus,
                   angle=self.pressure_angle, profile_shift=self.profile_shift,
                   mount_diameter=3.0 * self.axler2,
                   callback=lambda: self.crosshole(self.axler2),
                   move="right")
        self.gearr1, d1, d1 = self.gears.sizes(
            teeth=self.teeth1, dimension=self.modulus,
            angle=self.pressure_angle, profile_shift=self.profile_shift)

        self.gears(teeth=self.teeth2, dimension=self.modulus,
                   angle=self.pressure_angle, profile_shift=self.profile_shift,
                   mount_diameter=3.0 * self.axler2,
                   callback=lambda: self.crosshole(self.axler2),
                   move="right")

        self.gearr2, d2, d2 = self.gears.sizes(
            teeth=self.teeth2, dimension=self.modulus,
            angle=self.pressure_angle, profile_shift=self.profile_shift)

        if self.spacerdir == "rect":
            self.rectangularWall(x, y, "eeee", move="right", callback=fingerHolesRect)
            self.rectangularWall(x, y, "eeee", move="right", callback=fingerHolesRect)

            move="down left"
            for i in range(8):
                self.rectangularWall(strutx, struty, "fefe", move=move,callback=struts)
                move = "left"
        else:
            self.rectangularWall(x, y, "eeee", move="right", callback=fingerHolesDiag)
            self.rectangularWall(x, y, "eeee", move="right", callback=fingerHolesDiag)

            move="down left"
            for i in range(4):
                self.rectangularWall(strutx, struty, "fefe", move=move,callback=struts)
                move = "left"


        self.axleOutline(self.axlespec, reverse=False,move="down right", label="ax1")
        self.axleOutline(self.axlespec, reverse=True, move="right", label="ax1rev")
        self.axleOutline(self.axlespec, reverse=False,move="right")
        self.axleOutline(self.axlespec, reverse=True, move="right")

        self.axleEnd(7.0, 1.5*self.axleradius, move="down left")
        self.axleEnd(7.0, 1.5*self.axleradius, move="left")
        self.axleEnd(5.0, self.axleradius, move="left", label="End1")
        self.axleEnd(5.0, self.axleradius, move="left", label="End2")
        self.axleEnd(5.0, self.axleradius, move="left", label="End3")
        self.axleEnd(5.0, self.axleradius, move="left")
        self.axleEnd(5.0, self.axleradius + 1.0, move="left")
        self.axleEnd(5.0, self.axleradius + 1.0, move="left")
        self.axlePulley(40, 15, 5.0, "left")

        self.debug=False