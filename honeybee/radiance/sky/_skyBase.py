from abc import ABCMeta, abstractproperty
import os


# TODO: write methods to create and adjust ground glow, source material, etc.
class RadianceSky:
    """Base class for Honeybee Skies."""

    __metaclass__ = ABCMeta

    def __init__(self):
        """Initiate Radiance Sky."""
        self.__head = "# Generated by Honeybee\n"
        self.__main = "# Place holder for Radiance command." + \
            "If you are a developer overwrite this by __genRadianceSkyLine() method." + \
            "otherwise use self.main to set the velaue for main."
        self.__tale = "\nskyfunc glow sky_mat\n" + \
            "0\n" + \
            "0\n" + \
            "4\n" + \
            "1 1 1 0\n" + \
            "sky_mat source sky\n" + \
            "0\n" + \
            "0\n" + \
            "4\n" + \
            "0 0 1 180\n" + \
            "skyfunc glow ground_glow\n" + \
            "0\n" + \
            "0\n" + \
            "4\n" + \
            "1 .8 .5 0\n" + \
            "ground_glow source ground\n" + \
            "0\n" + \
            "0\n" + \
            "4\n" + \
            "0 0 -1 180\n"

    @property
    def isRadianceSky(self):
        """Return True for skies."""
        return True

    @abstractproperty
    def isClimateBased(self):
        """Return True if the sky is created based on values from weather file."""
        pass

    @abstractproperty
    def main(self):
        """Radiance sky line."""
        pass

    def toRadString(self):
        """Return radiance definition as a string."""
        return self.__head + self.main + self.__tale

    def writeToFile(self, targetFolder, name=None):
        """Save sky definition to a file."""
        assert os.path.exists(targetFolder), \
            "%s doesn't exist. create folder and try again." % targetFolder

        name = self.name if not name else name

        filePath = os.path.normpath(os.path.join(targetFolder, name + ".sky"))

        try:
            with open(filePath, "wb") as skyFile:
                # write the sky to file
                skyFile.write(self.toRadString())
                return filePath
        except Exception as e:
            raise Exception("Failed to write the sky file to: %s" % e)
