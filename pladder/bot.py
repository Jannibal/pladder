import os

from gi.repository import GLib
from pydbus import SessionBus

from pladder.snusk import SnuskDb


def main():
    pladder_bot = PladderBot()
    bus = SessionBus()
    bus.publish("se.raek.PladderBot", pladder_bot)
    loop = GLib.MainLoop()
    loop.run()


class PladderBot:
    """
    <node>
      <interface name="se.raek.PladderBot">
        <method name="RunCommand">
          <arg direction="in" name="text" type="s" />
          <arg direction="out" name="return" type="s" />
        </method>
      </interface>
    </node>
    """

    def __init__(self):
        state_home = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.environ["HOME"], ".config"))
        snusk_db_path = os.path.join(state_home, "pladder-bot", "snusk_db.json")
        self.snusk_db = SnuskDb(snusk_db_path)

    def RunCommand(self, text):
        parts = text.strip().split(maxsplit=1)
        if len(parts) == 1:
            command, argument = text, ""
        else:
            command, argument = parts
        if command == "snusk" and not argument:
            return self.snusk_db.snusk()
        elif command == "snuska" and argument:
            return self.snusk_db.directed_snusk(argument)
        elif command == "add-snusk":
            arguments = argument.split()
            if len(arguments) == 2:
                if self.snusk_db.add_snusk(*arguments):
                    return self.snusk_db.example_snusk(*arguments)
                else:
                    return "Hörrudu! Den där finns ju redan!"
        return ""


if __name__ == "__main__":
    main()
