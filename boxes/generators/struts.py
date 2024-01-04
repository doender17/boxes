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
        # self.addSettingsArgs(edges.StackableSettings)
        # self.addSettingsArgs(edges.HingeSettings)
        # self.addSettingsArgs(edges.SlideOnLidSettings)
        # self.addSettingsArgs(edges.ClickSettings)
        # self.addSettingsArgs(edges.FlexSettings)

        # remove cli params you do not need
        self.buildArgParser(x=400, y=100)
        # Add non default cli params if needed (see argparse std lib)
        self.argparser.add_argument(
            "--strutx", action="store", type=float, default=40,
            help="Strength of the struts")

        self.argparser.add_argument(
            "--struty", action="store", type=float, default=40,
            help="Strength of the struts")

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
            "--spacerdir", action="store", type=str, default="diag",
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


    def axle1(self, move):
        e = self.edges.get("a")
        r1 = self.axler1
        r2 = self.axler2
        r3 = self.axler3
        totallength = self.axlelength
        incut = (totallength - 3.0*self.thickness) * 0.5

        cr = 1.0

        if self.move(totallength + self.spacing, 2*r1 + self.spacing, move, before=True):
            return

        def lower_to_tip():
            self.moveTo(totallength - self.spacing, 0.0, 90)
            e(2 * r1)
            self.corner(90)
            self.edge(self.thickness)
            self.corner(90)
            self.edge(r1-r2)
            self.corner(-90)
            self.edge(self.thickness)
            self.corner(90)
            self.edge(r2-r3)
            self.corner(-90)
            self.edge(totallength - 3.0 * self.thickness - cr)

        def tip():
            self.corner(90, cr)
            self.edge(r3 - self.thickness/2.0 - cr)
            self.corner(90)
            self.edge(incut)
            self.corner(-90)
            self.edge(self.thickness)
            self.corner(-90)
            self.edge(incut)
            self.corner(90)
            self.edge(r3 - self.thickness/2.0 - cr)
            self.corner(90, cr)

        def upper_back():
            self.edge(totallength - 3.0 * self.thickness - cr)
            self.corner(-90)
            self.edge(r2 - r3)
            self.corner(90)
            self.edge(self.thickness)
            self.corner(-90)
            self.edge(r1 - r2)
            self.corner(90)
            self.edge(self.thickness)
            self.corner(-90)

        with self.saved_context():
            lower_to_tip()
            tip()
            upper_back()

        self.move(totallength + self.spacing, 2 * r1 + self.spacing, move)

    def axle2(self, move):

        r1 = self.axler1
        r2 = self.axler2
        r3 = self.axler3
        totallength = self.axlelength
        incut = (totallength - 3.0*self.thickness) * 0.5
        cr = 1.0

        if self.move(totallength + self.spacing, 2*r1 + self.spacing, move, before=True):
            return


        def lower_to_tip():
            self.corner(-90)
            self.edge(r1-r3)
            self.corner(90)
            self.edge(self.thickness)
            self.corner(90)
            self.edge(r1-r2)
            self.corner(-90)
            self.edge(self.thickness)
            self.corner(90)
            self.edge(r2-r3)
            self.corner(-90)
            self.edge(totallength - 3.0 * self.thickness - cr)
            self.corner(90, cr)

        def base():
            # |
            # ----------
            #           |
            # ----------
            # |
            self.moveTo(0, r2 + r3 + self.spacing, -90)
            self.edge(r3 - self.thickness/2.0 - cr)
            self.corner(90)
            self.edge(totallength-incut)
            self.corner(-90)
            self.edge(self.thickness)
            self.corner(-90)
            self.edge(totallength-incut)
            self.corner(90)
            self.edge(r3 - self.thickness/2.0 - cr)
            self.corner(90, cr)
            self.edge(self.thickness - cr)
        def tip():
            self.edge(r3 - self.thickness/2.0 - cr)
            self.corner(90)
            self.edge(self.thickness)
            self.corner(180)
            self.edge(self.thickness)
            self.corner(90)
            self.edge(self.thickness)
            self.corner(90)
            self.edge(self.thickness)
            self.corner(180)
            self.edge(self.thickness)
            self.corner(90)
            self.edge(r3 - self.thickness/2.0 - cr)
            self.corner(90, cr)
            pass
        def upper_back():
            self.edge(totallength - 3.0 * self.thickness - cr)
            self.corner(-90)
            self.edge(r2 - r3)
            self.corner(90)
            self.edge(self.thickness)
            self.corner(-90)
            self.edge(r1 - r2)
            self.corner(90)
            self.edge(self.thickness)
            self.corner(90)
            self.edge(r1-r3)
            self.corner(-90)
            self.edge(self.thickness - cr)
            self.corner(90,cr)

        with self.saved_context():
            base()
            lower_to_tip()
            tip()
            upper_back()

        self.move(totallength + self.spacing, 2*r1 + self.spacing, move)

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

    def axleEnd(self, move):
        if self.move(self.spacing + 2.0 * self.axleradius, self.spacing + 2.0 * self.axleradius, where=move, before=True):
            return

        self.moveTo(self.axleradius + 0.5 * self.spacing, self.axleradius +  0.5 * self.spacing)
        self.circle(0.0, 0.0, self.axleradius)

        self.crosshole(self.axler3)
        self.move(self.spacing + 2.0 * self.axleradius, self.spacing + 2.0 * self.axleradius, where=move)

    def render(self):
        # adjust to the variables you want in the local scope
        x, y = self.x, self.y
        strutx, struty = self.strutx, self.struty
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


        if self.spacerdir == "rect":
            pass
            for i in range(8):
                self.rectangularWall(strutx, struty, "fefe", move="left",callback=struts)
            self.rectangularWall(x, y, "eeee", move="down", callback=fingerHolesRect)
            self.rectangularWall(x, y, "eeee", move="down", callback=fingerHolesRect)

        else:
            for i in range(4):
                self.rectangularWall(strutx, struty, "fefe", move="left",callback=struts)

            self.rectangularWall(x, y, "eeee", move="down", callback=fingerHolesDiag)
            self.rectangularWall(x, y, "eeee", move="left", callback=fingerHolesDiag)

        self.axle1(move="right down")
        self.axle2(move="right")

        self.axleEnd(move="right")
        self.axleEnd(move="right")

        self.gears(teeth=self.teeth2, dimension=self.modulus,
                   angle=self.pressure_angle, profile_shift=self.profile_shift,
                   mount_diameter=3.0 * self.axler2,
                   callback=lambda: self.crosshole(self.axler2),
                   move="down")
