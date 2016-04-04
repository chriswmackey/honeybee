import os
from commandbase import RadianceCommand
from ..parameters.gridbased import LowQuality
from ..datatype import RadiancePath


class Rtrace(RadianceCommand):
    u"""Create a grid-based Radiance ray-tracer.

    Read more at: http://radsite.lbl.gov/radiance/man_html/rtrace.1.html

    Attributes:
        projectName: Name of this run. It will be used to set-up results file
            name (Default: untitled).
        octFile: Full path to input oct files (Default: None)
        pointFile: Full path to input pt files (Default: None)
        simulationType: An integer to define type of analysis.
            0: Illuminance (lux), 1: Radiation (kWh), 2: Luminance (Candela)
            (Default: 0)
        radianceParameters: Radiance parameters for this analysis.
            (Default: girdbased.LowQuality)
    """

    outputFile = RadiancePath("res", "results file", extension=".res")
    octFile = RadiancePath("oct", "octree file", extension=".oct")
    pointFile = RadiancePath("points", "test point file", extension=".pts")

    def __init__(self, projectName="untitled", octFile=None, pointFile=None,
                 simulationType=0, radianceParameters=None):
        """Initialize the class."""
        # Initialize base class to make sure path to radiance is set correctly
        RadianceCommand.__init__(self)

        self.outputFile = projectName if projectName.lower().endswith(".res") \
            else projectName + ".res"
        """oct file name which is usually the same as the project name (Default: untitled)"""

        self.octFile = octFile
        """Full path to input oct file."""

        self.pointFile = pointFile
        """Full path to input points file."""

        self.simulationType = simulationType
        """Simulation type: 0: Illuminance(lux), 1: Radiation (kWh), 2: Luminance (Candela)
            (Default: 0)
        """

        self.radianceParameters = radianceParameters
        """Radiance parameters for this analysis (Default: RadianceParameters.LowQuality)."""

        # add -h to parameters to get no header, True is no header
        self.radianceParameters.addRadianceBoolFlag("h", "output header switch", defaultValue=True)

        # add error file as an extra parameter for rtrace.
        # this can be added under default radiance parameters later.
        self.radianceParameters.addRadianceValue("e", "error output file", defaultValue="error.txt")

    @property
    def simulationType(self):
        """Get/set simulation Type.

        0: Illuminance(lux), 1: Radiation (kWh), 2: Luminance (Candela) (Default: 0)
        """
        return self.__simType

    @simulationType.setter
    def simulationType(self, value):
        try:
            value = int(value)
        except:
            value = 0

        assert 0 <= value <= 2, \
            "Simulation type should be between 0-2. Current value: {}".format(value)

        # If this is a radiation analysis make sure the sky is climate-based
        if value == 1:
            assert self.sky.isClimateBased, \
                "The sky for radition analysis should be climate-based."

        self.__simType = value

    @property
    def iswitch(self):
        """Return I/i switch.

        -I > Boolean switch to compute irradiance rather than radiance, with the input
        origin and direction interpreted instead as measurement point and orientation.
        """
        _switch = {0: "-I", 1: "-I", 2: ""}

        return _switch[self.simulationType]

    @property
    def radianceParameters(self):
        """Get and set Radiance parameters."""
        return self.__radParameters

    @radianceParameters.setter
    def radianceParameters(self, radParameters):
        if not radParameters:
            radParameters = LowQuality()
        assert hasattr(radParameters, 'isGridBasedRadianceParameters'), \
            "%s is not a radiance parameters." % type(radParameters)
        self.__radParameters = radParameters

    # TODO: Implement relative path
    def toRadString(self, relativePath=False):
        """Return full command as a string."""
        return "%s %s %s %s < %s > %s" % (
            os.path.join(self.radbinPath, "rtrace"),
            self.iswitch,
            self.radianceParameters.toRadString(),
            self.octFile.toRadString(),
            self.pointFile.toRadString(),
            self.outputFile.toRadString()
        )

    def inputFiles(self):
        """Input files for this command."""
        return self.octFile, self.pointFile


if __name__ == "__main__":
    oc = Rtrace()
