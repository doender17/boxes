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
            "--strutx", action="store", type=float, default=50,
            help="Strength of the struts")

        self.argparser.add_argument(
            "--struty", action="store", type=float, default=50,
            help="Strength of the struts")

        self.argparser.add_argument(
            "--strength",  action="store", type=float, default=5,
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
        #s = edges.FingerJointSettings(self.thickness, relative=False,
        #                              space = 10, finger=10,
        #                              width=self.thickness)

        #p = edges.FingerJointEdge(self, s)
        #p.char = "a" # 'a', 'A', 'b' and 'B' is reserved for being used within generators

        def struts(edge_num):
            if edge_num != 0:
                return
            self.moveTo(s, s)
            for j in range(ny):
                for i in range(nx):
                    self.polyline(0,90,tri_y, -90, tri_x, -90-alpha, tri_h, alpha + 90)
                    self.moveTo((s * f), 0)
                    self.polyline(0, 90-alpha, tri_h, -180+ alpha, tri_y, -90, tri_x, 180)
                    self.moveTo(tri_x + s, 0)
                self.moveTo(-1.0* (nx * tri_x + nx * f * s + nx * s), tri_y + s, 180)
                self.moveTo(0,0, 180)

        def fingerHoles(edge_num):

            if edge_num == 0:
                with self.saved_context():
                    self.set_source_color(Color.ANNOTATIONS)
                    sx = 1.0/math.sqrt(2.0) * strutx
                    sy = 1.0 / math.sqrt(2.0) * struty
                    self.moveTo(sx, sy)
                    self.rectangularWall(x - 2 * sx, y - 2 * sy)

            self.moveTo(0.0, 0.0, -45)
            self.fingerHolesAt(0.0, 0.0, strutx)

        self.rectangularWall(strutx, struty, "fefe", move="left",callback=struts)
        self.rectangularWall(strutx, struty, "fefe", move="left", callback=struts)
        self.rectangularWall(strutx, struty, "fefe", move="left", callback=struts)
        self.rectangularWall(strutx, struty, "fefe", move="left", callback=struts)

        self.rectangularWall(x, y, "eeee", move="down", callback=fingerHoles)
        self.rectangularWall(x, y, "eeee", move="left", callback=fingerHoles)

        # render your parts here

